"""Модуль обработчиков расписания и загрузки автосервиса.

Обеспечивает вывод сводок занятости постов на сегодня и завтра,
расчет свободных временных окон, просмотр персональных записей мастера
и формирование вечерней сводки по цеху.
"""

from __future__ import annotations

from collections.abc import Sequence
import datetime
import operator
import zoneinfo

from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import MenuAction
from app.bot.keyboards.inline import get_appointment_actions_kb
from app.bot.keyboards.inline import get_load_summary_kb
from app.bot.keyboards.reply import NEW_BOOKING_HINT_TEXT
from app.config import POST_NAMES
from app.config import PostCode
from app.config import TIMEZONE_NAME
from app.config import WORK_DAY_END_HOUR
from app.config import WORK_DAY_START_HOUR
from app.core.booking_service import BookingService
from app.core.booking_service import DayScheduleOverview
from app.core.booking_service import UpcomingSlot
from app.database.models import Appointment
from app.database.models import User
from app.database.repositories import AppointmentRepository
from app.schemas.appointment import AppointmentStatus

router = Router()

_WORK_DAY_START: datetime.time = datetime.time(WORK_DAY_START_HOUR, 0)
_WORK_DAY_END: datetime.time = datetime.time(WORK_DAY_END_HOUR, 0)

_RUSSIAN_WEEKDAY_NAMES: tuple[str, ...] = (
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье',
)


def _get_time_of_day_emoji(time_obj: datetime.time) -> str:
    """Возвращает эмодзи времени суток по времени начала интервала.

    Args:
        time_obj: Время начала интервала.

    Returns:
        Символ эмодзи времени суток.
    """
    hour = time_obj.hour
    if 6 <= hour < 12:
        return '🌅'
    if 12 <= hour < 16:
        return '☀️'
    if 16 <= hour < 23:
        return '🌙'
    return '🛌'


def _format_post_schedule_block(
    post_code: PostCode,
    post_name: str,
    appointments: Sequence[Appointment],
) -> str:
    """Формирует структурированный блок расписания для поста по BR-003.

    Args:
        post_code: Системный код поста.
        post_name: Название рабочего поста.
        appointments: Список записей на пост.

    Returns:
        Многострочный блок расписания с переносами и эмодзи.
    """
    post_title = POST_NAMES.get(post_code, post_name)
    if not appointments:
        return f'• <b>{post_title}</b>:\n  🌅 🟢 09:00–20:00 свободно'

    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    sorted_appointments = sorted(
        appointments,
        key=operator.attrgetter('start_datetime'),
    )

    lines: list[str] = [f'• <b>{post_title}</b>:']
    current_time = _WORK_DAY_START

    for appointment in sorted_appointments:
        start_dt = appointment.start_datetime.astimezone(timezone)
        end_dt = appointment.end_datetime.astimezone(timezone)
        start_time = start_dt.time()
        end_time = end_dt.time()

        if start_time > current_time:
            emoji = _get_time_of_day_emoji(current_time)
            gap_str = (
                f'  {emoji} 🟢 {current_time.strftime("%H:%M")}–'
                f'{start_time.strftime("%H:%M")} свободно'
            )
            lines.append(gap_str)

        master_name = (
            appointment.master.full_name
            if appointment.master
            else 'Мастер'
        )
        occ_emoji = _get_time_of_day_emoji(start_time)
        appointment_str = (
            f'  {occ_emoji} ❌ {start_time.strftime("%H:%M")}–{end_time.strftime("%H:%M")} '
            f'{appointment.car_model}, {master_name}'
        )
        lines.append(appointment_str)

        if end_time > current_time:
            current_time = end_time

    if current_time < _WORK_DAY_END:
        end_emoji = _get_time_of_day_emoji(current_time)
        lines.append(
            f'  {end_emoji} 🟢 {current_time.strftime("%H:%M")}–'
            f'{_WORK_DAY_END.strftime("%H:%M")} свободно'
        )

    return '\n'.join(lines)


def _format_day_schedule(overview: DayScheduleOverview) -> str:
    """Формирует текстовый отчет о загрузке сервиса за день по образцу BR-003.

    Args:
        overview: Сводка расписания за целевую дату.

    Returns:
        Готовое сообщение с расписанием всех постов с пустой строкой между ними.
    """
    date_str = overview.target_date.strftime('%d.%m.%Y')
    weekday_str = _RUSSIAN_WEEKDAY_NAMES[overview.target_date.weekday()]
    header = f'<b>Загрузка на {date_str} ({weekday_str}):</b>\n'

    post_blocks: list[str] = []
    for item in overview.posts_schedule:
        post_blocks.append(
            _format_post_schedule_block(
                post_code=item.post.code,
                post_name=item.post.name,
                appointments=item.appointments,
            )
        )

    return header + '\n\n'.join(post_blocks)


