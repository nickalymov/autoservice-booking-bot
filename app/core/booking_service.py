"""Модуль ядра бизнес-логики бронирования и управления ремонтами.

Обеспечивает проверку доступности слотов, разрешение коллизий,
создание заявок, синхронизацию с Google Календарём, расчет загрузки цеха
и ведение жизненного цикла статусов ремонтов.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import datetime
import zoneinfo

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import PostCode
from app.config import TIMEZONE_NAME
from app.config import UserRole
from app.core.permissions import can_manage_appointment
from app.database.models import Appointment
from app.database.models import HistoryActionType
from app.database.models import Post
from app.database.models import User
from app.database.repositories import AppointmentRepository
from app.database.repositories import HistoryLogRepository
from app.database.repositories import PostRepository
from app.database.repositories import UserRepository
from app.database.session import get_async_session
from app.schemas.appointment import AppointmentDraft
from app.schemas.appointment import AppointmentStatus
from app.services.calendar_service import CalendarServiceError
from app.services.calendar_service import GoogleCalendarService


class BookingError(Exception):
    """Базовое исключение бизнес-логики бронирования."""


class SlotConflictError(BookingError):
    """Вызывается при попытке занять уже занятый временной интервал."""


class PermissionDeniedError(BookingError):
    """Вызывается при попытке выполнить несанкционированное действие."""


class EntityNotFoundError(BookingError):
    """Вызывается, если запрашиваемая сущность не найдена в базе данных."""


@dataclass(frozen=True)
class SlotCheckResult:
    """Результат проверки доступности временного слота.

    Attributes:
        is_available: Доступен ли запрошенный пост в указанное время.
        conflicting_appointment: Запись, создающая накладку, или None.
        available_posts: Список свободных постов на этот интервал.
    """

    is_available: bool
    conflicting_appointment: Appointment | None
    available_posts: list[Post]


@dataclass(frozen=True)
class PostScheduleItem:
    """Расписание отдельного поста за день.

    Attributes:
        post: Объект рабочего поста.
        appointments: Список запланированных на пост записей.
    """

    post: Post
    appointments: list[Appointment]


@dataclass(frozen=True)
class DayScheduleOverview:
    """Сводная загрузка автосервиса за календарный день.

    Attributes:
        target_date: Дата расписания.
        posts_schedule: Список расписаний по каждому посту.
    """

    target_date: datetime.date
    posts_schedule: list[PostScheduleItem]


async def _fetch_active_user_and_appointment(
    session: AsyncSession,
    user_telegram_id: int,
    public_id: str,
) -> tuple[User, Appointment]:
    """Проверяет активность пользователя и находит заявку по публичному ID.

    Args:
        session: Асинхронная сессия базы данных.
        user_telegram_id: Telegram ID сотрудника.
        public_id: Публичный номер записи.

    Returns:
        Кортеж из объекта пользователя и найденной заявки.

    Raises:
        PermissionDeniedError: Если пользователь не найден или неактивен.
        EntityNotFoundError: Если заявка не найдена.
    """
    user_repo = UserRepository(session)
    appt_repo = AppointmentRepository(session)

    user = await user_repo.get_by_telegram_id(user_telegram_id)
    if user is None or not user.is_active:
        raise PermissionDeniedError('Доступ запрещен.')

    appointment = await appt_repo.get_by_public_id(public_id)
    if appointment is None:
        raise EntityNotFoundError('Запись не найдена.')

    return user, appointment


class BookingService:
    """Сервис управления бронированием и жизненным циклом ремонтов.

    Attributes:
        _session_factory: Фабрика асинхронных сессий базы данных.
        _calendar_service: Сервис синхронизации с Google Календарём.
        _booking_lock: Асинхронный мьютекс для защиты от состояния гонки.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        calendar_service: GoogleCalendarService | None = None,
    ) -> None:
        """Инициализирует сервис с заданной фабрикой сессий и календарем.

        Args:
            session_factory: Фабрика создания сессий SQLAlchemy.
            calendar_service: Опциональный сервис интеграции с календарем.
        """
        self._session_factory = session_factory
        self._calendar_service = calendar_service
        self._booking_lock = asyncio.Lock()

    async def check_slot(
        self,
        post_code: PostCode | None,
        start_dt: datetime.datetime,
        end_dt: datetime.datetime,
        exclude_appointment_id: int | None = None,
    ) -> SlotCheckResult:
        """Проверяет доступность слота и возвращает свободные альтернативы.

        Args:
            post_code: Код выбранного поста или None.
            start_dt: Время начала интервала.
            end_dt: Время окончания интервала.
            exclude_appointment_id: ID записи для исключения при проверке.

        Returns:
            Результат проверки доступности со списком альтернативных постов.

        Raises:
            BookingError: Если дата записи приходится на воскресенье.
        """
        if start_dt.weekday() == 6:
            raise BookingError(
                'Воскресенье — выходной день автосервиса. Запись возможна '
                'только с понедельника по субботу.',
            )

        async with get_async_session(self._session_factory) as session:
            post_repo = PostRepository(session)
            appt_repo = AppointmentRepository(session)

            active_posts = list(await post_repo.get_all_active())
            no_post_obj = await post_repo.get_by_code(PostCode.NO_POST)

            target_post: Post | None = None
            if post_code and post_code != PostCode.NO_POST:
                target_post = await post_repo.get_by_code(post_code)
                if target_post is None:
                    raise EntityNotFoundError(
                        f'Рабочий пост с кодом {post_code} не найден.',
                    )

            conflicting_appt: Appointment | None = None
            is_available = True

            if target_post is not None:
                conflicts = await appt_repo.get_conflicts(
                    post_id=target_post.id,
                    start_dt=start_dt,
                    end_dt=end_dt,
                    exclude_appointment_id=exclude_appointment_id,
                )
                if conflicts:
                    is_available = False
                    conflicting_appt = conflicts[0]

            available_posts: list[Post] = []
            for post in active_posts:
                if post.code == PostCode.NO_POST:
                    continue
                post_conflicts = await appt_repo.get_conflicts(
                    post_id=post.id,
                    start_dt=start_dt,
                    end_dt=end_dt,
                    exclude_appointment_id=exclude_appointment_id,
                )
                if not post_conflicts:
                    available_posts.append(post)

            if no_post_obj is not None:
                available_posts.append(no_post_obj)

            return SlotCheckResult(
                is_available=is_available,
                conflicting_appointment=conflicting_appt,
                available_posts=available_posts,
            )

    async def confirm_and_create(
        self,
        draft: AppointmentDraft,
        user_telegram_id: int,
    ) -> Appointment:
        """Создает подтвержденную запись в БД и в Google Календаре.

        Args:
            draft: Экземпляр черновика заявки.
            user_telegram_id: Telegram ID сотрудника, создающего запись.

        Returns:
            Созданный объект записи на ремонт.

        Raises:
            PermissionDeniedError: Если сотрудник не найден или неактивен.
            SlotConflictError: Если выбранный слот занят.
            BookingError: При ошибке валидации данных или Google Calendar.
        """
        if (
            not draft.is_ready_for_confirmation()
            or draft.start_datetime is None
            or draft.end_datetime is None
        ):
            raise BookingError(
                'Не заполнены все обязательные поля для подтверждения.',
            )

        if draft.start_datetime.weekday() == 6:
            raise BookingError(
                'Воскресенье — выходной день автосервиса.',
            )

        async with self._booking_lock:
            async with get_async_session(self._session_factory) as session:
                user_repo = UserRepository(session)
                post_repo = PostRepository(session)
                appt_repo = AppointmentRepository(session)
                history_repo = HistoryLogRepository(session)

                creator = await user_repo.get_by_telegram_id(user_telegram_id)
                if creator is None or not creator.is_active:
                    raise PermissionDeniedError(
                        'У вас нет прав для создания записи в системе.',
                    )

                target_master: User | None = None
                if draft.master_id is not None:
                    target_master = await user_repo.get_by_id(draft.master_id)
                elif draft.master_telegram_id != user_telegram_id:
                    target_master = await user_repo.get_by_telegram_id(
                        draft.master_telegram_id,
                    )
                if target_master is None:
                    target_master = creator

                target_master_id = target_master.id

                post_id: int | None = None
                post_obj: Post | None = None
                if draft.post_code and draft.post_code != PostCode.NO_POST:
                    post_obj = await post_repo.get_by_code(draft.post_code)
                    if post_obj is not None:
                        post_id = post_obj.id
                        slot_check = await self.check_slot(
                            post_code=draft.post_code,
                            start_dt=draft.start_datetime,
                            end_dt=draft.end_datetime,
                        )
                        if not slot_check.is_available:
                            raise SlotConflictError(
                                'Выбранный пост занят в указанное время.',
                            )

                public_id = await appt_repo.generate_unique_public_id(
                    draft.start_datetime.date(),
                )
                appointment = await appt_repo.create_from_draft(
                    draft=draft,
                    post_id=post_id,
                    master_id=target_master_id,
                    created_by_user_id=creator.id,
                    public_id=public_id,
                )
                appointment.post = post_obj
                appointment.master = target_master

                if self._calendar_service is not None:
                    try:
                        event_id = await self._calendar_service.create_event(
                            appointment=appointment,
                            post=post_obj,
                            master_name=target_master.full_name,
                        )
                        await appt_repo.update_calendar_event_id(
                            appointment_id=appointment.id,
                            event_id=event_id,
                        )
                        appointment.google_calendar_event_id = event_id
                    except CalendarServiceError as exc:
                        raise BookingError(
                            f'Ошибка создания события в Google Календаре: {exc}',
                        ) from exc

                await history_repo.log_action(
                    appointment_id=appointment.id,
                    action_type=HistoryActionType.CREATED,
                    user_id=creator.id,
                    comment=f'Запись создана сотрудником {creator.full_name}',
                )
                return appointment

    async def find_active_by_car(
        self,
        car_query: str,
    ) -> list[Appointment]:
        """Ищет активные записи по марке автомобиля.

        Args:
            car_query: Название марки или модели автомобиля.

        Returns:
            Список найденных активных записей.
        """
        async with get_async_session(self._session_factory) as session:
            appt_repo = AppointmentRepository(session)
            return list(await appt_repo.search_active_by_car(car_query))

    async def reschedule_appointment(
        self,
        public_id: str,
        new_start_dt: datetime.datetime,
        new_post_code: PostCode | None,
        user_telegram_id: int,
    ) -> Appointment:
        """Переносит существующую запись на новое время или пост.

        Args:
            public_id: Публичный номер записи.
            new_start_dt: Новые дата и время начала ремонта.
            new_post_code: Новый рабочий пост или None.
            user_telegram_id: Telegram ID сотрудника.

        Returns:
            Обновленная запись на ремонт.

        Raises:
            PermissionDeniedError: Если у пользователя нет прав на изменение.
            SlotConflictError: При занятости целевого слота.
            BookingError: При ошибке валидации данных.
        """
        if new_start_dt.weekday() == 6:
            raise BookingError('Воскресенье — выходной день автосервиса.')

        async with self._booking_lock:
            async with get_async_session(self._session_factory) as session:
                user, appointment = await _fetch_active_user_and_appointment(
                    session=session,
                    user_telegram_id=user_telegram_id,
                    public_id=public_id,
                )
                if not can_manage_appointment(user, appointment):
                    raise PermissionDeniedError(
                        'Недостаточно прав для изменения этой записи.',
                    )

                post_repo = PostRepository(session)
                history_repo = HistoryLogRepository(session)

                new_end_dt = new_start_dt + datetime.timedelta(
                    minutes=appointment.planned_duration_minutes,
                )
                target_post_code = new_post_code or (
                    appointment.post.code
                    if appointment.post
                    else PostCode.NO_POST
                )

                slot_check = await self.check_slot(
                    post_code=target_post_code,
                    start_dt=new_start_dt,
                    end_dt=new_end_dt,
                    exclude_appointment_id=appointment.id,
                )
                if not slot_check.is_available:
                    raise SlotConflictError(
                        'Выбранный пост занят на это время.',
                    )

                new_post_obj: Post | None = None
                if target_post_code != PostCode.NO_POST:
                    new_post_obj = await post_repo.get_by_code(
                        target_post_code,
                    )

                old_time_str = appointment.start_datetime.strftime(
                    '%d.%m %H:%M',
                )
                appointment.start_datetime = new_start_dt
                appointment.end_datetime = new_end_dt
                appointment.post_id = (
                    new_post_obj.id if new_post_obj is not None else None
                )
                appointment.post = new_post_obj
                await session.flush()

                if (
                    self._calendar_service is not None
                    and appointment.google_calendar_event_id
                ):
                    try:
                        master_name = (
                            appointment.master.full_name
                            if (
                                'master' in appointment.__dict__
                                and appointment.master
                            )
                            else None
                        )
                        await self._calendar_service.update_event(
                            event_id=appointment.google_calendar_event_id,
                            appointment=appointment,
                            post=new_post_obj,
                            master_name=master_name,
                        )
                    except CalendarServiceError:
                        pass

                new_time_str = new_start_dt.strftime('%d.%m %H:%M')
                await history_repo.log_action(
                    appointment_id=appointment.id,
                    action_type=HistoryActionType.UPDATED,
                    user_id=user.id,
                    field_name='schedule',
                    old_value=old_time_str,
                    new_value=new_time_str,
                    comment=f'Перенос записи сотрудником {user.full_name}',
                )
                return appointment

    async def mark_no_show(
        self,
        public_id: str,
        user_telegram_id: int,
    ) -> Appointment:
        """Переводит запись в статус «Не приехал» и удаляет событие календаря.

        Args:
            public_id: Публичный номер записи.
            user_telegram_id: Telegram ID сотрудника.

        Returns:
            Запись со статусом NO_SHOW.

        Raises:
            PermissionDeniedError: Если у пользователя нет прав на изменение.
        """
        async with get_async_session(self._session_factory) as session:
            user, appointment = await _fetch_active_user_and_appointment(
                session=session,
                user_telegram_id=user_telegram_id,
                public_id=public_id,
            )
            if not can_manage_appointment(user, appointment):
                raise PermissionDeniedError(
                    'Недостаточно прав для отметки неявки по этой записи.',
                )

            history_repo = HistoryLogRepository(session)
            event_id = appointment.google_calendar_event_id
            post_code = appointment.post.code if appointment.post else None

            appointment.status = AppointmentStatus.NO_SHOW
            await session.flush()

            if self._calendar_service is not None and event_id:
                try:
                    await self._calendar_service.delete_event(
                        event_id=event_id,
                        post_code=post_code,
                    )
                    appointment.google_calendar_event_id = None
                    await session.flush()
                except CalendarServiceError:
                    pass

            await history_repo.log_action(
                appointment_id=appointment.id,
                action_type=HistoryActionType.STATUS_CHANGED,
                user_id=user.id,
                field_name='status',
                old_value='CONFIRMED',
                new_value='NO_SHOW',
                comment='Клиент не явился ко времени записи',
            )
            return appointment

    async def get_day_load_summary(
        self,
        target_date: datetime.date,
    ) -> DayScheduleOverview:
        """Формирует сводку загрузки постов автосервиса за день.

        Args:
            target_date: Календарная дата для построения расписания.

        Returns:
            Сводка расписания по всем постам за день.
        """
        timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
        start_of_day = datetime.datetime.combine(
            target_date,
            datetime.time.min,
            tzinfo=timezone,
        )
        end_of_day = datetime.datetime.combine(
            target_date,
            datetime.time.max,
            tzinfo=timezone,
        )

        async with get_async_session(self._session_factory) as session:
            post_repo = PostRepository(session)
            appt_repo = AppointmentRepository(session)

            active_posts = list(await post_repo.get_all_active())
            day_appointments = list(
                await appt_repo.get_day_schedule(
                    start_of_day=start_of_day,
                    end_of_day=end_of_day,
                ),
            )

            posts_schedule: list[PostScheduleItem] = []
            for post in active_posts:
                post_appts = [
                    appt for appt in day_appointments
                    if appt.post_id == post.id
                ]
                posts_schedule.append(
                    PostScheduleItem(
                        post=post,
                        appointments=post_appts,
                    ),
                )

            return DayScheduleOverview(
                target_date=target_date,
                posts_schedule=posts_schedule,
            )

    async def start_appointment(
        self,
        public_id: str,
        user_telegram_id: int,
    ) -> Appointment:
        """Переводит заявку в статус «В работе».

        Args:
            public_id: Публичный номер записи.
            user_telegram_id: Telegram ID сотрудника.

        Returns:
            Обновленный объект записи.

        Raises:
            PermissionDeniedError: Если у пользователя нет прав на изменение.
        """
        async with get_async_session(self._session_factory) as session:
            user, appointment = await _fetch_active_user_and_appointment(
                session=session,
                user_telegram_id=user_telegram_id,
                public_id=public_id,
            )
            if not can_manage_appointment(user, appointment):
                raise PermissionDeniedError(
                    'Недостаточно прав для взятия в работу этой записи.',
                )

            history_repo = HistoryLogRepository(session)
            appt_repo = AppointmentRepository(session)

            timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
            now_dt = datetime.datetime.now(timezone)
            updated = await appt_repo.start_work(
                appointment_id=appointment.id,
                actual_start=now_dt,
            )
            if updated is None:
                raise EntityNotFoundError('Не удалось обновить запись.')

            await history_repo.log_action(
                appointment_id=updated.id,
                action_type=HistoryActionType.STATUS_CHANGED,
                user_id=user.id,
                field_name='status',
                old_value='CONFIRMED',
                new_value='IN_PROGRESS',
                comment=f'Мастер {user.full_name} принял машину в работу',
            )
            return updated

    async def complete_appointment(
        self,
        public_id: str,
        user_telegram_id: int,
        early_release: bool = False,
        comment: str | None = None,
    ) -> Appointment:
        """Завершает ремонт и синхронизирует календарь.

        Args:
            public_id: Публичный номер записи.
            user_telegram_id: Telegram ID сотрудника.
            early_release: Флаг досрочного освобождения поста.
            comment: Опциональный комментарий мастера.

        Returns:
            Завершенная запись на ремонт.

        Raises:
            PermissionDeniedError: Если у пользователя нет прав на завершение.
        """
        async with get_async_session(self._session_factory) as session:
            user, appointment = await _fetch_active_user_and_appointment(
                session=session,
                user_telegram_id=user_telegram_id,
                public_id=public_id,
            )
            if not can_manage_appointment(user, appointment):
                raise PermissionDeniedError(
                    'Недостаточно прав для завершения этой записи.',
                )

            history_repo = HistoryLogRepository(session)
            appt_repo = AppointmentRepository(session)

            timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
            now_dt = datetime.datetime.now(timezone)
            updated = await appt_repo.complete_work(
                appointment_id=appointment.id,
                actual_end=now_dt,
                early_release=early_release,
            )
            if updated is None:
                raise EntityNotFoundError('Не удалось завершить запись.')

            if comment:
                updated.master_comment = comment
                await session.flush()

            if (
                early_release
                and self._calendar_service is not None
                and updated.google_calendar_event_id
            ):
                try:
                    master_name = (
                        updated.master.full_name
                        if (
                            'master' in updated.__dict__
                            and updated.master
                        )
                        else None
                    )
                    await self._calendar_service.update_event(
                        event_id=updated.google_calendar_event_id,
                        appointment=updated,
                        post=updated.post,
                        master_name=master_name,
                    )
                except CalendarServiceError:
                    pass

            action = (
                HistoryActionType.EARLY_COMPLETED
                if early_release
                else HistoryActionType.STATUS_CHANGED
            )
            await history_repo.log_action(
                appointment_id=updated.id,
                action_type=action,
                user_id=user.id,
                field_name='status',
                old_value='IN_PROGRESS',
                new_value='DONE',
                comment=f'Работы завершены мастером {user.full_name}',
            )
            return updated

    async def cancel_appointment(
        self,
        public_id: str,
        user_telegram_id: int,
        comment: str | None = None,
    ) -> Appointment:
        """Отменяет бронирование записи и удаляет событие из календаря.

        Args:
            public_id: Публичный номер записи.
            user_telegram_id: Telegram ID сотрудника.
            comment: Причина отмены.

        Returns:
            Отмененная запись на ремонт.

        Raises:
            PermissionDeniedError: Если у пользователя нет прав на отмену.
        """
        async with get_async_session(self._session_factory) as session:
            user, appointment = await _fetch_active_user_and_appointment(
                session=session,
                user_telegram_id=user_telegram_id,
                public_id=public_id,
            )
            if not can_manage_appointment(user, appointment):
                raise PermissionDeniedError(
                    'Недостаточно прав для отмены этой записи.',
                )

            history_repo = HistoryLogRepository(session)
            appt_repo = AppointmentRepository(session)

            event_id = appointment.google_calendar_event_id
            post_code = (
                appointment.post.code if appointment.post else None
            )

            updated = await appt_repo.cancel_appointment(
                appointment_id=appointment.id,
                comment=comment,
            )
            if updated is None:
                raise EntityNotFoundError('Не удалось отменить запись.')

            if self._calendar_service is not None and event_id:
                try:
                    await self._calendar_service.delete_event(
                        event_id=event_id,
                        post_code=post_code,
                    )
                    await appt_repo.update_calendar_event_id(
                        appointment_id=updated.id,
                        event_id=None,
                    )
                except CalendarServiceError:
                    pass

            await history_repo.log_action(
                appointment_id=updated.id,
                action_type=HistoryActionType.CANCELLED,
                user_id=user.id,
                field_name='status',
                old_value=str(appointment.status.value),
                new_value='CANCELLED',
                comment=f'Запись отменена сотрудником {user.full_name}',
            )
            return updated

    async def request_transfer(
        self,
        public_id: str,
        sender_telegram_id: int,
        target_master_telegram_id: int,
    ) -> Appointment:
        """Инициирует передачу записи другому мастеру.

        Args:
            public_id: Публичный номер записи.
            sender_telegram_id: Telegram ID текущего мастера.
            target_master_telegram_id: Telegram ID мастера-получателя.

        Returns:
            Запись в статусе ожидания принятия передачи.
        """
        async with get_async_session(self._session_factory) as session:
            sender, appointment = await _fetch_active_user_and_appointment(
                session=session,
                user_telegram_id=sender_telegram_id,
                public_id=public_id,
            )

            user_repo = UserRepository(session)
            history_repo = HistoryLogRepository(session)
            appt_repo = AppointmentRepository(session)

            target_master = await user_repo.get_by_telegram_id(
                target_master_telegram_id,
            )
            if target_master is None or not target_master.is_active:
                raise EntityNotFoundError('Мастер-получатель не найден.')

            if (
                appointment.master_id != sender.id
                and sender.role != 'OWNER'
            ):
                raise PermissionDeniedError(
                    'Мастер может передать только собственную запись.',
                )

            updated = await appt_repo.request_transfer(
                appointment_id=appointment.id,
                target_master_id=target_master.id,
            )
            if updated is None:
                raise EntityNotFoundError('Не удалось передать запись.')

            await history_repo.log_action(
                appointment_id=updated.id,
                action_type=HistoryActionType.TRANSFER_REQUESTED,
                user_id=sender.id,
                comment=(
                    f'Мастер {sender.full_name} предложил передать '
                    f'запись мастеру {target_master.full_name}'
                ),
            )
            return updated

    async def accept_transfer(
        self,
        public_id: str,
        receiver_telegram_id: int,
    ) -> Appointment:
        """Принимает переданную запись.

        Args:
            public_id: Публичный номер записи.
            receiver_telegram_id: Telegram ID принимающего мастера.

        Returns:
            Обновленная запись с новым мастером.
        """
        async with get_async_session(self._session_factory) as session:
            receiver, appointment = await _fetch_active_user_and_appointment(
                session=session,
                user_telegram_id=receiver_telegram_id,
                public_id=public_id,
            )

            history_repo = HistoryLogRepository(session)
            appt_repo = AppointmentRepository(session)

            if appointment.target_master_id != receiver.id:
                raise PermissionDeniedError(
                    'Эту запись предлагали передать другому мастеру.',
                )

            updated = await appt_repo.accept_transfer(
                appointment_id=appointment.id,
            )
            if updated is None:
                raise EntityNotFoundError('Не удалось принять запись.')

            if (
                self._calendar_service is not None
                and updated.google_calendar_event_id
            ):
                try:
                    await self._calendar_service.update_event(
                        event_id=updated.google_calendar_event_id,
                        appointment=updated,
                        post=updated.post,
                        master_name=receiver.full_name,
                    )
                except CalendarServiceError:
                    pass

            await history_repo.log_action(
                appointment_id=updated.id,
                action_type=HistoryActionType.TRANSFER_ACCEPTED,
                user_id=receiver.id,
                comment=(
                    f'Мастер {receiver.full_name} принял переданную запись'
                ),
            )
            return updated

    async def reject_transfer(
        self,
        public_id: str,
        receiver_telegram_id: int,
    ) -> Appointment:
        """Отклоняет передачу записи.

        Args:
            public_id: Публичный номер записи.
            receiver_telegram_id: Telegram ID мастера.

        Returns:
            Запись, возвращенная исходному мастеру.
        """
        async with get_async_session(self._session_factory) as session:
            receiver, appointment = await _fetch_active_user_and_appointment(
                session=session,
                user_telegram_id=receiver_telegram_id,
                public_id=public_id,
            )

            history_repo = HistoryLogRepository(session)
            appt_repo = AppointmentRepository(session)

            if (
                appointment.target_master_id != receiver.id
                and appointment.master_id != receiver.id
            ):
                raise PermissionDeniedError('Доступ запрещен.')

            updated = await appt_repo.reject_transfer(
                appointment_id=appointment.id,
            )
            if updated is None:
                raise EntityNotFoundError('Не удалось отклонить передачу.')

            await history_repo.log_action(
                appointment_id=updated.id,
                action_type=HistoryActionType.TRANSFER_REJECTED,
                user_id=receiver.id,
                comment=(
                    f'Мастер {receiver.full_name} отклонил передачу записи'
                ),
            )
            return updated

    async def clear_all_calendars_and_appointments(
        self,
        user_telegram_id: int,
    ) -> dict[str, int]:
        """Очищает события во всех Google Календарях и отменяет наряды в базе.

        Args:
            user_telegram_id: Telegram ID владельца, запросившего очистку.

        Returns:
            Статистика удаленных событий по каждому календарю.

        Raises:
            PermissionDeniedError: Если пользователь не является владельцем.
            BookingError: При отсутствии подключения к Google Календарю.
        """
        async with self._booking_lock:
            async with get_async_session(self._session_factory) as session:
                user_repo = UserRepository(session)
                user = await user_repo.get_by_telegram_id(user_telegram_id)
                if user is None or user.role != UserRole.OWNER:
                    raise PermissionDeniedError(
                        'Очистка календарей разрешена только владельцу сервиса.',
                    )

                if self._calendar_service is None:
                    raise BookingError(
                        'Интеграция с Google Календарём не подключена.',
                    )

                stats = await self._calendar_service.clear_all_events()

                stmt = (
                    update(Appointment)
                    .where(
                        Appointment.status.in_([
                            AppointmentStatus.CONFIRMED,
                            AppointmentStatus.IN_PROGRESS,
                            AppointmentStatus.WAITING_TRANSFER,
                        ])
                    )
                    .values(
                        status=AppointmentStatus.CANCELLED,
                        google_calendar_event_id=None,
                        master_comment='Массовая очистка календарей владельцем',
                    )
                )
                await session.execute(stmt)
                return stats
