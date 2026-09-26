"""Модуль обработчиков общих команд и навигации Telegram-бота.

Содержит реализацию команды /start, перехват текстовых кнопок главного меню
быстрого доступа, управление напоминаниями и администрирование пользователей.
"""

from __future__ import annotations

import datetime
import zoneinfo

from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.schedule import format_my_appointments_view
from app.bot.handlers.schedule import format_nearest_free_slots_view
from app.bot.handlers.schedule import format_shop_appointments_view
from app.bot.handlers.schedule import format_today_schedule_view
from app.bot.keyboards.inline import ClosedApptAction
from app.bot.keyboards.inline import NewUserRoleAction
from app.bot.keyboards.inline import StaffAction
from app.bot.keyboards.inline import StaffRoleAction
from app.bot.keyboards.inline import get_closed_appointments_kb
from app.bot.keyboards.inline import get_delete_confirm_kb
from app.bot.keyboards.inline import get_load_summary_kb
from app.bot.keyboards.inline import get_new_user_role_selector_kb
from app.bot.keyboards.inline import get_role_selector_kb
from app.bot.keyboards.inline import get_staff_list_kb
from app.bot.keyboards.inline import get_user_card_kb
from app.bot.keyboards.reply import BTN_ALL_BOOKINGS
from app.bot.keyboards.reply import BTN_CLOSED_BOOKINGS
from app.bot.keyboards.reply import BTN_FREE_SLOTS
from app.bot.keyboards.reply import BTN_MY_BOOKINGS
from app.bot.keyboards.reply import BTN_NEW_BOOKING
from app.bot.keyboards.reply import BTN_REMINDERS_TOGGLE
from app.bot.keyboards.reply import BTN_STAFF_MANAGEMENT
from app.bot.keyboards.reply import BTN_TODAY_LOAD
from app.bot.keyboards.reply import NEW_BOOKING_HINT_TEXT
from app.bot.keyboards.reply import get_main_reply_kb
from app.bot.states.booking_states import BookingState
from app.config import POST_NAMES
from app.config import TIMEZONE_NAME
from app.config import UserRole
from app.core.booking_service import BookingError
from app.core.booking_service import BookingService
from app.core.booking_service import PermissionDeniedError
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
        full_name = ' '.join(part for part in parts if part).strip()
        if full_name:
            return full_name
        if message.from_user.username:
            return f'@{message.from_user.username}'
    return str(current_user.telegram_id)


def _format_user_card_text(
    target_user: User,
    current_user: User,
) -> str:
    """Формирует текст карточки профиля сотрудника.

    Args:
        target_user: Целевой сотрудник.
        current_user: Текущий авторизованный пользователь.

    Returns:
        Отформатированный HTML-текст карточки профиля.
    """
    is_self = target_user.telegram_id == current_user.telegram_id
    status_label = '🟢 Активен' if target_user.is_active else '🔴 Заблокирован'
    role_label = (
        'Мастер (MECHANIC)'
        if target_user.role == UserRole.MECHANIC
        else 'Продавец (SALES)'
        if target_user.role == UserRole.SALES
        else 'Владелец (OWNER)'
    )
    rem_label = 'Включены' if target_user.reminders_enabled else 'Отключены'

    card_text = (
        f'<b>Профиль сотрудника:</b> {target_user.full_name}\n\n'
        f'• <b>Роль:</b> {role_label}\n'
        f'• <b>Статус:</b> {status_label}\n'
        f'• <b>Напоминания (30 мин):</b> {rem_label}\n'
        f'• <b>Telegram ID:</b> <code>{target_user.telegram_id}</code>\n'
    )
    if is_self:
        card_text += '\n<i>(Это ваш собственный аккаунт)</i>'

    return card_text


