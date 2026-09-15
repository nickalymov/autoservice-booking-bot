"""Модуль обработчиков общих команд и навигации Telegram-бота.

Содержит реализацию команды /start, перехват текстовых кнопок главного меню
быстрого доступа, управление напоминаниями и администрирование пользователей.
"""

import datetime
import zoneinfo

from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.schedule import _calculate_free_windows
from app.bot.handlers.schedule import _format_day_schedule
from app.bot.handlers.schedule import format_my_appointments_view
from app.bot.handlers.schedule import format_shop_appointments_view
from app.bot.keyboards.inline import StaffToggleAction
from app.bot.keyboards.inline import get_load_summary_kb
from app.bot.keyboards.inline import get_staff_management_kb
from app.bot.keyboards.reply import BTN_ALL_BOOKINGS
from app.bot.keyboards.reply import BTN_FREE_SLOTS
from app.bot.keyboards.reply import BTN_MY_BOOKINGS
from app.bot.keyboards.reply import BTN_NEW_BOOKING
from app.bot.keyboards.reply import BTN_REMINDERS_TOGGLE
from app.bot.keyboards.reply import BTN_STAFF_MANAGEMENT
from app.bot.keyboards.reply import BTN_TODAY_LOAD
from app.bot.keyboards.reply import NEW_BOOKING_HINT_TEXT
from app.bot.keyboards.reply import get_main_reply_kb
from app.config import TIMEZONE_NAME
from app.config import UserRole
from app.core.booking_service import BookingError
from app.core.booking_service import BookingService
from app.database.models import User
from app.database.repositories import AppointmentRepository
from app.database.repositories import UserRepository

router = Router()


def _resolve_greeting_name(
    message: Message,
    current_user: User,
) -> str:
    """Определяет обращение по правилу: Имя Фамилия -> @username -> ID.

    Args:
        message: Входящее сообщение Telegram.
        current_user: Авторизованный пользователь из базы данных.

    Returns:
        Строка с отображаемым именем для персонализированного приветствия.
    """
    if message.from_user:
        parts = [message.from_user.first_name, message.from_user.last_name]
        full_name = ' '.join(p for p in parts if p).strip()
        if full_name:
            return full_name
        if message.from_user.username:
            return f'@{message.from_user.username}'
    return str(current_user.telegram_id)


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    current_user: User,
) -> None:
    """Обрабатывает команду /start, отправляет меню и клавиатуру.

    Args:
        message: Объект сообщения Telegram.
        current_user: Объект авторизованного пользователя.
    """
    role_label = (
        'Владелец'
        if current_user.role == UserRole.OWNER
        else 'Продавец'
        if current_user.role == UserRole.SALES
        else 'Мастер'
    )
    greeting_name = _resolve_greeting_name(
        message=message,
        current_user=current_user,
    )
    await message.answer(
        text=(
            f'Привет, <b>{greeting_name}</b> ({role_label})!\n'
            'Бот автосервиса готов к работе.\n'
            'Вы можете надиктовать запись голосовым сообщением, '
            'перенести наряд или выбрать нужный пункт меню.'
        ),
        reply_markup=get_main_reply_kb(current_user.role),
    )
    await message.answer(
        text='Панель оперативной сводки:',
        reply_markup=get_load_summary_kb(),
    )


