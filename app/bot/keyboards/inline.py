"""Модуль фабрик инлайн-клавиатур для Telegram-бота.

Определяет фабрики обратных вызовов и функции генерации клавиатур
для управления заявками, разрешения конфликтов постов и навигации.
"""

from __future__ import annotations

from collections.abc import Sequence

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from app.database.models.appointment import Appointment
from app.database.models.post import Post
from app.database.models.user import User
from app.schemas.appointment import AppointmentStatus


class BookingAction(CallbackData, prefix='book'):
    """Фабрика данных для действий с записью."""

    action: str
    public_id: str


class RescheduleConfirmAction(CallbackData, prefix='resch'):
    """Фабрика данных для подтверждения переноса записи."""

    action: str
    public_id: str


class PostAction(CallbackData, prefix='post'):
    """Фабрика данных для выбора рабочего поста."""

    post_code: str
    public_id: str


class TransferAction(CallbackData, prefix='trans'):
    """Фабрика данных для выбора мастера при передаче."""

    master_id: int
    public_id: str


class DraftMasterAction(CallbackData, prefix='drmast'):
    """Фабрика данных для назначения мастера при создании наряда магазином."""

    master_id: int
    public_id: str


class SelectCarAction(CallbackData, prefix='selcar'):
    """Фабрика данных для выбора машины при нескольких совпадениях."""

    action: str
    public_id: str


class StatusAction(CallbackData, prefix='status'):
    """Фабрика данных для изменения статуса записи."""

    action: str
    public_id: str


class MenuAction(CallbackData, prefix='menu'):
    """Фабрика данных для навигации по меню."""

    action: str


class StaffToggleAction(CallbackData, prefix='stftog'):
    """Фабрика данных для переключения активности сотрудника."""

    user_id: int


def get_confirmation_kb(public_id: str) -> InlineKeyboardMarkup:
    """Создает клавиатуру подтверждения записи.

    Args:
        public_id: Публичный идентификатор заявки.

    Returns:
        Объект клавиатуры Telegram.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Подтвердить',
                callback_data=BookingAction(
                    action='confirm',
                    public_id=public_id,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Изменить данные',
                callback_data=BookingAction(
                    action='edit',
                    public_id=public_id,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Отменить',
                callback_data=BookingAction(
                    action='cancel',
                    public_id=public_id,
                ).pack(),
            ),
        ],
    ])


def get_reschedule_confirm_kb(public_id: str) -> InlineKeyboardMarkup:
    """Создает клавиатуру подтверждения изменения записи по п. 10.4 ТЗ.

    Args:
        public_id: Публичный номер изменяемой записи.

    Returns:
        Инлайн-клавиатура с кнопками подтверждения, правки и отмены.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Подтвердить изменение',
                callback_data=RescheduleConfirmAction(
                    action='confirm',
                    public_id=public_id,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Изменить еще',
                callback_data=RescheduleConfirmAction(
                    action='edit_more',
                    public_id=public_id,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Отмена',
                callback_data=RescheduleConfirmAction(
                    action='cancel',
                    public_id=public_id,
                ).pack(),
            ),
        ],
    ])


