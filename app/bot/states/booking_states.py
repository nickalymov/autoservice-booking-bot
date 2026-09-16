"""Модуль состояний FSM для процесса бронирования записи на ремонт.

Определяет набор состояний конечного автомата, используемых для
управления диалогом с мастером при создании и редактировании заявок.
"""

from __future__ import annotations

from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class BookingState(StatesGroup):
    """Группа состояний процесса бронирования записи и управления персоналом.

    Attributes:
        waiting_for_confirmation: Ожидание подтверждения карточки записи.
        waiting_for_edit: Ожидание ввода исправленных данных.
        waiting_for_post_selection: Ожидание выбора поста из списка.
        waiting_for_new_time: Ожидание ввода нового времени записи.
        waiting_for_missing_field: Ожидание ввода недостающего поля.
        waiting_for_reschedule_edit: Ожидание дополнительных правок переноса.
        waiting_for_master_selection: Ожидание выбора ответственного мастера.
        waiting_for_new_user_id: Ожидание ввода Telegram ID нового сотрудника.
        waiting_for_new_user_name: Ожидание ввода имени нового сотрудника.
    """

    waiting_for_confirmation = State()
    waiting_for_edit = State()
    waiting_for_post_selection = State()
    waiting_for_new_time = State()
    waiting_for_missing_field = State()
    waiting_for_reschedule_edit = State()
    waiting_for_master_selection = State()
    waiting_for_new_user_id = State()
    waiting_for_new_user_name = State()