async def _get_target_user_or_deny(
    callback: CallbackQuery,
    current_user: User,
    session: AsyncSession,
    user_id: int,
) -> User | None:
    """Проверяет права владельца и возвращает пользователя или отклоняет вызов.

    Args:
        callback: Запрос обратного вызова Telegram.
        current_user: Текущий авторизованный пользователь.
        session: Асинхронная сессия базы данных.
        user_id: Идентификатор целевого сотрудника.

    Returns:
        Объект целевого пользователя или None в случае отказа в доступе.
    """
    if current_user.role != UserRole.OWNER:
        await callback.answer('Доступ запрещен.', show_alert=True)
        return None

    user_repo = UserRepository(session)
    target_user = await user_repo.get_by_id(user_id)
    if target_user is None:
        await callback.answer('Сотрудник не найден.', show_alert=True)
        return None

    return target_user


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    current_user: User,
    state: FSMContext,
) -> None:
    """Обрабатывает команду /start, сбрасывает зависший контекст и шлет меню.

    Args:
        message: Объект сообщения Telegram.
        current_user: Объект авторизованного пользователя.
        state: Контекст FSM для гарантированной очистки.
    """
    await state.clear()
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
    state_str = 'Включены 🔔' if new_state else 'Отключены 🔕'
    await message.answer(
        text=f'Напоминания за 30 минут до ваших записей <b>{state_str}</b>.',
    )