def format_today_schedule_view(overview: DayScheduleOverview) -> str:
    """Формирует строковое представление расписания на день.

    Args:
        overview: Сводка расписания за день.

    Returns:
        Текстовый отчет о загрузке.
    """
    return _format_day_schedule(overview)


def format_nearest_free_slots_view(
    slots: Sequence[UpcomingSlot],
) -> str:
    """Формирует отчет о ближайших свободных окнах по постам вперед по BR-004.

    Args:
        slots: Список доступных будущих окон.

    Returns:
        Текст с группировкой по датам и дням недели.
    """
    if not slots:
        return 'Ближайших свободных окон на ближайшие дни не найдено.'

    lines: list[str] = ['<b>Ближайшие доступные окна для записи:</b>\n']
    current_date: datetime.date | None = None

    for slot in slots:
        if slot.target_date != current_date:
            current_date = slot.target_date
            weekday_name = _RUSSIAN_WEEKDAY_NAMES[current_date.weekday()]
            date_header = (
                f'📅 <b>{current_date.strftime("%d.%m.%Y")} ({weekday_name})</b>:'
            )
            lines.append(f'\n{date_header}')

        time_emoji = _get_time_of_day_emoji(slot.start_time)
        lines.append(
            f'  {time_emoji} 🟢 {slot.post_name}: '
            f'{slot.start_time.strftime("%H:%M")}–{slot.end_time.strftime("%H:%M")}'
        )

    return '\n'.join(lines)


def _format_evening_summary(
    today_overview: DayScheduleOverview,
    tomorrow_overview: DayScheduleOverview,
) -> str:
    """Формирует текст вечерней сводки по требованиям BR-014.

    Args:
        today_overview: Загрузка за сегодняшний день.
        tomorrow_overview: Загрузка за завтрашний день.

    Returns:
        Текст вечернего отчета из трех разделов с дробными строками.
    """
    lines: list[str] = ['<b>Вечерняя сводка автосервиса</b>\n']

    unclosed_appointments: list[Appointment] = []
    for item in today_overview.posts_schedule:
        for appointment in item.appointments:
            if appointment.status in (
                AppointmentStatus.CONFIRMED,
                AppointmentStatus.IN_PROGRESS,
            ):
                unclosed_appointments.append(appointment)

    lines.append('<b>1. Незакрытые записи на сегодня:</b>')
    if unclosed_appointments:
        for appointment in unclosed_appointments:
            status_ru = (
                'В работе'
                if appointment.status == AppointmentStatus.IN_PROGRESS
                else 'Ожидает'
            )
            master_name = (
                appointment.master.full_name
                if appointment.master
                else 'Мастер'
            )
            lines.append(
                f'• [{appointment.public_id}] {appointment.car_model} '
                f'— {master_name} ({status_ru})',
            )
    else:
        lines.append('Все запланированные работы сегодня завершены.')

    tomorrow_count = sum(
        len(item.appointments)
        for item in tomorrow_overview.posts_schedule
    )
    tomorrow_date_str = tomorrow_overview.target_date.strftime('%d.%m')
    tomorrow_weekday_str = _RUSSIAN_WEEKDAY_NAMES[
        tomorrow_overview.target_date.weekday()
    ]
    lines.append(
        f'\n<b>2. Записей на завтра ({tomorrow_date_str}, {tomorrow_weekday_str}):</b> '
        f'{tomorrow_count} шт.',
    )

    lines.append('\n<b>3. Свободные окна на завтра:</b>')
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)

    for item in tomorrow_overview.posts_schedule:
        if item.post.code == PostCode.NO_POST:
            continue

        post_title = POST_NAMES.get(item.post.code, item.post.name)
        lines.append(f'• <b>{post_title}</b>:')

        if not item.appointments:
            lines.append('  🌅 🟢 09:00–20:00 (весь день)')
            continue

        sorted_appointments = sorted(
            item.appointments,
            key=operator.attrgetter('start_datetime'),
        )
        current_time = _WORK_DAY_START
        gaps_found = False

        for appointment in sorted_appointments:
            start_dt = appointment.start_datetime.astimezone(timezone)
            end_dt = appointment.end_datetime.astimezone(timezone)
            start_time = start_dt.time()
            end_time = end_dt.time()

            if start_time > current_time:
                time_emoji = _get_time_of_day_emoji(current_time)
                lines.append(
                    f'  {time_emoji} 🟢 {current_time.strftime("%H:%M")}–'
                    f'{start_time.strftime("%H:%M")} свободно'
                )
                gaps_found = True

            if end_time > current_time:
                current_time = end_time

        if current_time < _WORK_DAY_END:
            time_emoji = _get_time_of_day_emoji(current_time)
            lines.append(
                f'  {time_emoji} 🟢 {current_time.strftime("%H:%M")}–'
                f'{_WORK_DAY_END.strftime("%H:%M")} свободно'
            )
            gaps_found = True

        if not gaps_found:
            lines.append('  ❌ нет свободных окон')

    return '\n'.join(lines)


