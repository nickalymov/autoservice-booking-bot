"""Пакет генераторов клавиатур и меню Telegram-бота.

Экспортирует фабрики инлайн-кнопок, постоянное Reply-меню
быстрого доступа и текстовые шаблоны для надиктовки.
"""

from app.bot.keyboards.inline import BookingAction
from app.bot.keyboards.inline import MenuAction
from app.bot.keyboards.inline import PostAction
from app.bot.keyboards.inline import StatusAction
from app.bot.keyboards.inline import TransferAction
from app.bot.keyboards.inline import get_appointment_actions_kb
from app.bot.keyboards.inline import get_confirmation_kb
from app.bot.keyboards.inline import get_load_summary_kb
from app.bot.keyboards.inline import get_mechanic_selector_kb
from app.bot.keyboards.inline import get_post_selector_kb
from app.bot.keyboards.reply import BTN_FREE_SLOTS
from app.bot.keyboards.reply import BTN_MY_BOOKINGS
from app.bot.keyboards.reply import BTN_NEW_BOOKING
from app.bot.keyboards.reply import BTN_TODAY_LOAD
from app.bot.keyboards.reply import NEW_BOOKING_HINT_TEXT
from app.bot.keyboards.reply import get_main_reply_kb

__all__: tuple[str, ...] = (
    'BTN_FREE_SLOTS',
    'BTN_MY_BOOKINGS',
    'BTN_NEW_BOOKING',
    'BTN_TODAY_LOAD',
    'BookingAction',
    'MenuAction',
    'NEW_BOOKING_HINT_TEXT',
    'PostAction',
    'StatusAction',
    'TransferAction',
    'get_appointment_actions_kb',
    'get_confirmation_kb',
    'get_load_summary_kb',
    'get_main_reply_kb',
    'get_mechanic_selector_kb',
    'get_post_selector_kb',
)
