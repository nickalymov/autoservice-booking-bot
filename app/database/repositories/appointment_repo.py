"""Модуль репозитория записей на ремонт автосервиса.

Обеспечивает создание, поиск, проверку пересечений временных интервалов,
управление переходами статусов, передачу записей и досрочное завершение.
"""

from __future__ import annotations

from collections.abc import Sequence
import datetime

from sqlalchemy import Select
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.config import PostCode
from app.database.models.appointment import Appointment
from app.database.models.user import User
from app.schemas.appointment import AppointmentDraft
from app.schemas.appointment import AppointmentStatus

_BLOCKING_STATUSES: tuple[AppointmentStatus, ...] = (
    AppointmentStatus.CONFIRMED,
    AppointmentStatus.IN_PROGRESS,
    AppointmentStatus.WAITING_TRANSFER,
)

_CLOSED_STATUSES: tuple[AppointmentStatus, ...] = (
    AppointmentStatus.DONE,
    AppointmentStatus.CANCELLED,
    AppointmentStatus.NO_SHOW,
)


def _build_detailed_appointment_query() -> Select[tuple[Appointment]]:
    """Формирует базовый запрос выборки записи со всеми связями.

    Returns:
        Объект запроса Select с настроенной жадной загрузкой связей.
    """
    return select(Appointment).options(
        joinedload(Appointment.post),
        joinedload(Appointment.master),
        joinedload(Appointment.created_by),
        joinedload(Appointment.target_master),
    )