@router.message(Command(commands=['reminders', 'notifications']))
async def cmd_toggle_reminders(
    message: Message,
    current_user: User,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    """Переключает статус получения напоминаний за 30 минут по команде.

    Args:
        message: Сообщение Telegram.
        current_user: Текущий пользователь.
        session: Асинхронная сессия базы данных.
        state: Контекст FSM.
    """
    await state.clear()
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
    state: FSMContext,
) -> None:
    """Переключает статус напоминаний по нажатию Reply-кнопки.

    Args:
        message: Сообщение Telegram.
        current_user: Текущий пользователь.
        session: Асинхронная сессия базы данных.
        state: Контекст FSM.
    """
    await state.clear()
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
    """Выводит интерактивный список сотрудников сервиса для владельца.

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

    header_text = (
        '<b>Управление командой автосервиса</b>\n\n'
        'Выберите сотрудника из списка ниже для просмотра профиля, '
        'изменения роли, блокировки или удаления:\n'
        'Либо нажмите <b>«Добавить сотрудника»</b> для регистрации нового мастера.'
    )
    await message.answer(
        text=header_text,
        reply_markup=get_staff_list_kb(users),
    )


@router.message(Command(commands=['users', 'staff']))
async def cmd_list_users(
    message: Message,
    current_user: User,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    """Выводит список пользователей системы для владельца по команде.

    Args:
        message: Сообщение Telegram.
        current_user: Текущий пользователь.
        session: Асинхронная сессия базы данных.
        state: Контекст FSM.
    """
    await state.clear()
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
    state: FSMContext,
) -> None:
    """Открывает интерактивную панель сотрудников по Reply-кнопке.

    Args:
        message: Сообщение Telegram.
        current_user: Текущий пользователь.
        session: Асинхронная сессия базы данных.
        state: Контекст FSM.
    """
    await state.clear()
    await _render_staff_management_panel(
        message=message,
        current_user=current_user,
        session=session,
    )


@router.callback_query(StaffAction.filter(F.action == 'add_start'))
async def handle_staff_add_start(
    callback: CallbackQuery,
    current_user: User,
    state: FSMContext,
) -> None:
    """Запускает процесс добавления нового сотрудника через FSM.

    Args:
        callback: Запрос обратного вызова.
        current_user: Авторизованный владелец.
        state: Контекст FSM.
    """
    if current_user.role != UserRole.OWNER:
        await callback.answer('Доступ запрещен.', show_alert=True)
        return

    await state.set_state(BookingState.waiting_for_new_user_id)
    if callback.message:
        await callback.message.answer(
            '<b>Добавление нового сотрудника</b>\n\n'
            'Введите числовой <b>Telegram ID</b> сотрудника '
            '(его можно узнать, переслав сообщение в бота @userinfobot):',
        )
    await callback.answer()


@router.message(BookingState.waiting_for_new_user_id, F.text)
async def process_new_user_id_input(
    message: Message,
    state: FSMContext,
) -> None:
    """Принимает Telegram ID создаваемого сотрудника.

    Args:
        message: Сообщение с числовым ID.
        state: Контекст FSM.
    """
    if not message.text:
        return

    raw_id = message.text.strip().lstrip('@')
    try:
        tg_id = int(raw_id)
    except ValueError:
        await message.answer(
            'Telegram ID должен состоять только из цифр. Попробуйте еще раз:',
        )
        return

    await state.update_data({'new_user_tg_id': tg_id})
    await state.set_state(BookingState.waiting_for_new_user_name)
    await message.answer(
        'Отлично. Теперь введите <b>Имя и Фамилию</b> сотрудника '
        '(например: <i>Вова</i> или <i>Иван Иванов</i>):',
    )


@router.message(BookingState.waiting_for_new_user_name, F.text)
async def process_new_user_name_input(
    message: Message,
    state: FSMContext,
) -> None:
    """Принимает имя создаваемого сотрудника и запрашивает выбор роли.

    Args:
        message: Сообщение с именем сотрудника.
        state: Контекст FSM.
    """
    if not message.text:
        return

    full_name = message.text.strip()
    await state.update_data({'new_user_name': full_name})

    await message.answer(
        text=f'Выберите системную роль для сотрудника <b>{full_name}</b>:',
        reply_markup=get_new_user_role_selector_kb(),
    )


@router.callback_query(NewUserRoleAction.filter())
async def handle_new_user_role_chosen(
    callback: CallbackQuery,
    callback_data: NewUserRoleAction,
    current_user: User,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """Завершает регистрацию нового сотрудника с выбранной ролью.

    Args:
        callback: Запрос обратного вызова.
        callback_data: Выбранная роль.
        current_user: Владелец сервиса.
        state: Контекст FSM с данными ID и имени.
        session: Асинхронная сессия базы данных.
    """
    if current_user.role != UserRole.OWNER:
        await callback.answer('Доступ запрещен.', show_alert=True)
        return

    data = await state.get_data()
    tg_id = data.get('new_user_tg_id')
    full_name = data.get('new_user_name')

    if not tg_id or not full_name:
        await callback.answer('Данные устарели. Начните заново.', show_alert=True)
        await state.clear()
        return

    role = UserRole(callback_data.role)
    user_repo = UserRepository(session)
    user = await user_repo.upsert_user(
        telegram_id=tg_id,
        full_name=full_name,
        role=role,
    )
    await session.commit()
    await state.clear()

    role_ru = (
        'Мастер'
        if role == UserRole.MECHANIC
        else 'Продавец'
        if role == UserRole.SALES
        else 'Владелец'
    )
    if callback.message:
        await callback.message.edit_text(
            f'Сотрудник <b>{user.full_name}</b> (ID: <code>{user.telegram_id}</code>) '
            f'успешно зарегистрирован с ролью <b>{role_ru}</b>.',
        )

    users = await user_repo.get_all_users()
    if callback.message:
        await callback.message.answer(
            text='<b>Список сотрудников автосервиса:</b>',
            reply_markup=get_staff_list_kb(users),
        )
    await callback.answer('Сотрудник добавлен.')


@router.callback_query(StaffAction.filter(F.action == 'view'))
async def handle_staff_view_profile(
    callback: CallbackQuery,
    callback_data: StaffAction,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Отображает карточку управления выбранным сотрудником.

    Args:
        callback: Запрос обратного вызова.
        callback_data: Данные действия.
        current_user: Авторизованный владелец.
        session: Асинхронная сессия базы данных.
    """
    target_user = await _get_target_user_or_deny(
        callback=callback,
        current_user=current_user,
        session=session,
        user_id=callback_data.user_id,
    )
    if target_user is None:
        return

    is_self = target_user.telegram_id == current_user.telegram_id
    card_text = _format_user_card_text(
        target_user=target_user,
        current_user=current_user,
    )

    if callback.message:
        await callback.message.edit_text(
            text=card_text,
            reply_markup=get_user_card_kb(target_user, is_self=is_self),
        )
    await callback.answer()