def format_shop_appointments_view(
    appointments: Sequence[Appointment],
) -> tuple[str, InlineKeyboardMarkup]:
    """Формирует обзор всех нарядов автосервиса для магазина и руководства.

    Args:
        appointments: Список всех актуальных записей сервиса.

    Returns:
        Текст со списком нарядов и инлайн-клавиатура действий.
    """
    if not appointments:
        return (
            'В цехе сейчас нет активных записей на обслуживание.',
            get_load_summary_kb(),
        )

    lines: list[str] = ['<b>Все активные записи автосервиса:</b>\n']
    keyboard_buttons: list[list[InlineKeyboardButton]] = []
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)

    for appointment in appointments:
        post_label = (
            POST_NAMES.get(appointment.post.code, appointment.post.name)
            if appointment.post
            else 'Без поста'
        )
        master_label = (
            appointment.master.full_name if appointment.master else 'Мастер'
        )
        start_dt = appointment.start_datetime.astimezone(timezone)
        end_dt = appointment.end_datetime.astimezone(timezone)
        time_str = (
            f'{start_dt.strftime("%d.%m %H:%M")}–{end_dt.strftime("%H:%M")}'
        )
        status_label = (
            'В работе'
            if appointment.status == AppointmentStatus.IN_PROGRESS
            else 'Ожидает'
        )

        lines.append(
            f'• <b>[{appointment.public_id}]</b> {appointment.car_model}\n'
            f'  Мастер: {master_label} | Пост: {post_label}\n'
            f'  Время: {time_str} ({status_label})\n'
            f'  Работы: {appointment.work_description}',
        )

        action_kb = get_appointment_actions_kb(
            public_id=appointment.public_id,
            status=appointment.status,
            car_model=appointment.car_model,
        )
        keyboard_buttons.extend(action_kb.inline_keyboard)

    keyboard_buttons.append([
        InlineKeyboardButton(
            text='« Назад в меню',
            callback_data=MenuAction(action='today').pack(),
        ),
    ])

    return (
        '\n\n'.join(lines),
        InlineKeyboardMarkup(inline_keyboard=keyboard_buttons),
    )


def format_my_appointments_view(
    appointments: Sequence[Appointment],
) -> tuple[str, InlineKeyboardMarkup]:
    """Формирует текст и клавиатуру для просмотра активных записей мастера.

    Args:
        appointments: Последовательность активных записей мастера.

    Returns:
        Кортеж из отформатированного текста и инлайн-клавиатуры.
    """
    if not appointments:
        return (
            'У вас пока нет активных записей на ремонт.',
            get_load_summary_kb(),
        )

    lines: list[str] = ['<b>Ваши активные записи:</b>\n']
    keyboard_buttons: list[list[InlineKeyboardButton]] = []
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)

    for appointment in appointments:
        post_label = (
            POST_NAMES.get(appointment.post.code, appointment.post.name)
            if appointment.post
            else 'Без поста'
        )
        start_dt = appointment.start_datetime.astimezone(timezone)
        end_dt = appointment.end_datetime.astimezone(timezone)
        time_str = (
            f'{start_dt.strftime("%d.%m %H:%M")}–'
            f'{end_dt.strftime("%H:%M")}'
        )
        status_label = (
            'В работе'
            if appointment.status == AppointmentStatus.IN_PROGRESS
            else 'Ожидает'
        )

        lines.append(
            f'• <b>[{appointment.public_id}]</b> {appointment.car_model}\n'
            f'  Пост: {post_label} | Время: {time_str} ({status_label})\n'
            f'  Работы: {appointment.work_description}',
        )

        action_kb = get_appointment_actions_kb(
            public_id=appointment.public_id,
            status=appointment.status,
            car_model=appointment.car_model,
        )
        keyboard_buttons.extend(action_kb.inline_keyboard)

    keyboard_buttons.append([
        InlineKeyboardButton(
            text='« Назад в меню',
            callback_data=MenuAction(action='today').pack(),
        ),
    ])

    return (
        '\n\n'.join(lines),
        InlineKeyboardMarkup(inline_keyboard=keyboard_buttons),
    )


