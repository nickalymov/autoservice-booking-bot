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
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import MenuAction
from app.bot.keyboards.inline import StatusAction
from app.bot.keyboards.inline import get_load_summary_kb
from app.bot.keyboards.reply import NEW_BOOKING_HINT_TEXT
from app.config import TIMEZONE_NAME
from app.config import PostCode
from app.core.booking_service import BookingService
from app.core.booking_service import DayScheduleOverview
from app.database.models import Appointment
from app.database.models import User
from app.database.repositories import AppointmentRepository
from app.schemas.appointment import AppointmentStatus

router = Router()

_WORK_DAY_START: datetime.time = datetime.time(9, 0)
_WORK_DAY_END: datetime.time = datetime.time(19, 0)


def _format_post_schedule_line(
    post_name: str,
    appointments: Sequence[Appointment],
) -> str:
    """Формирует строку расписания для одного поста с учетом окон.

    Args:
        post_name: Название рабочего поста.
        appointments: Список записей, назначенных на данный пост.

    Returns:
        Отформатированная строка занятости и свободных окон.
    """
    if not appointments:
        return f'• <b>{post_name}</b>: свободен на весь день'

    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    sorted_appointments = sorted(
        appointments,
        key=operator.attrgetter('start_datetime'),
    )
    segments: list[str] = []
    current_time = _WORK_DAY_START

    for appointment in sorted_appointments:
        start_dt = appointment.start_datetime.astimezone(timezone)
        end_dt = appointment.end_datetime.astimezone(timezone)
        start_time = start_dt.time()
        end_time = end_dt.time()

        if start_time > current_time:
            gap_str = (
                f'{current_time.strftime("%H:%M")}–'
                f'{start_time.strftime("%H:%M")} свободно'
            )
            segments.append(gap_str)

        master_name = (
            appointment.master.full_name
            if appointment.master
            else 'Мастер'
        )
        appointment_str = (
            f'{start_time.strftime("%H:%M")}–{end_time.strftime("%H:%M")} '
            f'{appointment.car_model}, {master_name}'
        )
        segments.append(appointment_str)

        if end_time > current_time:
            current_time = end_time

    if current_time < _WORK_DAY_END:
        segments.append(
            f'{current_time.strftime("%H:%M")}–'
            f'{_WORK_DAY_END.strftime("%H:%M")} свободно',
        )

    return f'• <b>{post_name}</b>: ' + '; '.join(segments)


def _format_day_schedule(overview: DayScheduleOverview) -> str:
    """Формирует текстовый отчет о загрузке сервиса за день по образцу ТЗ.

    Args:
        overview: Сводка расписания за целевую дату.

    Returns:
        Готовое сообщение с расписанием всех постов.
    """
    date_str = overview.target_date.strftime('%d.%m.%Y')
    lines: list[str] = [f'<b>Загрузка на {date_str}:</b>\n']

    for item in overview.posts_schedule:
        lines.append(
            _format_post_schedule_line(
                post_name=item.post.name,
                appointments=item.appointments,
            ),
        )

    return '\n'.join(lines)


def _calculate_free_windows(overview: DayScheduleOverview) -> str:
    """Вычисляет и форматирует свободные окна для физических постов цеха.

    Args:
        overview: Сводка расписания за день.

    Returns:
        Текст со списком доступных временных окон по постам.
    """
    date_str = overview.target_date.strftime('%d.%m.%Y')
    lines: list[str] = [f'<b>Свободные окна на {date_str}:</b>\n']
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)

    for item in overview.posts_schedule:
        if item.post.code == PostCode.NO_POST:
            continue

        if not item.appointments:
            lines.append(
                f'• <b>{item.post.name}</b>: 09:00–19:00 (весь день)',
            )
            continue

        sorted_appointments = sorted(
            item.appointments,
            key=operator.attrgetter('start_datetime'),
        )
        free_gaps: list[str] = []
        current_time = _WORK_DAY_START

        for appointment in sorted_appointments:
            start_dt = appointment.start_datetime.astimezone(timezone)
            end_dt = appointment.end_datetime.astimezone(timezone)
            start_time = start_dt.time()
            end_time = end_dt.time()

            if start_time > current_time:
                free_gaps.append(
                    f'{current_time.strftime("%H:%M")}–'
                    f'{start_time.strftime("%H:%M")}',
                )
            if end_time > current_time:
                current_time = end_time

        if current_time < _WORK_DAY_END:
            free_gaps.append(
                f'{current_time.strftime("%H:%M")}–'
                f'{_WORK_DAY_END.strftime("%H:%M")}',
            )

        gaps_text = (
            ', '.join(free_gaps) if free_gaps else 'нет свободных окон'
        )
        lines.append(f'• <b>{item.post.name}</b>: {gaps_text}')

    return '\n'.join(lines)