def get_post_selector_kb(
    posts: Sequence[Post],
    public_id: str,
) -> InlineKeyboardMarkup:
    """Создает клавиатуру выбора рабочего поста.

    Args:
        posts: Список доступных постов.
        public_id: Публичный идентификатор заявки.

    Returns:
        Объект клавиатуры выбора поста.
    """
    keyboard: list[list[InlineKeyboardButton]] = []
    for post in posts:
        keyboard.append([
            InlineKeyboardButton(
                text=post.name,
                callback_data=PostAction(
                    post_code=post.code,
                    public_id=public_id,
                ).pack(),
            ),
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_post_conflict_kb(
    posts: Sequence[Post],
    public_id: str,
) -> InlineKeyboardMarkup:
    """Создает клавиатуру при занятом посте строго по разделу 10.3 ТЗ.

    Args:
        posts: Список свободных постов на это время.
        public_id: Идентификатор черновика.

    Returns:
        Клавиатура с выбором постов, другого времени и отменой.
    """
    keyboard: list[list[InlineKeyboardButton]] = []
    for post in posts:
        keyboard.append([
            InlineKeyboardButton(
                text=post.name,
                callback_data=PostAction(
                    post_code=post.code,
                    public_id=public_id,
                ).pack(),
            ),
        ])

    keyboard.append([
        InlineKeyboardButton(
            text='Выбрать другое время',
            callback_data=BookingAction(
                action='change_time',
                public_id=public_id,
            ).pack(),
        ),
    ])
    keyboard.append([
        InlineKeyboardButton(
            text='Отмена',
            callback_data=BookingAction(
                action='cancel',
                public_id=public_id,
            ).pack(),
        ),
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_appointment_actions_kb(
    public_id: str,
    status: AppointmentStatus,
) -> InlineKeyboardMarkup:
    """Создает контекстное меню действий для записи.

    Args:
        public_id: Публичный идентификатор заявки.
        status: Текущий статус записи.

    Returns:
        Объект клавиатуры действий.
    """
    rows: list[list[InlineKeyboardButton]] = []
    if status == AppointmentStatus.CONFIRMED:
        rows.append([
            InlineKeyboardButton(
                text='Взять в работу',
                callback_data=StatusAction(
                    action='start',
                    public_id=public_id,
                ).pack(),
            ),
        ])
        rows.append([
            InlineKeyboardButton(
                text='Перенести',
                callback_data=StatusAction(
                    action='reschedule',
                    public_id=public_id,
                ).pack(),
            ),
            InlineKeyboardButton(
                text='Передать',
                callback_data=StatusAction(
                    action='transfer',
                    public_id=public_id,
                ).pack(),
            ),
        ])
        rows.append([
            InlineKeyboardButton(
                text='Не приехал',
                callback_data=StatusAction(
                    action='no_show',
                    public_id=public_id,
                ).pack(),
            ),
            InlineKeyboardButton(
                text='Отмена',
                callback_data=StatusAction(
                    action='cancel',
                    public_id=public_id,
                ).pack(),
            ),
        ])
    elif status == AppointmentStatus.IN_PROGRESS:
        rows.append([
            InlineKeyboardButton(
                text='Завершить',
                callback_data=StatusAction(
                    action='complete',
                    public_id=public_id,
                ).pack(),
            ),
            InlineKeyboardButton(
                text='Отмена',
                callback_data=StatusAction(
                    action='cancel',
                    public_id=public_id,
                ).pack(),
            ),
        ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_mechanic_selector_kb(
    mechanics: Sequence[User],
    public_id: str,
) -> InlineKeyboardMarkup:
    """Создает клавиатуру выбора мастера для передачи записи.

    Args:
        mechanics: Список доступных мастеров.
        public_id: Публичный идентификатор заявки.

    Returns:
        Объект клавиатуры выбора исполнителя.
    """
    keyboard: list[list[InlineKeyboardButton]] = []
    for mechanic in mechanics:
        keyboard.append([
            InlineKeyboardButton(
                text=mechanic.full_name,
                callback_data=TransferAction(
                    master_id=mechanic.id,
                    public_id=public_id,
                ).pack(),
            ),
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_draft_master_selector_kb(
    mechanics: Sequence[User],
    public_id: str,
) -> InlineKeyboardMarkup:
    """Создает клавиатуру назначения мастера для магазина.

    Args:
        mechanics: Список активных мастеров сервиса.
        public_id: Идентификатор черновика заявки.

    Returns:
        Объект инлайн-клавиатуры выбора мастера.
    """
    keyboard: list[list[InlineKeyboardButton]] = []
    for mechanic in mechanics:
        keyboard.append([
            InlineKeyboardButton(
                text=mechanic.full_name,
                callback_data=DraftMasterAction(
                    master_id=mechanic.id,
                    public_id=public_id,
                ).pack(),
            ),
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_multiple_cars_selector_kb(
    appointments: Sequence[Appointment],
    action: str,
) -> InlineKeyboardMarkup:
    """Создает клавиатуру выбора автомобиля при множественных совпадениях.

    Args:
        appointments: Список найденных активных записей.
        action: Тип выполняемого действия.

    Returns:
        Инлайн-клавиатура с кнопками найденных записей.
    """
    keyboard: list[list[InlineKeyboardButton]] = []
    for appt in appointments:
        master_name = appt.master.full_name if appt.master else 'Мастер'
        post_label = appt.post.code if appt.post else 'Без поста'
        btn_label = (
            f'{appt.public_id}: {appt.car_model} '
            f'({master_name}, {post_label})'
        )
        keyboard.append([
            InlineKeyboardButton(
                text=btn_label,
                callback_data=SelectCarAction(
                    action=action,
                    public_id=appt.public_id,
                ).pack(),
            ),
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_load_summary_kb() -> InlineKeyboardMarkup:
    """Создает меню просмотра загрузки сервиса согласно п. 10.9 ТЗ.

    Returns:
        Объект клавиатуры меню загрузки.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Загрузка сегодня',
                callback_data=MenuAction(action='today').pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Загрузка завтра',
                callback_data=MenuAction(action='tomorrow').pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Свободные окна',
                callback_data=MenuAction(action='free_slots').pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Мои записи',
                callback_data=MenuAction(action='my_appointments').pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Создать запись',
                callback_data=MenuAction(action='create_booking').pack(),
            ),
        ],
    ])


def get_staff_management_kb(
    users: Sequence[User],
) -> InlineKeyboardMarkup:
    """Создает интерактивную панель управления доступом сотрудников.

    Args:
        users: Список зарегистрированных сотрудников.

    Returns:
        Инлайн-клавиатура переключения доступа сотрудников.
    """
    keyboard: list[list[InlineKeyboardButton]] = []
    for user in users:
        status_icon = '🟢' if user.is_active else '🔴'
        btn_label = f'{status_icon} {user.full_name} ({user.role.value})'
        keyboard.append([
            InlineKeyboardButton(
                text=btn_label,
                callback_data=StaffToggleAction(user_id=user.id).pack(),
            ),
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