@router.callback_query(MenuAction.filter(F.action == 'today'))
async def handle_today_schedule(
    callback: CallbackQuery,
    booking_service: BookingService,
    state: FSMContext,
) -> None:
    """Отображает актуальную загрузку постов на текущий день со сбросом FSM.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        booking_service: Сервис бизнес-логики бронирования.
        state: Контекст FSM.
    """
    await state.clear()
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    today = datetime.datetime.now(timezone).date()
    overview = await booking_service.get_day_load_summary(today)

    if callback.message:
        await callback.message.edit_text(
            text=_format_day_schedule(overview),
            reply_markup=get_load_summary_kb(),
        )
    await callback.answer()


@router.callback_query(MenuAction.filter(F.action == 'tomorrow'))
async def handle_tomorrow_schedule(
    callback: CallbackQuery,
    booking_service: BookingService,
    state: FSMContext,
) -> None:
    """Отображает запланированную загрузку постов на завтра со сбросом FSM.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        booking_service: Сервис бизнес-логики бронирования.
        state: Контекст FSM.
    """
    await state.clear()
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    tomorrow = datetime.datetime.now(timezone).date() + datetime.timedelta(
        days=1,
    )
    overview = await booking_service.get_day_load_summary(tomorrow)

    if callback.message:
        await callback.message.edit_text(
            text=_format_day_schedule(overview),
            reply_markup=get_load_summary_kb(),
        )
    await callback.answer()


@router.callback_query(MenuAction.filter(F.action == 'free_slots'))
async def handle_free_slots(
    callback: CallbackQuery,
    booking_service: BookingService,
    state: FSMContext,
) -> None:
    """Выводит список ближайших доступных окон по постам вперед по BR-004.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        booking_service: Сервис бизнес-логики бронирования.
        state: Контекст FSM.
    """
    await state.clear()
    slots = await booking_service.get_nearest_free_slots(duration_minutes=30)

    if callback.message:
        await callback.message.edit_text(
            text=format_nearest_free_slots_view(slots),
            reply_markup=get_load_summary_kb(),
        )
    await callback.answer()


@router.callback_query(MenuAction.filter(F.action == 'my_appointments'))
async def handle_my_appointments(
    callback: CallbackQuery,
    current_user: User,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    """Отображает список текущих активных записей авторизованного мастера.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        current_user: Авторизованный сотрудник.
        session: Асинхронная сессия базы данных.
        state: Контекст FSM.
    """
    await state.clear()
    appt_repo = AppointmentRepository(session)
    appointments = await appt_repo.get_master_appointments(
        master_id=current_user.id,
    )
    text, reply_markup = format_my_appointments_view(appointments)

    if callback.message:
        await callback.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )
    await callback.answer()


@router.callback_query(MenuAction.filter(F.action == 'create_booking'))
async def handle_create_booking_menu(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    """Отправляет подсказку по созданию новой записи с очисткой FSM.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        state: Контекст FSM.
    """
    await state.clear()
    if callback.message:
        await callback.message.answer(
            text=NEW_BOOKING_HINT_TEXT,
        )
    await callback.answer()


@router.message(Command(commands=['summary', 'evening']))
async def cmd_evening_summary(
    message: Message,
    booking_service: BookingService,
    state: FSMContext,
) -> None:
    """Формирует и отправляет вечернюю сводку загрузки по BR-014.

    Args:
        message: Входящее сообщение Telegram.
        booking_service: Сервис управления бронированием.
        state: Контекст FSM.
    """
    await state.clear()
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    now_dt = datetime.datetime.now(timezone)
    today = now_dt.date()
    tomorrow = today + datetime.timedelta(days=1)

    today_overview = await booking_service.get_day_load_summary(today)
    tomorrow_overview = await booking_service.get_day_load_summary(tomorrow)

    await message.answer(
        text=_format_evening_summary(today_overview, tomorrow_overview),
        reply_markup=get_load_summary_kb(),
    )
