"""Модуль обработчиков управления существующими записями автосервиса.

Обеспечивает перевод заявок в статус «В работе», завершение с возможностью
досрочного освобождения поста, двухэтапную передачу записей между мастерами,
фиксацию неявки клиента (NO_SHOW) и подтверждение изменений записи.
"""

from __future__ import annotations

import datetime
import zoneinfo

from aiogram import Bot
from aiogram import F
from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.booking import extract_message_text
from app.bot.keyboards.inline import RescheduleConfirmAction
from app.bot.keyboards.inline import SelectCarAction
from app.bot.keyboards.inline import StatusAction
from app.bot.keyboards.inline import TransferAction
from app.bot.keyboards.inline import get_appointment_actions_kb
from app.bot.keyboards.inline import get_mechanic_selector_kb
from app.bot.keyboards.inline import get_reschedule_confirm_kb
from app.bot.states.booking_states import BookingState
from app.config import POST_NAMES
from app.config import TIMEZONE_NAME
from app.config import PostCode
from app.core.booking_service import BookingError
from app.core.booking_service import BookingService
from app.database.models.appointment import Appointment
from app.database.models.user import User
from app.database.repositories.appointment_repo import AppointmentRepository
from app.database.repositories.user_repo import UserRepository
from app.schemas.appointment import AppointmentStatus
from app.services.ai_service import AIService
from app.services.ai_service import AIServiceError

router = Router()


class EarlyReleaseAction(CallbackData, prefix='rel'):
    """Фабрика обратного вызова для решения о досрочном освобождении поста."""

    release: bool
    public_id: str


class TransferDecisionAction(CallbackData, prefix='trdec'):
    """Фабрика обратного вызова для принятия или отклонения передачи."""

    decision: str
    public_id: str


def get_early_release_kb(
    public_id: str,
    planned_end_str: str,
) -> InlineKeyboardMarkup:
    """Создает клавиатуру выбора досрочного освобождения поста.

    Args:
        public_id: Публичный идентификатор заявки.
        planned_end_str: Время планового окончания в строковом формате.

    Returns:
        Клавиатура с вариантами освобождения слота.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да, освободить',
                callback_data=EarlyReleaseAction(
                    release=True,
                    public_id=public_id,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'Нет, оставить до {planned_end_str}',
                callback_data=EarlyReleaseAction(
                    release=False,
                    public_id=public_id,
                ).pack(),
            ),
        ],
    ])


def _get_transfer_decision_kb(public_id: str) -> InlineKeyboardMarkup:
    """Создает клавиатуру для подтверждения или отказа от переданной заявки.

    Args:
        public_id: Публичный номер записи.

    Returns:
        Клавиатура решения мастера-получателя.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Принять',
                callback_data=TransferDecisionAction(
                    decision='accept',
                    public_id=public_id,
                ).pack(),
            ),
            InlineKeyboardButton(
                text='Отклонить',
                callback_data=TransferDecisionAction(
                    decision='reject',
                    public_id=public_id,
                ).pack(),
            ),
        ],
    ])


def format_reschedule_card_text(
    appointment: Appointment,
    new_start_dt: datetime.datetime,
    new_post_code: PostCode,
) -> str:
    """Формирует симметричный блок Было / Будет с кодами постов по BR-013.

    Args:
        appointment: Текущая запись на ремонт.
        new_start_dt: Новые дата и время начала ремонта.
        new_post_code: Новый рабочий пост.

    Returns:
        Отформатированный HTML-текст блока сравнения.
    """
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    old_start_msk = appointment.start_datetime.astimezone(timezone)
    old_end_msk = appointment.end_datetime.astimezone(timezone)
    old_post_code = (
        appointment.post.code if appointment.post else PostCode.NO_POST
    )
    old_post_label = POST_NAMES.get(old_post_code, str(old_post_code))
    old_line = (
        f'{old_start_msk.strftime("%d.%m, %H:%M")}–'
        f'{old_end_msk.strftime("%H:%M")}, {old_post_label}'
    )

    new_end_dt = new_start_dt + datetime.timedelta(
        minutes=appointment.planned_duration_minutes,
    )
    new_post_label = POST_NAMES.get(new_post_code, str(new_post_code))
    new_line = (
        f'{new_start_dt.strftime("%d.%m, %H:%M")}–'
        f'{new_end_dt.strftime("%H:%M")}, {new_post_label}'
    )

    return (
        '<b>Изменение записи</b>\n'
        f'<b>Было:</b> {old_line}\n'
        f'<b>Будет:</b> {new_line}\n\n'
        'Подтвердить изменение?'
    )


