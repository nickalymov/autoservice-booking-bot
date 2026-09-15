"""Модуль генерации постоянного главного меню Telegram-бота.

Определяет константы быстрого выбора и фабрику постоянной Reply-клавиатуры
для управления записями сервиса без необходимости ручного ввода команд.
"""

from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup

from app.config import UserRole

BTN_NEW_BOOKING: str = '🎙 Новая запись'
BTN_TODAY_LOAD: str = '📅 Загрузка сегодня'
BTN_FREE_SLOTS: str = '⏱ Свободные окна'
BTN_MY_BOOKINGS: str = '📋 Мои записи'
BTN_ALL_BOOKINGS: str = '🏬 Все записи сервиса'
BTN_STAFF_MANAGEMENT: str = '👥 Сотрудники'
BTN_REMINDERS_TOGGLE: str = '🔔 Напоминания'

NEW_BOOKING_HINT_TEXT: str = (
    '<b>Для новой записи надиктуйте или напишите боту:</b>\n\n'
    '1. Автомобиль: марка и модель <i>(обязательно)</i>\n'
    '2. Время записи <i>(обязательно, шаг 30 мин)</i>\n'
    '3. Телефон клиента <i>(обязательно)</i>\n'
    '4. Вид работ <i>(обязательно, перечислите подробно)</i>\n'
    '5. Пост <i>(P1, P2, P3, P4 или без поста)</i>\n\n'
    '<i>Дополнительно: имя клиента, госномер, VIN.</i>\n\n'
    '<b>Пример:</b>\n'
    '<i>«Запиши Киа Рио завтра на 10:00, телефон 9281234567, '
    'замена стоек стабилизатора, пост 2»</i>\n\n'
    '<b>Для переноса:</b>\n'
    '<i>«Запись Kia Rio в десять перенеси на двенадцать, '
    'на первый подъемник»</i>\n\n'
    '<b>Для завершения:</b>\n'
    '<i>«Kia Rio готова, закончил в 11:10»</i>'
)


def get_main_reply_kb(
    role: UserRole = UserRole.MECHANIC,
) -> ReplyKeyboardMarkup:
    """Создает постоянную панель быстрого доступа внизу экрана с учетом роли.

    Args:
        role: Системная роль авторизованного сотрудника.

    Returns:
        Объект ReplyKeyboardMarkup с основными действиями сервиса.
    """
    rows: list[list[KeyboardButton]] = [
        [
            KeyboardButton(text=BTN_NEW_BOOKING),
            KeyboardButton(text=BTN_TODAY_LOAD),
        ],
        [
            KeyboardButton(text=BTN_FREE_SLOTS),
            KeyboardButton(text=BTN_MY_BOOKINGS),
        ],
    ]

    if role == UserRole.OWNER:
        rows.append([
            KeyboardButton(text=BTN_ALL_BOOKINGS),
            KeyboardButton(text=BTN_STAFF_MANAGEMENT),
        ])
        rows.append([KeyboardButton(text=BTN_REMINDERS_TOGGLE)])
    elif role == UserRole.SALES:
        rows.append([
            KeyboardButton(text=BTN_ALL_BOOKINGS),
            KeyboardButton(text=BTN_REMINDERS_TOGGLE),
        ])
    else:
        rows.append([KeyboardButton(text=BTN_REMINDERS_TOGGLE)])

    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        is_persistent=True,
    )