class AppointmentRepository:
    """Репозиторий для выполнения операций с таблицей записей на ремонт.

    Attributes:
        _session: Асинхронная сессия SQLAlchemy для выполнения запросов.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Инициализирует репозиторий с заданной сессией базы данных.

        Args:
            session: Асинхронная сессия базы данных.
        """
        self._session = session

    async def generate_unique_public_id(
        self,
        post_code: PostCode | None,
        start_datetime: datetime.datetime,
        master_id: int,
    ) -> str:
        """Генерирует человекочитаемый номер записи вида P1-1909-1530-1.

        Args:
            post_code: Код поста или None.
            start_datetime: Дата и время начала обслуживания.
            master_id: Первичный ключ назначенного мастера.

        Returns:
            Человекочитаемый строковый номер записи.
        """
        post_prefix = (
            post_code.value
            if post_code and post_code != PostCode.NO_POST
            else 'P0'
        )
        date_part = start_datetime.strftime('%d%m')
        time_part = start_datetime.strftime('%H%M')
        base_id = f'{post_prefix}-{date_part}-{time_part}-{master_id}'

        candidate_id = base_id
        suffix = 1
        while (await self.get_by_public_id(candidate_id)) is not None:
            suffix += 1
            candidate_id = f'{base_id}-{suffix}'

        return candidate_id

    async def search_active_by_car(
        self,
        car_query: str,
    ) -> Sequence[Appointment]:
        """Ищет активные записи по подстроке марки или модели автомобиля.

        Args:
            car_query: Подстрока марки или модели.

        Returns:
            Список найденных активных записей.
        """
        pattern = f'%{car_query.strip()}%'
        stmt = (
            _build_detailed_appointment_query()
            .where(
                Appointment.status.in_(_BLOCKING_STATUSES),
                Appointment.car_model.ilike(pattern),
            )
            .order_by(Appointment.start_datetime.asc())
        )
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_all_active_shop_appointments(self) -> Sequence[Appointment]:
        """Возвращает все активные записи цеха для магазина и руководства.

        Returns:
            Последовательность всех актуальных нарядов сервиса.
        """
        stmt = (
            _build_detailed_appointment_query()
            .where(Appointment.status.in_(_BLOCKING_STATUSES))
            .order_by(Appointment.start_datetime.asc())
        )
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_closed_appointments(
        self,
        master_id: int | None = None,
        limit: int = 15,
    ) -> Sequence[Appointment]:
        """Возвращает список последних завершенных и отмененных записей.

        Args:
            master_id: Опциональный идентификатор мастера для фильтрации.
            limit: Количество возвращаемых записей.

        Returns:
            Список закрытых нарядов, отсортированных по убыванию времени.
        """
        stmt = _build_detailed_appointment_query().where(
            Appointment.status.in_(_CLOSED_STATUSES),
        )
        if master_id is not None:
            stmt = stmt.where(Appointment.master_id == master_id)
        stmt = stmt.order_by(Appointment.updated_at.desc()).limit(limit)
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_conflicts(
        self,
        post_id: int,
        start_dt: datetime.datetime,
        end_dt: datetime.datetime,
        exclude_appointment_id: int | None = None,
    ) -> Sequence[Appointment]:
        """Выбирает записи, создающие временную накладку на заданном посту.

        Args:
            post_id: Первичный ключ рабочего поста.
            start_dt: Дата и время начала планируемого интервала.
            end_dt: Дата и время окончания планируемого интервала.
            exclude_appointment_id: ID текущей записи для исключения.

        Returns:
            Список записей, пересекающихся с заданным интервалом.
        """
        stmt = select(Appointment).where(
            Appointment.post_id == post_id,
            Appointment.status.in_(_BLOCKING_STATUSES),
            Appointment.start_datetime < end_dt,
            Appointment.end_datetime > start_dt,
        )
        if exclude_appointment_id is not None:
            stmt = stmt.where(Appointment.id != exclude_appointment_id)
        stmt = stmt.order_by(Appointment.start_datetime)
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_master_conflicts(
        self,
        master_id: int,
        start_dt: datetime.datetime,
        end_dt: datetime.datetime,
        exclude_appointment_id: int | None = None,
    ) -> Sequence[Appointment]:
        """Выбирает записи мастера, создающие накладку в его личном времени.

        Args:
            master_id: Первичный ключ мастера.
            start_dt: Начало интервала.
            end_dt: Окончание интервала.
            exclude_appointment_id: ID текущей записи для исключения.

        Returns:
            Список пересекающихся нарядов того же мастера.
        """
        stmt = (
            _build_detailed_appointment_query()
            .where(
                Appointment.master_id == master_id,
                Appointment.status.in_(_BLOCKING_STATUSES),
                Appointment.start_datetime < end_dt,
                Appointment.end_datetime > start_dt,
            )
        )
        if exclude_appointment_id is not None:
            stmt = stmt.where(Appointment.id != exclude_appointment_id)
        stmt = stmt.order_by(Appointment.start_datetime)
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_by_id(
        self,
        appointment_id: int,
    ) -> Appointment | None:
        """Возвращает запись по первичному ключу с загрузкой связей.

        Args:
            appointment_id: Первичный ключ записи.

        Returns:
            Найденный объект записи или None, если запись отсутствует.
        """
        stmt = _build_detailed_appointment_query().where(
            Appointment.id == appointment_id,
        )
        result = await self._session.scalars(stmt)
        return result.first()

    async def get_by_public_id(
        self,
        public_id: str,
    ) -> Appointment | None:
        """Возвращает запись по публичному идентификатору.

        Args:
            public_id: Публичный строковый номер записи.

        Returns:
            Найденный объект записи или None, если запись отсутствует.
        """
        stmt = _build_detailed_appointment_query().where(
            Appointment.public_id == public_id,
        )
        result = await self._session.scalars(stmt)
        return result.first()

    async def create_from_draft(
        self,
        draft: AppointmentDraft,
        post_id: int | None,
        master_id: int,
        created_by_user_id: int,
        public_id: str,
    ) -> Appointment:
        """Создает новую запись на ремонт на основе данных черновика.

        Args:
            draft: Экземпляр черновика заявки.
            post_id: Первичный ключ поста или None для без поста.
            master_id: Первичный ключ ответственного мастера.
            created_by_user_id: Первичный ключ автора создания.
            public_id: Уникальный публичный номер заявки.

        Returns:
            Созданная сущность записи на ремонт.
        """
        duration = draft.planned_duration_minutes or 30
        appointment = Appointment(
            public_id=public_id,
            status=AppointmentStatus.CONFIRMED,
            source=draft.source,
            start_datetime=draft.start_datetime,
            end_datetime=draft.end_datetime,
            planned_duration_minutes=duration,
            post_id=post_id,
            master_id=master_id,
            created_by_user_id=created_by_user_id,
            car_model=draft.car_model or 'Не указан',
            client_phone=draft.client_phone or 'Не указан',
            client_name=draft.client_name,
            license_plate=draft.license_plate,
            vin=draft.vin,
            work_description=(
                draft.work_description or ', '.join(draft.work_items)
            ),
            work_items=draft.work_items,
            raw_transcription=draft.raw_transcription,
        )
        self._session.add(appointment)
        await self._session.flush()
        return appointment

    async def get_day_schedule(
        self,
        start_of_day: datetime.datetime,
        end_of_day: datetime.datetime,
    ) -> Sequence[Appointment]:
        """Возвращает все активные записи за указанный день.

        Args:
            start_of_day: Начало временного диапазона дня.
            end_of_day: Окончание временного диапазона дня.

        Returns:
            Последовательность активных записей за день.
        """
        stmt = (
            select(Appointment)
            .options(
                joinedload(Appointment.post),
                joinedload(Appointment.master),
            )
            .where(
                Appointment.status.in_(_BLOCKING_STATUSES),
                Appointment.start_datetime < end_of_day,
                Appointment.end_datetime > start_of_day,
            )
            .order_by(Appointment.start_datetime)
        )
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_master_appointments(
        self,
        master_id: int,
        start_of_day: datetime.datetime | None = None,
        end_of_day: datetime.datetime | None = None,
    ) -> Sequence[Appointment]:
        """Возвращает активные записи мастера с фильтрацией.

        Args:
            master_id: Первичный ключ мастера.
            start_of_day: Опциональное начало диапазона дат.
            end_of_day: Опциональное окончание диапазона дат.

        Returns:
            Последовательность записей ответственного мастера.
        """
        stmt = (
            select(Appointment)
            .options(joinedload(Appointment.post))
            .where(
                Appointment.master_id == master_id,
                Appointment.status.in_(_BLOCKING_STATUSES),
            )
        )
        if start_of_day is not None and end_of_day is not None:
            stmt = stmt.where(
                Appointment.start_datetime < end_of_day,
                Appointment.end_datetime > start_of_day,
            )
        stmt = stmt.order_by(Appointment.start_datetime)
        result = await self._session.scalars(stmt)
        return result.all()

    async def start_work(
        self,
        appointment_id: int,
        actual_start: datetime.datetime,
    ) -> Appointment | None:
        """Переводит запись в статус «В работе» с фиксацией времени начала.

        Args:
            appointment_id: Первичный ключ записи.
            actual_start: Фактическое время взятия в работу.

        Returns:
            Обновленная запись или None, если запись отсутствует.
        """
        appointment = await self.get_by_id(appointment_id)
        if appointment is not None:
            appointment.status = AppointmentStatus.IN_PROGRESS
            appointment.actual_start_datetime = actual_start
            await self._session.flush()
        return appointment

    async def complete_work(
        self,
        appointment_id: int,
        actual_end: datetime.datetime,
        early_release: bool = False,
    ) -> Appointment | None:
        """Переводит запись в статус «Готово» с расчетом длительности.

        Args:
            appointment_id: Первичный ключ записи.
            actual_end: Фактическое время завершения работ.
            early_release: Флаг досрочного освобождения слота.

        Returns:
            Обновленная запись или None, если запись отсутствует.
        """
        appointment = await self.get_by_id(appointment_id)
        if appointment is not None:
            appointment.status = AppointmentStatus.DONE
            appointment.actual_end_datetime = actual_end
            if appointment.actual_start_datetime is not None:
                delta = actual_end - appointment.actual_start_datetime
                appointment.actual_duration_minutes = max(
                    1,
                    int(delta.total_seconds() // 60),
                )
            if early_release:
                appointment.end_datetime = actual_end
            await self._session.flush()
        return appointment

    async def cancel_appointment(
        self,
        appointment_id: int,
        comment: str | None = None,
    ) -> Appointment | None:
        """Отменяет бронирование с сохранением причины.

        Args:
            appointment_id: Первичный ключ записи.
            comment: Опциональный комментарий с причиной отмены.

        Returns:
            Обновленная запись или None, если запись не найдена.
        """
        appointment = await self.get_by_id(appointment_id)
        if appointment is not None:
            appointment.status = AppointmentStatus.CANCELLED
            if comment:
                appointment.master_comment = comment
            await self._session.flush()
        return appointment

    async def request_transfer(
        self,
        appointment_id: int,
        target_master_id: int,
    ) -> Appointment | None:
        """Инициирует процесс передачи записи другому мастеру.

        Args:
            appointment_id: Первичный ключ записи.
            target_master_id: Первичный ключ мастера-получателя.

        Returns:
            Обновленная запись или None, если запись не найдена.
        """
        appointment = await self.get_by_id(appointment_id)
        if appointment is not None:
            appointment.status = AppointmentStatus.WAITING_TRANSFER
            appointment.target_master_id = target_master_id
            await self._session.flush()
        return appointment

    async def accept_transfer(
        self,
        appointment_id: int,
    ) -> Appointment | None:
        """Принимает переданную заявку и назначает нового мастера.

        Args:
            appointment_id: Первичный ключ записи.

        Returns:
            Обновленная запись или None, если запись не найдена.
        """
        appointment = await self.get_by_id(appointment_id)
        if (
            appointment is not None
            and appointment.target_master_id is not None
        ):
            appointment.master_id = appointment.target_master_id
            appointment.target_master_id = None
            appointment.status = AppointmentStatus.CONFIRMED
            await self._session.flush()
        return appointment

    async def reject_transfer(
        self,
        appointment_id: int,
    ) -> Appointment | None:
        """Отклоняет передачу заявки и возвращает её исходному мастеру.

        Args:
            appointment_id: Первичный ключ записи.

        Returns:
            Обновленная запись или None, если запись не найдена.
        """
        appointment = await self.get_by_id(appointment_id)
        if appointment is not None:
            appointment.target_master_id = None
            appointment.status = AppointmentStatus.CONFIRMED
            await self._session.flush()
        return appointment

    async def get_upcoming_for_reminders(
        self,
        window_start: datetime.datetime,
        window_end: datetime.datetime,
    ) -> Sequence[Appointment]:
        """Выбирает предстоящие записи для отправки напоминаний мастерам.

        Args:
            window_start: Начало временного интервала для напоминания.
            window_end: Окончание временного интервала для напоминания.

        Returns:
            Список записей, требующих отправки напоминания.
        """
        stmt = (
            select(Appointment)
            .join(Appointment.master)
            .options(
                joinedload(Appointment.post),
                joinedload(Appointment.master),
            )
            .where(
                Appointment.status == AppointmentStatus.CONFIRMED,
                Appointment.start_datetime >= window_start,
                Appointment.start_datetime <= window_end,
                User.reminders_enabled.is_(True),
            )
            .order_by(Appointment.start_datetime)
        )
        result = await self._session.scalars(stmt)
        return result.all()

    async def update_calendar_event_id(
        self,
        appointment_id: int,
        event_id: str | None,
    ) -> Appointment | None:
        """Обновляет внешний ID события Google Календаря для записи.

        Args:
            appointment_id: Первичный ключ записи.
            event_id: Идентификатор созданного события в календаре.

        Returns:
            Обновленная запись или None, если запись не найдена.
        """
        appointment = await self.get_by_id(appointment_id)
        if appointment is not None:
            appointment.google_calendar_event_id = event_id
            await self._session.flush()
        return appointment