@router.callback_query(StaffAction.filter(F.action == 'toggle'))
async def handle_staff_toggle_access(
    callback: CallbackQuery,
    callback_data: StaffAction,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Блокирует или восстанавливает доступ сотрудника.

    Args:
        callback: Запрос обратного вызова.
        callback_data: Данные действия.
        current_user: Авторизованный владелец.
        session: Асинхронная сессия базы данных.
    """
    target_user = await _get_target_user_or_deny(
        callback=callback,
        current_user=current_user,
        session=session,
        user_id=callback_data.user_id,
    )
    if target_user is None:
        return

    if target_user.telegram_id == current_user.telegram_id:
        await callback.answer(
            'Нельзя заблокировать собственный аккаунт владельца.',
            show_alert=True,
        )
        return

    target_user.is_active = not target_user.is_active
    await session.commit()

    word = 'активирован' if target_user.is_active else 'заблокирован'
    await callback.answer(f'Доступ сотрудника {word}.')

    is_self = target_user.telegram_id == current_user.telegram_id
    card_text = _format_user_card_text(
        target_user=target_user,
        current_user=current_user,
    )
    if callback.message:
        await callback.message.edit_text(
            text=card_text,
            reply_markup=get_user_card_kb(target_user, is_self=is_self),
        )


@router.callback_query(StaffAction.filter(F.action == 'role_menu'))
async def handle_staff_role_menu(
    callback: CallbackQuery,
    callback_data: StaffAction,
    current_user: User,
) -> None:
    """Открывает меню назначения новой роли сотруднику.

    Args:
        callback: Запрос обратного вызова.
        callback_data: Данные действия.
        current_user: Авторизованный владелец.
    """
    if current_user.role != UserRole.OWNER:
        await callback.answer('Доступ запрещен.', show_alert=True)
        return

    if callback.message:
        await callback.message.edit_text(
            text='Выберите новую системную роль для сотрудника:',
            reply_markup=get_role_selector_kb(callback_data.user_id),
        )
    await callback.answer()


@router.callback_query(StaffRoleAction.filter())
async def handle_staff_set_role(
    callback: CallbackQuery,
    callback_data: StaffRoleAction,
    current_user: User,
    booking_service: BookingService,
    session: AsyncSession,
) -> None:
    """Применяет выбранную системную роль сотруднику.

    Args:
        callback: Запрос обратного вызова.
        callback_data: Данные выбранной роли.
        current_user: Авторизованный владелец.
        booking_service: Сервис бизнес-логики.
        session: Асинхронная сессия базы данных.
    """
    try:
        new_role = UserRole(callback_data.role)
        updated = await booking_service.change_user_role(
            target_user_id=callback_data.user_id,
            new_role=new_role,
            owner_telegram_id=current_user.telegram_id,
        )
        await callback.answer(
            f'Роль сотрудника {updated.full_name} изменена на {new_role.value}.',
        )

        user_repo = UserRepository(session)
        target_user = await user_repo.get_by_id(callback_data.user_id)
        if target_user and callback.message:
            is_self = target_user.telegram_id == current_user.telegram_id
            card_text = _format_user_card_text(
                target_user=target_user,
                current_user=current_user,
            )
            await callback.message.edit_text(
                text=card_text,
                reply_markup=get_user_card_kb(target_user, is_self=is_self),
            )
    except (PermissionDeniedError, ValueError) as exc:
        await callback.answer(str(exc), show_alert=True)


@router.callback_query(StaffAction.filter(F.action == 'delete_ask'))
async def handle_staff_delete_ask(
    callback: CallbackQuery,
    callback_data: StaffAction,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Запрашивает подтверждение удаления сотрудника.

    Args:
        callback: Запрос обратного вызова.
        callback_data: Данные действия.
        current_user: Авторизованный владелец.
        session: Асинхронная сессия базы данных.
    """
    target_user = await _get_target_user_or_deny(
        callback=callback,
        current_user=current_user,
        session=session,
        user_id=callback_data.user_id,
    )
    if target_user is None:
        return

    if callback.message:
        await callback.message.edit_text(
            text=(
                f'Вы действительно хотите удалить сотрудника '
                f'<b>{target_user.full_name}</b> из базы данных сервиса?'
            ),
            reply_markup=get_delete_confirm_kb(target_user.id),
        )
    await callback.answer()


@router.callback_query(StaffAction.filter(F.action == 'delete_confirm'))
async def handle_staff_delete_confirm(
    callback: CallbackQuery,
    callback_data: StaffAction,
    current_user: User,
    booking_service: BookingService,
    session: AsyncSession,
) -> None:
    """Выполняет удаление сотрудника из базы данных.

    Args:
        callback: Запрос обратного вызова.
        callback_data: Данные действия.
        current_user: Авторизованный владелец.
        booking_service: Сервис управления бронированием.
        session: Асинхронная сессия базы данных.
    """
    try:
        await booking_service.delete_user_by_owner(
            target_user_id=callback_data.user_id,
            owner_telegram_id=current_user.telegram_id,
        )
        await callback.answer('Сотрудник успешно удален из системы.')

        user_repo = UserRepository(session)
        users = await user_repo.get_all_users()
        if callback.message:
            header_text = (
                '<b>Управление командой автосервиса</b>\n\n'
                'Выберите сотрудника из списка ниже для просмотра профиля, '
                'изменения роли, блокировки или удаления:\n'
                'Либо нажмите <b>«Добавить сотрудника»</b> для регистрации нового мастера.'
            )
            await callback.message.edit_text(
                text=header_text,
                reply_markup=get_staff_list_kb(users),
            )
    except PermissionDeniedError as exc:
        await callback.answer(str(exc), show_alert=True)


@router.callback_query(StaffAction.filter(F.action == 'back_list'))
async def handle_staff_back_list(
    callback: CallbackQuery,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Возвращает владельца к списку сотрудников.

    Args:
        callback: Запрос обратного вызова.
        current_user: Авторизованный владелец.
        session: Асинхронная сессия базы данных.
    """
    if current_user.role != UserRole.OWNER:
        await callback.answer('Доступ запрещен.', show_alert=True)
        return

    user_repo = UserRepository(session)
    users = await user_repo.get_all_users()
    if callback.message:
        header_text = (
            '<b>Управление командой автосервиса</b>\n\n'
            'Выберите сотрудника из списка ниже для просмотра профиля, '
            'изменения роли, блокировки или удаления:\n'
            'Либо нажмите <b>«Добавить сотрудника»</b> для регистрации нового мастера.'
        )
        await callback.message.edit_text(
            text=header_text,
            reply_markup=get_staff_list_kb(users),
        )
    await callback.answer()


@router.message(Command(commands=['clear_calendars', 'purge_calendars', 'reset_all']))
async def cmd_clear_calendars(
    message: Message,
    current_user: User,
    booking_service: BookingService,
    state: FSMContext,
) -> None:
    """Очищает события в Google Календарях и удаляет наряды из базы данных.

    Args:
        message: Сообщение Telegram.
        current_user: Авторизованный сотрудник.
        booking_service: Сервис управления бронированием.
        state: Контекст FSM.
    """
    await state.clear()
    if current_user.role != UserRole.OWNER:
        await message.answer('Команда доступна только владельцу автосервиса.')
        return

    await message.answer('Начинаю полную очистку Google Календарей и базы нарядов...')
    try:
        stats = await booking_service.clear_all_calendars_and_appointments(
            user_telegram_id=current_user.telegram_id,
        )
        report_lines = ['<b>Очистка завершена успешно:</b>\n']
        for cal_name, count in stats.items():
            report_lines.append(f'• {cal_name}: удалено {count} событий')
        report_lines.append(
            '\nВсе тестовые наряды и история изменений удалены из базы данных.'
        )
        await message.answer(text='\n'.join(report_lines))
    except BookingError as exc:
        await message.answer(f'Ошибка при очистке: <code>{exc}</code>')


@router.message(F.text == BTN_NEW_BOOKING)
async def handle_new_booking_button(
    message: Message,
    current_user: User,
    state: FSMContext,
) -> None:
    """Отправляет мастеру шаблон-подсказку для новой записи со сбросом FSM.

    Args:
        message: Сообщение с нажатой кнопкой меню.
        current_user: Текущий пользователь.
        state: Контекст FSM.
    """
    await state.clear()
    await message.answer(
        text=NEW_BOOKING_HINT_TEXT,
        reply_markup=get_main_reply_kb(current_user.role),
    )


@router.message(F.text == BTN_TODAY_LOAD)
async def handle_today_button(
    message: Message,
    booking_service: BookingService,
    state: FSMContext,
) -> None:
    """Выводит актуальную загрузку постов на сегодня по нажатию кнопки.

    Args:
        message: Сообщение Telegram.
        booking_service: Сервис бизнес-логики бронирования.
        state: Контекст FSM.
    """
    await state.clear()
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    today = datetime.datetime.now(timezone).date()
    overview = await booking_service.get_day_load_summary(today)
    await message.answer(
        text=format_today_schedule_view(overview),
        reply_markup=get_load_summary_kb(),
    )


@router.message(F.text == BTN_FREE_SLOTS)
async def handle_free_slots_button(
    message: Message,
    booking_service: BookingService,
    state: FSMContext,
) -> None:
    """Выводит список ближайших доступных окон по постам вперед.

    Args:
        message: Сообщение Telegram.
        booking_service: Сервис бизнес-логики бронирования.
        state: Контекст FSM.
    """
    await state.clear()
    slots = await booking_service.get_nearest_free_slots(duration_minutes=30)
    await message.answer(
        text=format_nearest_free_slots_view(slots),
        reply_markup=get_load_summary_kb(),
    )


@router.message(F.text == BTN_MY_BOOKINGS)
async def handle_my_bookings_button(
    message: Message,
    current_user: User,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    """Отображает список активных записей мастера по нажатию Reply-кнопки.

    Args:
        message: Сообщение Telegram.
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
    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )


@router.message(F.text == BTN_ALL_BOOKINGS)
async def handle_all_bookings_button(
    message: Message,
    current_user: User,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    """Отображает все активные наряды цеха для магазина и владельца.

    Args:
        message: Сообщение Telegram.
        current_user: Авторизованный сотрудник.
        session: Асинхронная сессия базы данных.
        state: Контекст FSM.
    """
    await state.clear()
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


@router.message(F.text == BTN_CLOSED_BOOKINGS)
async def handle_closed_bookings_button(
    message: Message,
    current_user: User,
    booking_service: BookingService,
    state: FSMContext,
) -> None:
    """Выводит список недавно закрытых, завершенных и отмененных нарядов.

    Args:
        message: Сообщение Telegram.
        current_user: Авторизованный пользователь.
        booking_service: Сервис бронирования.
        state: Контекст FSM.
    """
    await state.clear()
    closed = await booking_service.get_closed_appointments(
        user_telegram_id=current_user.telegram_id,
        limit=15,
    )
    if not closed:
        await message.answer(
            text='История закрытых записей пока пуста.',
            reply_markup=get_load_summary_kb(),
        )
        return

    await message.answer(
        text=(
            '<b>Недавно закрытые, завершенные и отмененные наряды:</b>\n'
            'Выберите запись для просмотра деталей:'
        ),
        reply_markup=get_closed_appointments_kb(closed),
    )


@router.callback_query(ClosedApptAction.filter())
async def handle_closed_appointment_card(
    callback: CallbackQuery,
    callback_data: ClosedApptAction,
    session: AsyncSession,
) -> None:
    """Отображает полную информацию по закрытой или отмененной заявке.

    Args:
        callback: Запрос обратного вызова Telegram.
        callback_data: Данные действия с публичным номером.
        session: Асинхронная сессия базы данных.
    """
    appt_repo = AppointmentRepository(session)
    appointment = await appt_repo.get_by_public_id(callback_data.public_id)
    if appointment is None:
        await callback.answer('Запись не найдена.', show_alert=True)
        return

    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    start_str = appointment.start_datetime.astimezone(timezone).strftime('%d.%m.%Y, %H:%M')
    end_str = appointment.end_datetime.astimezone(timezone).strftime('%H:%M')
    post_label = (
        POST_NAMES.get(appointment.post.code, appointment.post.name)
        if appointment.post
        else 'Без поста'
    )
    master_label = (
        appointment.master.full_name if appointment.master else 'Мастер'
    )
    closed_at_str = appointment.updated_at.astimezone(timezone).strftime('%d.%m.%Y, %H:%M')

    card = (
        f'<b>Карточка архивного наряда {appointment.public_id}</b>\n\n'
        f'• <b>Автомобиль:</b> {appointment.car_model}\n'
        f'• <b>Статус:</b> {appointment.status.value}\n'
        f'• <b>Телефон:</b> <code>{appointment.client_phone}</code>\n'
        f'• <b>Клиент:</b> {appointment.client_name or "Не указан"}\n'
        f'• <b>Мастер:</b> {master_label}\n'
        f'• <b>Пост:</b> {post_label}\n'
        f'• <b>План:</b> {start_str}–{end_str}\n'
        f'• <b>Работы:</b> {appointment.work_description}\n'
        f'• <b>Дата закрытия/отмены:</b> {closed_at_str}\n'
    )
    if appointment.master_comment:
        card += f'• <b>Комментарий мастера:</b> {appointment.master_comment}\n'

    if callback.message:
        await callback.message.answer(text=card)
    await callback.answer()