async def _toggle_reminders_for_user(
    message: Message,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Внутренняя функция переключения статуса напоминаний.

    Args:
        message: Сообщение Telegram для ответа.
        current_user: Текущий авторизованный сотрудник.
        session: Асинхронная сессия базы данных.
    """
    user_repo = UserRepository(session)
    new_state = not current_user.reminders_enabled
    await user_repo.update_reminders(
        telegram_id=current_user.telegram_id,
        enabled=new_state,
    )
    current_user.reminders_enabled = new_state
    state_str = 'включены 🔔' if new_state else 'отключены 🔕'
    await message.answer(
        text=f'Напоминания за 30 минут до ваших записей <b>{state_str}</b>.',
    )


@router.message(Command(commands=['reminders', 'notifications']))
async def cmd_toggle_reminders(
    message: Message,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Переключает статус получения напоминаний за 30 минут по команде.

    Args:
        message: Сообщение Telegram.
        current_user: Текущий пользователь.
        session: Асинхронная сессия базы данных.
    """
    await _toggle_reminders_for_user(
        message=message,
        current_user=current_user,
        session=session,
    )


@router.message(F.text == BTN_REMINDERS_TOGGLE)
async def handle_reminders_button(
    message: Message,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Переключает статус напоминаний по нажатию Reply-кнопки.

    Args:
        message: Сообщение Telegram.
        current_user: Текущий пользователь.
        session: Асинхронная сессия базы данных.
    """
    await _toggle_reminders_for_user(
        message=message,
        current_user=current_user,
        session=session,
    )


async def _render_staff_management_panel(
    message: Message,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Выводит панель управления персоналом с кнопками переключения.

    Args:
        message: Сообщение Telegram.
        current_user: Текущий пользователь.
        session: Асинхронная сессия базы данных.
    """
    if current_user.role != UserRole.OWNER:
        await message.answer('Раздел доступен только владельцу автосервиса.')
        return

    user_repo = UserRepository(session)
    users = await user_repo.get_all_users()

    lines = [
        '<b>Управление сотрудниками автосервиса:</b>\n',
        'Нажмите на имя сотрудника ниже для переключения доступа:\n',
    ]
    for user in users:
        role_label = (
            'Владелец'
            if user.role == UserRole.OWNER
            else 'Продавец'
            if user.role == UserRole.SALES
            else 'Мастер'
        )
        status_label = 'Активен' if user.is_active else 'Отключен'
        rem_label = '🔔' if user.reminders_enabled else '🔕'
        lines.append(
            f'• <b>{user.full_name}</b> ({role_label}) — '
            f'{status_label} {rem_label}\n'
            f'  ID: <code>{user.telegram_id}</code>',
        )

    lines.append(
        '\nДля добавления нового сотрудника используйте:\n'
        '<code>/add_user &lt;id&gt; &lt;Имя&gt; &lt;MECHANIC|SALES|OWNER&gt;</code>',
    )

    await message.answer(
        text='\n'.join(lines),
        reply_markup=get_staff_management_kb(users),
    )


@router.message(Command(commands=['users', 'staff']))
async def cmd_list_users(
    message: Message,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Выводит список пользователей системы для владельца по команде.

    Args:
        message: Сообщение Telegram.
        current_user: Текущий пользователь.
        session: Асинхронная сессия базы данных.
    """
    await _render_staff_management_panel(
        message=message,
        current_user=current_user,
        session=session,
    )


@router.message(F.text == BTN_STAFF_MANAGEMENT)
async def handle_staff_management_button(
    message: Message,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Открывает интерактивную панель сотрудников по Reply-кнопке.

    Args:
        message: Сообщение Telegram.
        current_user: Текущий пользователь.
        session: Асинхронная сессия базы данных.
    """
    await _render_staff_management_panel(
        message=message,
        current_user=current_user,
        session=session,
    )


@router.callback_query(StaffToggleAction.filter())
async def handle_staff_toggle_callback(
    callback: CallbackQuery,
    callback_data: StaffToggleAction,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Переключает статус доступа сотрудника по инлайн-кнопке.

    Args:
        callback: Запрос обратного вызова.
        callback_data: Идентификатор целевого сотрудника.
        current_user: Авторизованный владелец.
        session: Асинхронная сессия базы данных.
    """
    if current_user.role != UserRole.OWNER:
        await callback.answer(
            'Только владелец может менять доступ сотрудников.',
            show_alert=True,
        )
        return

    user_repo = UserRepository(session)
    target_user = await user_repo.get_by_id(callback_data.user_id)
    if target_user is None:
        await callback.answer('Сотрудник не найден.', show_alert=True)
        return

    if target_user.telegram_id == current_user.telegram_id:
        await callback.answer(
            'Нельзя заблокировать собственный аккаунт владельца.',
            show_alert=True,
        )
        return

    target_user.is_active = not target_user.is_active
    await session.commit()

    users = await user_repo.get_all_users()
    if callback.message:
        await callback.message.edit_reply_markup(
            reply_markup=get_staff_management_kb(users),
        )

    state_word = 'активирован' if target_user.is_active else 'заблокирован'
    await callback.answer(
        f'Доступ сотрудника {target_user.full_name} {state_word}.',
    )


@router.message(Command(commands=['clear_calendars', 'purge_calendars']))
async def cmd_clear_calendars(
    message: Message,
    current_user: User,
    booking_service: BookingService,
) -> None:
    """Очищает события во всех Google Календарях сервиса (для владельца).

    Args:
        message: Сообщение Telegram.
        current_user: Авторизованный сотрудник.
        booking_service: Сервис управления бронированием.
    """
    if current_user.role != UserRole.OWNER:
        await message.answer('Команда доступна только владельцу автосервиса.')
        return

    await message.answer('Начинаю полную очистку Google Календарей...')
    try:
        stats = await booking_service.clear_all_calendars_and_appointments(
            user_telegram_id=current_user.telegram_id,
        )
        report_lines = ['<b>Очистка календарей завершена успешно:</b>\n']
        for cal_name, count in stats.items():
            report_lines.append(f'• {cal_name}: удалено {count} событий')
        report_lines.append('\nСвязанные наряды в базе данных сброшены.')
        await message.answer(text='\n'.join(report_lines))
    except BookingError as exc:
        await message.answer(f'Ошибка при очистке календарей: <code>{exc}</code>')


@router.message(Command(commands=['add_user']))
async def cmd_add_user(
    message: Message,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Добавляет нового сотрудника в систему владельцем сервиса.

    Args:
        message: Сообщение с аргументами команды.
        current_user: Текущий пользователь.
        session: Асинхронная сессия базы данных.
    """
    if current_user.role != UserRole.OWNER:
        await message.answer('Команда доступна только владельцу сервиса.')
        return

    if not message.text:
        return

    parts = message.text.strip().split(maxsplit=3)
    if len(parts) < 4:
        await message.answer(
            '<b>Формат команды:</b>\n'
            '<code>/add_user &lt;telegram_id&gt; &lt;Имя&gt; &lt;РОЛЬ&gt;</code>\n\n'
            '<b>Примеры:</b>\n'
            '<code>/add_user 123456789 Вова MECHANIC</code>\n'
            '<code>/add_user 987654321 Иван SALES</code>\n'
            'Роли: MECHANIC (мастер), SALES (магазин), OWNER (владелец)',
        )
        return

    _, raw_tg_id, full_name, raw_role = parts
    try:
        tg_id = int(raw_tg_id)
    except ValueError:
        await message.answer('Telegram ID должен быть числом.')
        return

    role_upper = raw_role.upper()
    if role_upper not in UserRole.__members__:
        await message.answer(
            'Недопустимая роль. Доступны: MECHANIC, SALES, OWNER.',
        )
        return

    target_role = UserRole(role_upper)
    user_repo = UserRepository(session)
    user = await user_repo.upsert_user(
        telegram_id=tg_id,
        full_name=full_name,
        role=target_role,
    )
    await session.commit()

    role_ru = (
        'Мастер'
        if target_role == UserRole.MECHANIC
        else 'Продавец'
        if target_role == UserRole.SALES
        else 'Владелец'
    )
    await message.answer(
        f'Сотрудник <b>{user.full_name}</b> (ID: <code>{user.telegram_id}</code>) '
        f'успешно сохранен с ролью <b>{role_ru}</b>.',
    )


@router.message(Command(commands=['toggle_user']))
async def cmd_toggle_user(
    message: Message,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Включает или отключает доступ сотрудника в системе.

    Args:
        message: Сообщение с аргументами команды.
        current_user: Текущий пользователь.
        session: Асинхронная сессия базы данных.
    """
    if current_user.role != UserRole.OWNER:
        await message.answer('Команда доступна только владельцу сервиса.')
        return

    if not message.text:
        return

    parts = message.text.strip().split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            '<b>Формат:</b> <code>/toggle_user &lt;telegram_id&gt;</code>',
        )
        return

    try:
        tg_id = int(parts[1])
    except ValueError:
        await message.answer('Telegram ID должен быть числом.')
        return

    user_repo = UserRepository(session)
    updated = await user_repo.toggle_active(tg_id)
    if updated is None:
        await message.answer('Сотрудник с таким Telegram ID не найден.')
        return

    await session.commit()
    status_str = 'активирован' if updated.is_active else 'заблокирован'
    await message.answer(
        f'Доступ сотрудника <b>{updated.full_name}</b> теперь <b>{status_str}</b>.',
    )


@router.message(F.text == BTN_NEW_BOOKING)
async def handle_new_booking_button(
    message: Message,
    current_user: User,
) -> None:
    """Отправляет мастеру шаблон-подсказку для новой записи по ТЗ.

    Args:
        message: Сообщение с нажатой кнопкой меню.
        current_user: Текущий пользователь.
    """
    await message.answer(
        text=NEW_BOOKING_HINT_TEXT,
        reply_markup=get_main_reply_kb(current_user.role),
    )


@router.message(F.text == BTN_TODAY_LOAD)
async def handle_today_button(
    message: Message,
    booking_service: BookingService,
) -> None:
    """Выводит актуальную загрузку постов на сегодня по нажатию кнопки.

    Args:
        message: Сообщение Telegram.
        booking_service: Сервис бизнес-логики бронирования.
    """
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    today = datetime.datetime.now(timezone).date()
    overview = await booking_service.get_day_load_summary(today)
    await message.answer(
        text=_format_day_schedule(overview),
        reply_markup=get_load_summary_kb(),
    )


@router.message(F.text == BTN_FREE_SLOTS)
async def handle_free_slots_button(
    message: Message,
    booking_service: BookingService,
) -> None:
    """Выводит список свободных окон по постам на сегодня.

    Args:
        message: Сообщение Telegram.
        booking_service: Сервис бизнес-логики бронирования.
    """
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    today = datetime.datetime.now(timezone).date()
    overview = await booking_service.get_day_load_summary(today)
    await message.answer(
        text=_calculate_free_windows(overview),
        reply_markup=get_load_summary_kb(),
    )


@router.message(F.text == BTN_MY_BOOKINGS)
async def handle_my_bookings_button(
    message: Message,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Отображает список активных записей мастера по нажатию Reply-кнопки.

    Args:
        message: Сообщение Telegram.
        current_user: Авторизованный сотрудник.
        session: Асинхронная сессия базы данных.
    """
    appt_repo = AppointmentRepository(session)
    appointments = await appt_repo.get_master_appointments(
        master_id=current_user.id,
    )
    text, reply_markup = format_my_appointments_view(appointments)
    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )


@router.message(F.text == BTN_ALL_BOOKINGS)
async def handle_all_bookings_button(
    message: Message,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Отображает все активные наряды цеха для магазина и владельца.

    Args:
        message: Сообщение Telegram.
        current_user: Авторизованный сотрудник.
        session: Асинхронная сессия базы данных.
    """
    if current_user.role not in (UserRole.SALES, UserRole.OWNER):
        await message.answer('Раздел доступен только магазину и руководству.')
        return

    appt_repo = AppointmentRepository(session)
    appointments = await appt_repo.get_all_active_shop_appointments()
    text, reply_markup = format_shop_appointments_view(appointments)
    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )
