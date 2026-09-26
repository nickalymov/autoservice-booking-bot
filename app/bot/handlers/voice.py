"""Модуль создания записей из голосовых и текстовых сообщений.

Обеспечивает прием аудио и текста, транскрибацию через Whisper,
извлечение реквизитов через GPT-4o-mini, маршрутизацию намерений мастера
(создание, перенос, завершение) согласно разделам 9 и 10 ТЗ.
"""

from __future__ import annotations

import datetime
import zoneinfo

from aiogram import Bot
from aiogram import F
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.booking import progress_appointment_draft
from app.bot.handlers.management import get_early_release_kb
from app.bot.handlers.management import show_reschedule_preview
from app.bot.keyboards.inline import get_multiple_cars_selector_kb
from app.bot.keyboards.reply import BTN_ALL_BOOKINGS
from app.bot.keyboards.reply import BTN_CLOSED_BOOKINGS
from app.bot.keyboards.reply import BTN_FREE_SLOTS
from app.bot.keyboards.reply import BTN_MY_BOOKINGS
from app.bot.keyboards.reply import BTN_NEW_BOOKING
from app.bot.keyboards.reply import BTN_REMINDERS_TOGGLE
from app.bot.keyboards.reply import BTN_STAFF_MANAGEMENT
from app.bot.keyboards.reply import BTN_TODAY_LOAD
from app.config import TIMEZONE_NAME
from app.config import PostCode
from app.config import UserRole
from app.core.booking_service import BookingService
from app.core.duration_estimator import estimate_duration_minutes
from app.database.models import Appointment
from app.database.models import User
from app.database.repositories import UserRepository
from app.schemas.appointment import ActionIntent
from app.schemas.appointment import AppointmentDraft
from app.schemas.appointment import AppointmentExtraction
from app.schemas.appointment import AppointmentSource
from app.services.ai_service import AIService
from app.services.ai_service import AIServiceError

router = Router()

_IGNORED_REPLY_BUTTONS: frozenset[str] = frozenset({
    BTN_NEW_BOOKING,
    BTN_TODAY_LOAD,
    BTN_FREE_SLOTS,
    BTN_MY_BOOKINGS,
    BTN_ALL_BOOKINGS,
    BTN_CLOSED_BOOKINGS,
    BTN_STAFF_MANAGEMENT,
    BTN_REMINDERS_TOGGLE,
})


def _parse_start_datetime(
    date_str: str | None,
    time_str: str | None,
) -> datetime.datetime | None:
    """Преобразует строковые дату и время в объект с московским часовым поясом.

    Args:
        date_str: Дата в формате YYYY-MM-DD или None.
        time_str: Время в формате HH:MM или None.

    Returns:
        Объект datetime с часовым поясом Europe/Moscow либо None.
    """
    if not date_str or not time_str:
        return None
    try:
        timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
        parsed_dt = datetime.datetime.strptime(
            f'{date_str} {time_str}',
            '%Y-%m-%d %H:%M',
        )
        return parsed_dt.replace(tzinfo=timezone)
    except ValueError:
        return None


def _generate_draft_id() -> str:
    """Формирует временный идентификатор черновика заявки.

    Returns:
        Строковый уникальный номер черновика.
    """
    now = datetime.datetime.now()
    return f'DRAFT-{now.strftime("%y%m%d%H%M%S")}'


async def _handle_complete_intent(
    extraction: AppointmentExtraction,
    message: Message,
    booking_service: BookingService,
) -> None:
    """Обрабатывает намерение досрочного завершения ремонта по разделу 10.7 ТЗ.

    Args:
        extraction: Извлеченные сущности.
        message: Входящее сообщение Telegram.
        booking_service: Сервис бронирования.
    """
    car_query = extraction.target_car_for_action or extraction.car_model
    if not car_query:
        await message.answer(
            text='Укажите автомобиль, который закончили ремонтировать.',
        )
        return

    found = await booking_service.find_active_by_car(car_query)
    if not found:
        await message.answer(
            text=f'Активных нарядов на автомобиль «{car_query}» не найдено.',
        )
        return

    if len(found) > 1:
        await message.answer(
            text=(
                f'Найдено несколько активных записей по запросу «{car_query}».\n'
                'Выберите нужный автомобиль для завершения:'
            ),
            reply_markup=get_multiple_cars_selector_kb(
                appointments=found,
                action='complete',
            ),
        )
        return

    appointment = found[0]
    await prompt_early_release_for_appointment(
        message=message,
        appointment=appointment,
        completion_time_str=extraction.completion_actual_time,
    )