async def show_reschedule_preview(
    message: Message,
    state: FSMContext,
    appointment: Appointment,
    new_start_dt: datetime.datetime,
    new_post_code: PostCode,
) -> None:
    """Сохраняет параметры переноса в FSM и выводит карточку сравнения.

    Args:
        message: Входящее сообщение Telegram для ответа.
        state: Контекст конечного автомата FSM.
        appointment: Объект текущей записи.
        new_start_dt: Новые дата и время начала обслуживания.
        new_post_code: Новый назначенный пост.
    """
    await state.set_data({
        'reschedule_public_id': appointment.public_id,
        'reschedule_start_dt': new_start_dt.isoformat(),
        'reschedule_post_code': new_post_code.value,
    })
    await state.set_state(BookingState.waiting_for_confirmation)

    compare_text = format_reschedule_card_text(
        appointment=appointment,
        new_start_dt=new_start_dt,
        new_post_code=new_post_code,
    )
    await message.answer(
        text=compare_text,
        reply_markup=get_reschedule_confirm_kb(
            public_id=appointment.public_id,
        ),
    )


@router.callback_query(SelectCarAction.filter())
async def handle_multiple_car_selection(
    callback: CallbackQuery,
    callback_data: SelectCarAction,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """Обрабатывает выбор конкретного автомобиля при совпадениях.

    Args:
        callback: Запрос обратного вызова Telegram.
        callback_data: Данные действия и публичный номер выбранной машины.
        state: Контекст FSM.
        session: Асинхронная сессия базы данных.
    """
    appt_repo = AppointmentRepository(session)
    appointment = await appt_repo.get_by_public_id(callback_data.public_id)

    if appointment is None:
        await callback.answer('Запись не найдена.', show_alert=True)
        return

    if callback.message:
        await callback.message.edit_text(
            text=f'Выбран наряд <b>{appointment.public_id}</b> ({appointment.car_model}).',
        )

    if callback_data.action == 'complete':
        from app.bot.handlers.voice import prompt_early_release_for_appointment

        if callback.message:
            await prompt_early_release_for_appointment(
                message=callback.message,
                appointment=appointment,
            )
    elif callback_data.action == 'reschedule':
        await state.set_data({
            'reschedule_public_id': appointment.public_id,
        })
        await state.set_state(BookingState.waiting_for_reschedule_edit)
        if callback.message:
            await callback.message.answer(
                text=(
                    f'На какое время перенести запись <b>{appointment.public_id}</b>?\n'
                    'Напишите или надиктуйте голосом (Шаг записи — 30 минут):'
                ),
            )
    await callback.answer()


@router.callback_query(StatusAction.filter(F.action == 'reschedule'))
async def handle_button_reschedule_click(
    callback: CallbackQuery,
    callback_data: StatusAction,
    state: FSMContext,
    booking_service: BookingService,
    session: AsyncSession,
) -> None:
    """Инициирует перенос с показом контекста наряда и окон по BR-013.

    Args:
        callback: Запрос обратного вызова Telegram.
        callback_data: Данные действия с публичным номером.
        state: Контекст конечного автомата FSM.
        booking_service: Сервис бронирования.
        session: Асинхронная сессия базы данных.
    """
    appt_repo = AppointmentRepository(session)
    appointment = await appt_repo.get_by_public_id(callback_data.public_id)
    if appointment is None:
        await callback.answer('Запись не найдена.', show_alert=True)
        return

    await state.set_data({
        'reschedule_public_id': callback_data.public_id,
    })
    await state.set_state(BookingState.waiting_for_reschedule_edit)

    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    start_str = appointment.start_datetime.astimezone(timezone).strftime('%d.%m %H:%M')
    end_str = appointment.end_datetime.astimezone(timezone).strftime('%H:%M')
    post_label = (
        POST_NAMES.get(appointment.post.code, appointment.post.name)
        if appointment.post
        else 'Без поста'
    )

    nearest_slots = await booking_service.get_nearest_free_slots(
        duration_minutes=appointment.planned_duration_minutes,
        days_ahead=3,
    )
    slots_preview: list[str] = []
    for slot in nearest_slots[:4]:
        slots_preview.append(
            f'• {slot.target_date.strftime("%d.%m")} '
            f'{slot.start_time.strftime("%H:%M")}–{slot.end_time.strftime("%H:%M")} '
            f'({slot.post_name})'
        )

    slots_text = (
        '\n'.join(slots_preview)
        if slots_preview
        else 'Свободные окна не найдены.'
    )

    prompt_text = (
        f'На какое время или пост перенести запись <b>{appointment.public_id} — {appointment.car_model}</b>?\n'
        f'Пост: {post_label} | Время: {start_str}–{end_str}\n\n'
        f'<b>Ближайшие свободные окна:</b>\n{slots_text}\n\n'
        'Напишите время (например: <i>«на завтра на 15:00 на подъемник 1»</i>) '
        'или напишите: <i>«на ближайшее свободное окно»</i>:'
    )

    if callback.message:
        await callback.message.answer(text=prompt_text)
    await callback.answer()


@router.callback_query(RescheduleConfirmAction.filter(F.action == 'confirm'))
async def handle_confirm_reschedule(
    callback: CallbackQuery,
    callback_data: RescheduleConfirmAction,
    state: FSMContext,
    current_user: User,
    booking_service: BookingService,
) -> None:
    """Подтверждает изменение даты, времени или поста существующей записи.

    Args:
        callback: Запрос обратного вызова Telegram.
        callback_data: Данные действия.
        state: Контекст FSM с новыми параметрами.
        current_user: Авторизованный сотрудник.
        booking_service: Сервис управления бронированием.
    """
    data = await state.get_data()
    iso_start = data.get('reschedule_start_dt')
    raw_post_code = data.get('reschedule_post_code')

    if not iso_start or not raw_post_code:
        await callback.answer('Параметры переноса устарели.', show_alert=True)
        return

    new_start_dt = datetime.datetime.fromisoformat(iso_start)
    new_post_code = PostCode(raw_post_code)

    try:
        updated = await booking_service.reschedule_appointment(
            public_id=callback_data.public_id,
            new_start_dt=new_start_dt,
            new_post_code=new_post_code,
            user_telegram_id=current_user.telegram_id,
            allow_sunday=True,
            allow_overtime=True,
        )
        if callback.message:
            await callback.message.edit_text(
                text=(
                    f'Запись <b>[{updated.public_id}] ({updated.car_model})</b> успешно перенесена.\n'
                    f'Новое время: '
                    f'{updated.start_datetime.strftime("%d.%m.%Y, %H:%M")}'
                ),
            )
        await state.clear()
        await callback.answer('Изменение подтверждено.')
    except BookingError as exc:
        await callback.answer(str(exc), show_alert=True)


@router.callback_query(RescheduleConfirmAction.filter(F.action == 'edit_more'))
async def handle_reschedule_edit_more(
    callback: CallbackQuery,
    callback_data: RescheduleConfirmAction,
    state: FSMContext,
) -> None:
    """Переводит в режим ожидания правок при переносе наряда по п. 10.4 ТЗ.

    Args:
        callback: Запрос обратного вызова Telegram.
        callback_data: Данные действия с публичным номером.
        state: Контекст FSM.
    """
    await state.set_state(BookingState.waiting_for_reschedule_edit)
    if callback.message:
        await callback.message.answer(
            text=(
                f'Напишите или надиктуйте голосом изменения для записи '
                f'<b>{callback_data.public_id}</b> (например: '
                '<i>«Перенеси на 15:00 на второй подъемник»</i>):'
            ),
        )
    await callback.answer()


@router.callback_query(RescheduleConfirmAction.filter(F.action == 'cancel'))
async def handle_cancel_reschedule(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    """Отменяет операцию переноса записи.

    Args:
        callback: Запрос обратного вызова Telegram.
        state: Контекст FSM.
    """
    await state.clear()
    if callback.message:
        await callback.message.edit_text(text='Перенос записи отменен.')
    await callback.answer('Отменено.')


@router.message(
    BookingState.waiting_for_reschedule_edit,
    F.text | F.voice,
)
async def process_reschedule_edit_input(
    message: Message,
    bot: Bot,
    state: FSMContext,
    ai_service: AIService,
    booking_service: BookingService,
    session: AsyncSession,
) -> None:
    """Обрабатывает ввод нового времени/поста или запрос на ближайшее окно по BR-013.

    Args:
        message: Сообщение мастера с уточнениями.
        bot: Клиент Telegram Bot API.
        state: Контекст FSM.
        ai_service: Сервис искусственного интеллекта.
        booking_service: Сервис бронирования.
        session: Асинхронная сессия базы данных.
    """
    raw_text = await extract_message_text(
        message=message,
        bot=bot,
        ai_service=ai_service,
    )
    if not raw_text:
        await message.answer('Не удалось распознать сообщение для переноса.')
        return

    data = await state.get_data()
    public_id = data.get('reschedule_public_id')
    if not public_id:
        await message.answer('Сессия переноса устарела.')
        await state.clear()
        return

    appt_repo = AppointmentRepository(session)
    appointment = await appt_repo.get_by_public_id(public_id)
    if appointment is None:
        await message.answer('Запись не найдена в базе данных.')
        await state.clear()
        return

    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    low_text = raw_text.lower()

    if 'ближайш' in low_text or 'окно' in low_text or 'свободн' in low_text:
        nearest_slots = await booking_service.get_nearest_free_slots(
            duration_minutes=appointment.planned_duration_minutes,
            days_ahead=5,
        )
        if not nearest_slots:
            await message.answer('Ближайших свободных окон на будущее не найдено.')
            return

        slot = nearest_slots[0]
        new_start_dt = datetime.datetime.combine(
            slot.target_date,
            slot.start_time,
            tzinfo=timezone,
        )
        new_post_code = slot.post_code
        await show_reschedule_preview(
            message=message,
            state=state,
            appointment=appointment,
            new_start_dt=new_start_dt,
            new_post_code=new_post_code,
        )
        return

    try:
        extraction = await ai_service.extract_appointment(raw_text=raw_text)
    except AIServiceError:
        await message.answer('Не удалось извлечь новое время или пост.')
        return

    current_date_str = appointment.start_datetime.astimezone(
        timezone,
    ).strftime('%Y-%m-%d')
    target_date = extraction.reschedule_new_date or extraction.start_date or current_date_str
    target_time = extraction.reschedule_new_time or extraction.start_time

    if not target_time:
        await message.answer('Укажите время для переноса (например: 14:00):')
        return

    try:
        new_start_dt = datetime.datetime.strptime(
            f'{target_date} {target_time}',
            '%Y-%m-%d %H:%M',
        ).replace(tzinfo=timezone)
    except ValueError:
        await message.answer('Некорректный формат времени.')
        return

    now_dt = datetime.datetime.now(timezone)
    if new_start_dt < now_dt:
        await message.answer(
            f'Указанное время ({new_start_dt.strftime("%d.%m.%Y %H:%M")}) '
            f'уже прошло. Текущее время: {now_dt.strftime("%H:%M")}.'
        )
        return

    new_post_code = extraction.reschedule_new_post or (
        appointment.post.code if appointment.post else PostCode.NO_POST
    )

    await show_reschedule_preview(
        message=message,
        state=state,
        appointment=appointment,
        new_start_dt=new_start_dt,
        new_post_code=new_post_code,
    )


@router.callback_query(StatusAction.filter(F.action == 'start'))
async def handle_start_work(
    callback: CallbackQuery,
    callback_data: StatusAction,
    current_user: User,
    booking_service: BookingService,
) -> None:
    """Переводит запись в работу и фиксирует фактическое время начала.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        callback_data: Данные действия со статусом.
        current_user: Авторизованный сотрудник.
        booking_service: Сервис бизнес-логики управления ремонтом.
    """
    try:
        updated = await booking_service.start_appointment(
            public_id=callback_data.public_id,
            user_telegram_id=current_user.telegram_id,
        )
        if callback.message:
            await callback.message.edit_text(
                text=(
                    f'Запись <b>[{updated.public_id}] ({updated.car_model})</b> переведена в работу.\n'
                    f'Мастер: {current_user.full_name}'
                ),
                reply_markup=get_appointment_actions_kb(
                    public_id=updated.public_id,
                    status=AppointmentStatus.IN_PROGRESS,
                    car_model=updated.car_model,
                ),
            )
        await callback.answer('Машина принята в работу.')
    except BookingError as exc:
        await callback.answer(str(exc), show_alert=True)


@router.callback_query(StatusAction.filter(F.action == 'no_show'))
async def handle_no_show_work(
    callback: CallbackQuery,
    callback_data: StatusAction,
    current_user: User,
    booking_service: BookingService,
) -> None:
    """Переводит запись в статус «Не приехал» по требованию раздела 10.8 ТЗ.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        callback_data: Данные действия со статусом.
        current_user: Авторизованный сотрудник.
        booking_service: Сервис управления бронированием.
    """
    try:
        updated = await booking_service.mark_no_show(
            public_id=callback_data.public_id,
            user_telegram_id=current_user.telegram_id,
        )
        if callback.message:
            await callback.message.edit_text(
                text=(
                    f'Запись <b>[{updated.public_id}] ({updated.car_model})</b> отмечена как '
                    '«Не приехал». Пост освобожден.'
                ),
            )
        await callback.answer('Зафиксирована неявка клиента.')
    except BookingError as exc:
        await callback.answer(str(exc), show_alert=True)


@router.callback_query(StatusAction.filter(F.action == 'complete'))
async def handle_complete_work(
    callback: CallbackQuery,
    callback_data: StatusAction,
    current_user: User,
    booking_service: BookingService,
    session: AsyncSession,
) -> None:
    """Инициирует завершение ремонта и проверяет необходимость досрочного релиза.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        callback_data: Данные действия со статусом.
        current_user: Авторизованный сотрудник.
        booking_service: Сервис бизнес-логики управления ремонтом.
        session: Асинхронная сессия базы данных.
    """
    appt_repo = AppointmentRepository(session)
    appointment = await appt_repo.get_by_public_id(callback_data.public_id)

    if appointment is None:
        await callback.answer('Запись не найдена.', show_alert=True)
        return

    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    now_dt = datetime.datetime.now(timezone)
    appointment_end_msk = appointment.end_datetime.astimezone(timezone)

    if now_dt < appointment_end_msk:
        post_label = (
            POST_NAMES.get(appointment.post.code, appointment.post.name)
            if appointment.post
            else 'пост'
        )
        planned_end_str = appointment_end_msk.strftime('%H:%M')
        actual_time_str = now_dt.strftime('%H:%M')

        if callback.message:
            await callback.message.edit_text(
                text=(
                    f'Запись была запланирована до {planned_end_str}.\n'
                    f'Освободить {post_label} с {actual_time_str}?'
                ),
                reply_markup=get_early_release_kb(
                    public_id=appointment.public_id,
                    planned_end_str=planned_end_str,
                ),
            )
        await callback.answer()
        return

    try:
        await booking_service.complete_appointment(
            public_id=appointment.public_id,
            user_telegram_id=current_user.telegram_id,
            early_release=False,
        )
        if callback.message:
            await callback.message.edit_text(
                text=f'Заказ-наряд <b>[{appointment.public_id}] ({appointment.car_model})</b> завершен.',
            )
        await callback.answer('Работы успешно завершены.')
    except BookingError as exc:
        await callback.answer(str(exc), show_alert=True)


@router.callback_query(EarlyReleaseAction.filter())
async def handle_early_release_decision(
    callback: CallbackQuery,
    callback_data: EarlyReleaseAction,
    current_user: User,
    booking_service: BookingService,
) -> None:
    """Применяет решение мастера о досрочном освобождении рабочего поста.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        callback_data: Решение мастера по освобождению слота.
        current_user: Авторизованный сотрудник.
        booking_service: Сервис бизнес-логики управления ремонтом.
    """
    try:
        updated = await booking_service.complete_appointment(
            public_id=callback_data.public_id,
            user_telegram_id=current_user.telegram_id,
            early_release=callback_data.release,
        )
        status_msg = (
            'Запись завершена, пост досрочно освобожден.'
            if callback_data.release
            else 'Запись завершена, пост сохранен забронированным.'
        )
        if callback.message:
            await callback.message.edit_text(
                text=(
                    f'Заказ-наряд <b>[{updated.public_id}] ({updated.car_model})</b> закрыт.\n'
                    f'{status_msg}'
                ),
            )
        await callback.answer(status_msg)
    except BookingError as exc:
        await callback.answer(str(exc), show_alert=True)


@router.callback_query(StatusAction.filter(F.action == 'transfer'))
async def handle_initiate_transfer(
    callback: CallbackQuery,
    callback_data: StatusAction,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Отображает список доступных мастеров для передачи заявки.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        callback_data: Данные действия со статусом.
        current_user: Авторизованный сотрудник.
        session: Асинхронная сессия базы данных.
    """
    user_repo = UserRepository(session)
    mechanics = await user_repo.get_active_mechanics(
        exclude_telegram_id=current_user.telegram_id,
    )

    if not mechanics:
        await callback.answer(
            'Нет других доступных мастеров для передачи.',
            show_alert=True,
        )
        return

    if callback.message:
        await callback.message.edit_text(
            text='Выберите мастера, которому хотите передать запись:',
            reply_markup=get_mechanic_selector_kb(
                mechanics=mechanics,
                public_id=callback_data.public_id,
            ),
        )
    await callback.answer()


@router.callback_query(TransferAction.filter())
async def handle_send_transfer(
    callback: CallbackQuery,
    callback_data: TransferAction,
    current_user: User,
    booking_service: BookingService,
    session: AsyncSession,
    bot: Bot,
) -> None:
    """Направляет целевому мастеру предложение принять запись.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        callback_data: Выбранный мастер для передачи.
        current_user: Инициатор передачи.
        booking_service: Сервис управления бронированием.
        session: Асинхронная сессия базы данных.
        bot: Клиент Telegram API для отправки уведомления.
    """
    user_repo = UserRepository(session)
    target_master = await user_repo.get_by_id(callback_data.master_id)

    if target_master is None:
        await callback.answer('Мастер не найден.', show_alert=True)
        return

    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)

    try:
        updated = await booking_service.request_transfer(
            public_id=callback_data.public_id,
            sender_telegram_id=current_user.telegram_id,
            target_master_telegram_id=target_master.telegram_id,
        )

        start_msk = updated.start_datetime.astimezone(timezone)
        end_msk = updated.end_datetime.astimezone(timezone)
        time_str = (
            f'{start_msk.strftime("%d.%m, %H:%M")}–'
            f'{end_msk.strftime("%H:%M")}'
        )
        post_str = (
            POST_NAMES.get(updated.post.code, updated.post.name)
            if updated.post
            else 'Без поста'
        )

        offer_text = (
            f'<b>{current_user.full_name}</b> предлагает передать вам запись:\n'
            f'<b>Номер:</b> [{updated.public_id}]\n'
            f'<b>Время:</b> {time_str}\n'
            f'<b>Пост:</b> {post_str}\n'
            f'<b>Автомобиль:</b> {updated.car_model}\n'
            f'<b>Работы:</b> {updated.work_description}\n\n'
            'Принять запись?'
        )

        await bot.send_message(
            chat_id=target_master.telegram_id,
            text=offer_text,
            reply_markup=_get_transfer_decision_kb(
                public_id=updated.public_id,
            ),
        )

        if callback.message:
            await callback.message.edit_text(
                text=(
                    f'Запрос на передачу записи <b>[{updated.public_id}] ({updated.car_model})</b> '
                    f'отправлен мастеру {target_master.full_name}.'
                ),
            )
        await callback.answer('Запрос отправлен коллеге.')
    except BookingError as exc:
        await callback.answer(str(exc), show_alert=True)


@router.callback_query(TransferDecisionAction.filter())
async def handle_transfer_decision(
    callback: CallbackQuery,
    callback_data: TransferDecisionAction,
    current_user: User,
    booking_service: BookingService,
    session: AsyncSession,
    bot: Bot,
) -> None:
    """Обрабатывает решение мастера-получателя о принятии или отказе от заявки.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        callback_data: Принятое решение (accept или reject).
        current_user: Принимающий мастер.
        booking_service: Сервис управления бронированием.
        session: Асинхронная сессия базы данных.
        bot: Клиент Telegram API для отправки уведомлений.
    """
    appt_repo = AppointmentRepository(session)
    appointment = await appt_repo.get_by_public_id(callback_data.public_id)

    if appointment is None:
        await callback.answer('Запись не найдена.', show_alert=True)
        return

    original_master_tg_id = (
        appointment.master.telegram_id if appointment.master else None
    )

    try:
        if callback_data.decision == 'accept':
            updated = await booking_service.accept_transfer(
                public_id=callback_data.public_id,
                receiver_telegram_id=current_user.telegram_id,
            )
            if callback.message:
                await callback.message.edit_text(
                    text=(
                        f'Вы приняли запись <b>[{updated.public_id}] ({updated.car_model})</b>.'
                    ),
                    reply_markup=get_appointment_actions_kb(
                        public_id=updated.public_id,
                        status=updated.status,
                        car_model=updated.car_model,
                    ),
                )
            if original_master_tg_id:
                await bot.send_message(
                    chat_id=original_master_tg_id,
                    text=(
                        f'Мастер {current_user.full_name} принял '
                        f'запись <b>[{updated.public_id}] ({updated.car_model})</b>.'
                    ),
                )
            await callback.answer('Запись успешно принята.')
        else:
            updated = await booking_service.reject_transfer(
                public_id=callback_data.public_id,
                receiver_telegram_id=current_user.telegram_id,
            )
            if callback.message:
                await callback.message.edit_text(
                    text=(
                        f'Вы отклонили передачу записи '
                        f'<b>[{updated.public_id}] ({updated.car_model})</b>.'
                    ),
                )
            if original_master_tg_id:
                await bot.send_message(
                    chat_id=original_master_tg_id,
                    text=(
                        f'Мастер {current_user.full_name} отклонил '
                        f'передачу записи <b>[{updated.public_id}] ({updated.car_model})</b>.'
                    ),
                )
            await callback.answer('Передача отклонена.')
    except BookingError as exc:
        await callback.answer(str(exc), show_alert=True)


@router.callback_query(StatusAction.filter(F.action == 'cancel'))
async def handle_cancel_appointment(
    callback: CallbackQuery,
    callback_data: StatusAction,
    current_user: User,
    booking_service: BookingService,
) -> None:
    """Отменяет бронь записи по запросу сотрудника.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        callback_data: Данные действия со статусом.
        current_user: Сотрудник, запросивший отмену.
        booking_service: Сервис управления бронированием.
    """
    try:
        updated = await booking_service.cancel_appointment(
            public_id=callback_data.public_id,
            user_telegram_id=current_user.telegram_id,
        )
        if callback.message:
            await callback.message.edit_text(
                text=(
                    f'Запись <b>[{updated.public_id}] ({updated.car_model})</b> отменена.\n'
                    'Слот поста освобожден.'
                ),
            )
        await callback.answer('Запись отменена.')
    except BookingError as exc:
        await callback.answer(str(exc), show_alert=True)