def _format_evening_summary(
    today_overview: DayScheduleOverview,
    tomorrow_overview: DayScheduleOverview,
) -> str:
    """Формирует текст вечерней сводки по требованиям раздела 10.9 ТЗ.

    Args:
        today_overview: Загрузка за сегодняшний день.
        tomorrow_overview: Загрузка за завтрашний день.

    Returns:
        Текст вечернего отчета из трех разделов.
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
    lines.append(
        f'\n<b>2. Записей на завтра ({tomorrow_date_str}):</b> '
        f'{tomorrow_count} шт.',
    )

    lines.append('\n<b>3. Свободные окна на завтра:</b>')
    lines.append(_calculate_free_windows(tomorrow_overview))

    return '\n'.join(lines)


def _build_appointment_action_rows(
    appointment: Appointment,
) -> list[list[InlineKeyboardButton]]:
    """Строит полный блок кнопок управления для наряда в списке.

    Args:
        appointment: Заказ-наряд на обслуживание.

    Returns:
        Список строк инлайн-кнопок управления нарядом.
    """
    rows: list[list[InlineKeyboardButton]] = []
    pid = appointment.public_id

    if appointment.status == AppointmentStatus.CONFIRMED:
        rows.append([
            InlineKeyboardButton(
                text=f'▶️ В работу {pid}',
                callback_data=StatusAction(
                    action='start',
                    public_id=pid,
                ).pack(),
            ),
        ])
        rows.append([
            InlineKeyboardButton(
                text='🔄 Перенести',
                callback_data=StatusAction(
                    action='reschedule',
                    public_id=pid,
                ).pack(),
            ),
            InlineKeyboardButton(
                text='👥 Передать',
                callback_data=StatusAction(
                    action='transfer',
                    public_id=pid,
                ).pack(),
            ),
        ])
        rows.append([
            InlineKeyboardButton(
                text='❌ Не приехал',
                callback_data=StatusAction(
                    action='no_show',
                    public_id=pid,
                ).pack(),
            ),
            InlineKeyboardButton(
                text='🗑 Отмена',
                callback_data=StatusAction(
                    action='cancel',
                    public_id=pid,
                ).pack(),
            ),
        ])
    elif appointment.status == AppointmentStatus.IN_PROGRESS:
        rows.append([
            InlineKeyboardButton(
                text=f'🏁 Завершить {pid}',
                callback_data=StatusAction(
                    action='complete',
                    public_id=pid,
                ).pack(),
            ),
            InlineKeyboardButton(
                text='🗑 Отмена',
                callback_data=StatusAction(
                    action='cancel',
                    public_id=pid,
                ).pack(),
            ),
        ])
    return rows


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
            appointment.post.name if appointment.post else 'Без поста'
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

        action_rows = _build_appointment_action_rows(appointment)
        keyboard_buttons.extend(action_rows)

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
            appointment.post.name if appointment.post else 'Без поста'
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

        action_rows = _build_appointment_action_rows(appointment)
        keyboard_buttons.extend(action_rows)

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
) -> None:
    """Отображает актуальную загрузку постов на текущий день.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        booking_service: Сервис бизнес-логики бронирования.
    """
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
) -> None:
    """Отображает запланированную загрузку постов на завтра.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        booking_service: Сервис бизнес-логики бронирования.
    """
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
) -> None:
    """Выводит список свободных окон по постам на текущий день.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        booking_service: Сервис бизнес-логики бронирования.
    """
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    today = datetime.datetime.now(timezone).date()
    overview = await booking_service.get_day_load_summary(today)

    if callback.message:
        await callback.message.edit_text(
            text=_calculate_free_windows(overview),
            reply_markup=get_load_summary_kb(),
        )
    await callback.answer()


@router.callback_query(MenuAction.filter(F.action == 'my_appointments'))
async def handle_my_appointments(
    callback: CallbackQuery,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Отображает список текущих активных записей авторизованного мастера.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        current_user: Авторизованный сотрудник.
        session: Асинхронная сессия базы данных.
    """
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
) -> None:
    """Отправляет подсказку по созданию новой записи по п. 10.9 ТЗ.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
    """
    if callback.message:
        await callback.message.answer(
            text=NEW_BOOKING_HINT_TEXT,
        )
    await callback.answer()


@router.message(Command(commands=['summary', 'evening']))
async def cmd_evening_summary(
    message: Message,
    booking_service: BookingService,
) -> None:
    """Формирует и отправляет вечернюю сводку загрузки по запросу.

    Args:
        message: Входящее сообщение Telegram.
        booking_service: Сервис управления бронированием.
    """
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