async def prompt_early_release_for_appointment(
    message: Message,
    appointment: Appointment,
    completion_time_str: str | None = None,
) -> None:
    """Запрашивает у мастера подтверждение освобождения поста при закрытии.

    Args:
        message: Сообщение Telegram для отправки ответа.
        appointment: Целевая запись на ремонт.
        completion_time_str: Опционально названное время завершения (HH:MM).
    """
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    now_dt = datetime.datetime.now(timezone)

    if completion_time_str:
        try:
            parsed_time = datetime.datetime.strptime(
                completion_time_str,
                '%H:%M',
            ).time()
            now_dt = now_dt.replace(
                hour=parsed_time.hour,
                minute=parsed_time.minute,
                second=0,
                microsecond=0,
            )
        except ValueError:
            pass

    planned_end_msk = appointment.end_datetime.astimezone(timezone)
    post_label = (
        appointment.post.name if appointment.post else 'Без поста'
    )
    planned_end_str = planned_end_msk.strftime('%H:%M')
    actual_time_str = now_dt.strftime('%H:%M')

    await message.answer(
        text=(
            f'Наряд <b>[{appointment.public_id}] ({appointment.car_model})</b>.\n'
            f'Запись была запланирована до {planned_end_str}.\n'
            f'Освободить {post_label} с {actual_time_str}?'
        ),
        reply_markup=get_early_release_kb(
            public_id=appointment.public_id,
            planned_end_str=planned_end_str,
        ),
    )


async def _handle_reschedule_intent(
    extraction: AppointmentExtraction,
    message: Message,
    booking_service: BookingService,
    state: FSMContext,
) -> None:
    """Обрабатывает намерение переноса наряда по разделу 10.4 ТЗ.

    Args:
        extraction: Извлеченные сущности.
        message: Входящее сообщение Telegram.
        booking_service: Сервис бронирования.
        state: Контекст FSM.
    """
    car_query = extraction.target_car_for_action or extraction.car_model
    if not car_query:
        await message.answer(
            text='Укажите автомобиль для переноса записи.',
        )
        return

    found = await booking_service.find_active_by_car(car_query)
    if not found:
        await message.answer(
            text=f'Активных нарядов на автомобиль «{car_query}» не найдено.',
        )
        return

    if len(found) > 1:
        await message.answer(
            text=(
                f'Найдено несколько активных записей по запросу «{car_query}».\n'
                'Выберите нужный автомобиль для переноса:'
            ),
            reply_markup=get_multiple_cars_selector_kb(
                appointments=found,
                action='reschedule',
            ),
        )
        return

    appointment = found[0]
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    current_date_str = appointment.start_datetime.astimezone(
        timezone,
    ).strftime('%Y-%m-%d')

    target_date = extraction.reschedule_new_date or current_date_str
    target_time = extraction.reschedule_new_time or extraction.start_time

    if not target_time:
        await message.answer(
            text=f'На какое время перенести запись {appointment.car_model}?',
        )
        return

    new_start_dt = _parse_start_datetime(target_date, target_time)
    if new_start_dt is None:
        await message.answer(text='Не удалось определить новое время записи.')
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


async def _process_appointment_text(
    raw_text: str,
    source: AppointmentSource,
    message: Message,
    ai_service: AIService,
    booking_service: BookingService,
    state: FSMContext,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Извлекает сущности из текста и инициирует карточку или выбор постов.

    Args:
        raw_text: Исходный текст заявки от мастера.
        source: Источник поступления данных.
        message: Входящее сообщение Telegram для отправки ответа.
        ai_service: Сервис искусственного интеллекта.
        booking_service: Сервис бизнес-логики бронирования.
        state: Контекст конечного автомата FSM.
        current_user: Сущность авторизованного сотрудника.
        session: Асинхронная сессия базы данных.
    """
    try:
        extraction = await ai_service.extract_appointment(raw_text=raw_text)
    except AIServiceError as exc:
        await message.answer(
            text=(
                'Не удалось обработать заявку через нейросеть.\n'
                f'Детали: <code>{exc}</code>\n\n'
                'Попробуйте надиктовать сообщение повторно или '
                'указать марку, время и пост более подробно.'
            ),
        )
        return

    if extraction.intent == ActionIntent.COMPLETE:
        await _handle_complete_intent(
            extraction=extraction,
            message=message,
            booking_service=booking_service,
        )
        return

    if extraction.intent == ActionIntent.RESCHEDULE:
        await _handle_reschedule_intent(
            extraction=extraction,
            message=message,
            booking_service=booking_service,
            state=state,
        )
        return

    if extraction.clarification_needed:
        await message.answer(
            text=f'Нужно уточнение:\n{extraction.clarification_needed}',
        )
        return

    start_dt = _parse_start_datetime(
        date_str=extraction.start_date,
        time_str=extraction.start_time,
    )

    normative_duration = estimate_duration_minutes(
        work_description=extraction.work_description,
        work_items=extraction.work_items,
    )
    ai_duration = extraction.suggested_duration_minutes

    if ai_duration and ai_duration > normative_duration:
        duration = ai_duration
    else:
        duration = normative_duration

    user_repo = UserRepository(session)
    assigned_master_id: int | None = None
    assigned_master_name: str = current_user.full_name
    assigned_master_tg_id: int = current_user.telegram_id

    if extraction.assigned_master_name:
        found_mechanic = await user_repo.find_mechanic_by_name(
            extraction.assigned_master_name,
        )
        if found_mechanic is not None:
            assigned_master_id = found_mechanic.id
            assigned_master_name = found_mechanic.full_name
            assigned_master_tg_id = found_mechanic.telegram_id
    elif current_user.role == UserRole.MECHANIC:
        assigned_master_id = current_user.id
        assigned_master_name = current_user.full_name
        assigned_master_tg_id = current_user.telegram_id

    draft_id = _generate_draft_id()
    draft = AppointmentDraft(
        draft_id=draft_id,
        master_telegram_id=assigned_master_tg_id,
        master_name=assigned_master_name,
        master_id=assigned_master_id,
        source=source,
        raw_transcription=raw_text,
        car_model=extraction.car_model,
        client_phone=extraction.client_phone,
        client_name=extraction.client_name,
        license_plate=extraction.license_plate,
        vin=extraction.vin,
        work_description=extraction.work_description,
        work_items=extraction.work_items,
        start_datetime=start_dt,
        planned_duration_minutes=duration,
        post_code=extraction.post_code,
    )

    await progress_appointment_draft(
        message=message,
        state=state,
        draft=draft,
        booking_service=booking_service,
        current_user=current_user,
        session=session,
    )


@router.message(StateFilter(None), F.voice)
async def handle_voice(
    message: Message,
    bot: Bot,
    ai_service: AIService,
    booking_service: BookingService,
    state: FSMContext,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Обрабатывает входящее голосовое сообщение со сбросом зависшего FSM.

    Args:
        message: Сообщение с голосовым вложением.
        bot: Экземпляр клиента Telegram Bot API.
        ai_service: Сервис распознавания речи и парсинга сущностей.
        booking_service: Сервис бизнес-логики бронирования.
        state: Контекст FSM для сохранения черновика.
        current_user: Авторизованный сотрудник сервиса.
        session: Асинхронная сессия базы данных.
    """
    if not message.voice:
        return

    await state.clear()
    await message.answer(text='Обрабатываю аудио...')

    file = await bot.get_file(message.voice.file_id)
    file_bytes = await bot.download_file(file.file_path)

    if file_bytes is None:
        await message.answer(text='Ошибка при загрузке аудиофайла.')
        return

    try:
        transcription = await ai_service.transcribe_audio(
            audio_bytes=file_bytes.read(),
        )
    except AIServiceError as exc:
        await message.answer(
            text=(
                'Не удалось распознать голосовое сообщение.\n'
                f'Ошибка: <code>{exc}</code>'
            ),
        )
        return

    await message.answer(text=f'Расшифровка:\n<i>{transcription}</i>')

    await _process_appointment_text(
        raw_text=transcription,
        source=AppointmentSource.VOICE,
        message=message,
        ai_service=ai_service,
        booking_service=booking_service,
        state=state,
        current_user=current_user,
        session=session,
    )


@router.message(StateFilter(None), F.text, ~F.text.startswith('/'))
async def handle_text_booking(
    message: Message,
    ai_service: AIService,
    booking_service: BookingService,
    state: FSMContext,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Обрабатывает текстовый ввод заявки по разделу 10.1 ТЗ со сбросом FSM.

    Args:
        message: Сообщение с текстом заявки.
        ai_service: Сервис распознавания и извлечения сущностей.
        booking_service: Сервис бизнес-логики бронирования.
        state: Контекст FSM.
        current_user: Авторизованный сотрудник сервиса.
        session: Асинхронная сессия базы данных.
    """
    if not message.text or message.text in _IGNORED_REPLY_BUTTONS:
        return

    await state.clear()
    await message.answer(text='Анализирую данные сообщения...')

    await _process_appointment_text(
        raw_text=message.text,
        source=AppointmentSource.TEXT,
        message=message,
        ai_service=ai_service,
        booking_service=booking_service,
        state=state,
        current_user=current_user,
        session=session,
    )
