"""Модуль обработчиков интерактивных действий с черновиками записей.

Обеспечивает подтверждение нарядов, выбор свободных постов цеха,
ручное редактирование реквизитов текстом и голосом, дозапрос пропущенных
обязательных полей, а также отмену.
"""

from __future__ import annotations

import datetime
import html
import re
import zoneinfo

from aiogram import Bot
from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import BookingAction
from app.bot.keyboards.inline import DraftMasterAction
from app.bot.keyboards.inline import MasterOverlapChoiceAction
from app.bot.keyboards.inline import OvertimeChoiceAction
from app.bot.keyboards.inline import PostAction
from app.bot.keyboards.inline import SundayChoiceAction
from app.bot.keyboards.inline import get_cancel_only_kb
from app.bot.keyboards.inline import get_confirmation_kb
from app.bot.keyboards.inline import get_draft_master_selector_kb
from app.bot.keyboards.inline import get_master_overlap_warning_kb
from app.bot.keyboards.inline import get_overtime_warning_kb
from app.bot.keyboards.inline import get_post_conflict_kb
from app.bot.keyboards.inline import get_post_selector_kb
from app.bot.keyboards.inline import get_sunday_warning_kb
from app.bot.states.booking_states import BookingState
from app.config import POST_NAMES
from app.config import TIMEZONE_NAME
from app.config import WORK_DAY_END_HOUR
from app.config import PostCode
from app.config import UserRole
from app.core.booking_service import BookingError
from app.core.booking_service import BookingService
from app.core.booking_service import OvertimeNoticeError
from app.core.booking_service import PastTimeError
from app.core.booking_service import SundayNoticeError
from app.database.models import User
from app.database.repositories import UserRepository
from app.schemas.appointment import AppointmentDraft
from app.services.ai_service import AIService
from app.services.ai_service import AIServiceError

router = Router()

_STOP_WORDS: tuple[str, ...] = (
    'не записывать',
    'отмена',
    'отменить',
    'стоп',
    'не надо',
    'отбой',
    'назад',
    'не нужно',
    'хватит',
    'отменяй',
)


def _is_cancellation_text(raw_text: str) -> bool:
    """Проверяет наличие стоп-слов отмены в тексте сообщения пользователя.

    Args:
        raw_text: Исходный текст сообщения.

    Returns:
        True, если в сообщении выражено намерение отменить действие.
    """
    clean_text = raw_text.strip().lower()
    return any(word in clean_text for word in _STOP_WORDS)


def _parse_time_fast(raw_text: str) -> str | None:
    """Извлекает время в формате HH:MM регулярным выражением.

    Args:
        raw_text: Входящая строка.

    Returns:
        Строка времени HH:MM или None.
    """
    match = re.search(r'\b([01]?\d|2[0-3])[:.-]?([0-5]\d)\b', raw_text.strip())
    if match:
        hours, minutes = match.group(1), match.group(2)
        return f'{int(hours):02d}:{minutes}'

    match_hour_only = re.search(r'\b([01]?\d|2[0-3])\b', raw_text.strip())
    if match_hour_only:
        hours = match_hour_only.group(1)
        return f'{int(hours):02d}:00'

    return None


async def extract_message_text(
    message: Message,
    bot: Bot,
    ai_service: AIService,
) -> str | None:
    """Извлекает текстовое содержимое из текстового или голосового сообщения.

    Args:
        message: Входящее сообщение Telegram.
        bot: Экземпляр клиента Telegram Bot API.
        ai_service: Сервис искусственного интеллекта.

    Returns:
        Распознанный или введенный текст сообщения либо None при ошибке.
    """
    if message.text:
        return message.text.strip()

    if message.voice:
        file = await bot.get_file(message.voice.file_id)
        file_bytes = await bot.download_file(file.file_path)
        if file_bytes is None:
            await message.answer('Ошибка при загрузке аудиофайла.')
            return None
        try:
            transcription = await ai_service.transcribe_audio(
                audio_bytes=file_bytes.read(),
            )
            await message.answer(f'Расшифровка:\n<i>{transcription}</i>')
            return transcription.strip()
        except AIServiceError as exc:
            await message.answer(
                f'Не удалось распознать голосовое сообщение: <code>{exc}</code>'
            )
            return None

    return None


async def _load_draft_and_extract_text(
    message: Message,
    bot: Bot,
    state: FSMContext,
    ai_service: AIService,
) -> tuple[AppointmentDraft | None, str | None]:
    """Загружает черновик из FSM и извлекает входящий текст или расшифровку.

    Args:
        message: Входящее сообщение Telegram.
        bot: Экземпляр клиента Telegram Bot API.
        state: Контекст конечного автомата FSM.
        ai_service: Сервис искусственного интеллекта.

    Returns:
        Кортеж из объекта AppointmentDraft и строки текста либо (None, None).
    """
    raw_text = await extract_message_text(
        message=message,
        bot=bot,
        ai_service=ai_service,
    )
    if not raw_text:
        return None, None

    data = await state.get_data()
    if 'draft' not in data:
        await message.answer('Черновик не найден. Начните запись заново.')
        await state.clear()
        return None, None

    draft = AppointmentDraft(**data['draft'])
    return draft, raw_text


async def _load_active_draft_or_handle_cancel(
    message: Message,
    bot: Bot,
    state: FSMContext,
    ai_service: AIService,
    cancel_message: str = 'Создание записи отменено.',
) -> tuple[AppointmentDraft | None, str | None]:
    """Загружает черновик и прерывает сценарий при наличии команды отмены.

    Args:
        message: Входящее сообщение Telegram.
        bot: Экземпляр клиента Telegram Bot API.
        state: Контекст конечного автомата FSM.
        ai_service: Сервис искусственного интеллекта.
        cancel_message: Текст ответа при обнаружении стоп-слова отмены.

    Returns:
        Кортеж из черновика и распознанного текста, либо (None, None).
    """
    draft, raw_text = await _load_draft_and_extract_text(
        message=message,
        bot=bot,
        state=state,
        ai_service=ai_service,
    )
    if draft is None or raw_text is None:
        return None, None

    if _is_cancellation_text(raw_text):
        await state.clear()
        await message.answer(cancel_message)
        return None, None

    return draft, raw_text


async def _resolve_time_and_date(
    raw_text: str,
    ai_service: AIService,
) -> tuple[str | None, str | None]:
    """Извлекает время и дату из сообщения быстрым regex или через ИИ.

    Args:
        raw_text: Входящий текст пользователя.
        ai_service: Сервис искусственного интеллекта.

    Returns:
        Кортеж со строками времени (HH:MM) и даты (YYYY-MM-DD) или (None, None).
    """
    fast_time = _parse_time_fast(raw_text)
    if fast_time:
        return fast_time, None

    try:
        extraction = await ai_service.extract_appointment(raw_text=raw_text)
        return extraction.start_time, extraction.start_date
    except AIServiceError:
        return None, None


async def _apply_parsed_datetime(
    message: Message,
    draft: AppointmentDraft,
    target_time_str: str,
    target_date_str: str | None,
    fallback_date: datetime.date,
) -> bool:
    """Парсит дату и время и записывает их в черновик наряда.

    Args:
        message: Сообщение для отправки ошибки валидации.
        draft: Черновик заявки.
        target_time_str: Время в формате HH:MM.
        target_date_str: Опциональная дата YYYY-MM-DD.
        fallback_date: Резервная дата при отсутствии явной.

    Returns:
        True при успешном парсинге, False при ошибке формата.
    """
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    date_str = target_date_str or fallback_date.strftime('%Y-%m-%d')
    try:
        parsed_dt = datetime.datetime.strptime(
            f'{date_str} {target_time_str}',
            '%Y-%m-%d %H:%M',
        ).replace(tzinfo=timezone)
        draft.start_datetime = parsed_dt
        return True
    except ValueError:
        await message.answer(
            text='Некорректный формат времени. Укажите, например: 14:00:',
            reply_markup=get_cancel_only_kb(draft.draft_id),
        )
        return False


async def progress_appointment_draft(
    message: Message,
    state: FSMContext,
    draft: AppointmentDraft,
    booking_service: BookingService,
    current_user: User | None = None,
    session: AsyncSession | None = None,
) -> None:
    """Проверяет полноту полей черновика и направляет на следующий шаг.

    Args:
        message: Сообщение для отправки ответов мастеру.
        state: Контекст конечного автомата FSM.
        draft: Текущий экземпляр черновика наряда.
        booking_service: Сервис бизнес-логики бронирования.
        current_user: Текущий авторизованный пользователь.
        session: Асинхронная сессия базы данных.
    """
    if not draft.car_model:
        await state.set_data({
            'draft': draft.model_dump(),
            'missing_field': 'car_model',
        })
        await state.set_state(BookingState.waiting_for_missing_field)
        await message.answer(
            text='Укажите марку и модель автомобиля:',
            reply_markup=get_cancel_only_kb(draft.draft_id),
        )
        return

    if draft.start_datetime is None:
        await state.set_data({
            'draft': draft.model_dump(),
            'missing_field': 'start_datetime',
        })
        await state.set_state(BookingState.waiting_for_missing_field)
        await message.answer(
            text='Во сколько записать? Шаг записи — 30 минут (например: на 10:00):',
            reply_markup=get_cancel_only_kb(draft.draft_id),
        )
        return

    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    now_dt = datetime.datetime.now(timezone)

    if draft.start_datetime < now_dt:
        draft.start_datetime = None
        await state.set_data({
            'draft': draft.model_dump(),
            'missing_field': 'start_datetime',
        })
        await state.set_state(BookingState.waiting_for_missing_field)
        await message.answer(
            text=(
                f'Указанное время уже прошло (сейчас {now_dt.strftime("%H:%M")}).\n'
                'На какое будущее время записать автомобиль? (Шаг 30 минут):'
            ),
            reply_markup=get_cancel_only_kb(draft.draft_id),
        )
        return

    if not draft.client_phone:
        await state.set_data({
            'draft': draft.model_dump(),
            'missing_field': 'client_phone',
        })
        await state.set_state(BookingState.waiting_for_missing_field)
        await message.answer(
            text='Укажите номер телефона клиента для связи:',
            reply_markup=get_cancel_only_kb(draft.draft_id),
        )
        return

    if not draft.work_description and not draft.work_items:
        await state.set_data({
            'draft': draft.model_dump(),
            'missing_field': 'work_description',
        })
        await state.set_state(BookingState.waiting_for_missing_field)
        await message.answer(
            text='Укажите причину обращения или перечень работ:',
            reply_markup=get_cancel_only_kb(draft.draft_id),
        )
        return

    if draft.start_datetime.weekday() == 6 and not draft.is_sunday_confirmed:
        await state.set_data({'draft': draft.model_dump()})
        await state.set_state(BookingState.waiting_for_sunday_decision)
        sunday_date_str = draft.start_datetime.strftime('%d.%m.%Y')
        await message.answer(
            text=(
                f'Дата {sunday_date_str} — воскресенье, обычно это выходной день.\n'
                'Куда записать наряд?'
            ),
            reply_markup=get_sunday_warning_kb(draft.draft_id),
        )
        return

    duration = draft.planned_duration_minutes or 30
    end_dt = draft.start_datetime + datetime.timedelta(minutes=duration)
    work_end_dt = datetime.datetime.combine(
        draft.start_datetime.date(),
        datetime.time(WORK_DAY_END_HOUR, 0),
        tzinfo=timezone,
    )

    if end_dt > work_end_dt and not draft.is_overtime_confirmed:
        await state.set_data({'draft': draft.model_dump()})
        await state.set_state(BookingState.waiting_for_overtime_decision)
        await message.answer(
            text=(
                f'Запись до {end_dt.strftime("%H:%M")} выходит за пределы '
                f'базового графика автосервиса ({WORK_DAY_END_HOUR}:00).\n'
                'Подтвердить сверхурочную работу мастера?'
            ),
            reply_markup=get_overtime_warning_kb(draft.draft_id),
        )
        return

    if (
        current_user is not None
        and current_user.role in (UserRole.SALES, UserRole.OWNER)
        and draft.master_id is None
        and session is not None
    ):
        user_repo = UserRepository(session)
        mechanics = await user_repo.get_active_mechanics()
        if mechanics:
            await state.set_data({'draft': draft.model_dump()})
            await state.set_state(BookingState.waiting_for_master_selection)
            await message.answer(
                text='Выберите ответственного мастера для этой записи:',
                reply_markup=get_draft_master_selector_kb(
                    mechanics=mechanics,
                    public_id=draft.draft_id,
                ),
            )
            return

    if draft.master_id and not draft.is_master_overlap_confirmed:
        overlap_appt = await booking_service.check_master_overlap(
            master_id=draft.master_id,
            start_dt=draft.start_datetime,
            end_dt=end_dt,
        )
        if overlap_appt is not None:
            ov_start = overlap_appt.start_datetime.astimezone(timezone).strftime('%H:%M')
            ov_end = overlap_appt.end_datetime.astimezone(timezone).strftime('%H:%M')
            ov_post = (
                overlap_appt.post.name if overlap_appt.post else 'Без поста'
            )
            draft.master_overlap_info = (
                f'У мастера {draft.master_name} на этот интервал '
                f'({ov_start}–{ov_end}) уже есть наряд: '
                f'{overlap_appt.car_model} на {ov_post}.'
            )
            await state.set_data({'draft': draft.model_dump()})
            await state.set_state(BookingState.waiting_for_master_overlap_decision)
            await message.answer(
                text=(
                    f'⚠️ <b>Внимание:</b> {draft.master_overlap_info}\n\n'
                    'Подтвердить запись всё равно или выбрать другое время?'
                ),
                reply_markup=get_master_overlap_warning_kb(draft.draft_id),
            )
            return

    try:
        check_result = await booking_service.check_slot(
            post_code=draft.post_code,
            start_dt=draft.start_datetime,
            end_dt=end_dt,
            allow_sunday=draft.is_sunday_confirmed,
            allow_overtime=draft.is_overtime_confirmed,
        )
    except PastTimeError:
        draft.start_datetime = None
        await state.set_data({
            'draft': draft.model_dump(),
            'missing_field': 'start_datetime',
        })
        await state.set_state(BookingState.waiting_for_missing_field)
        await message.answer(
            text='Указанное время уже прошло. Введите новое время (Шаг 30 минут):',
            reply_markup=get_cancel_only_kb(draft.draft_id),
        )
        return
    except (SundayNoticeError, OvertimeNoticeError) as exc:
        await message.answer(str(exc))
        return

    if draft.post_code is None:
        await state.set_data({'draft': draft.model_dump()})
        await state.set_state(BookingState.waiting_for_post_selection)

        available_names = [
            post.name
            for post in check_result.available_posts
            if post.code != PostCode.NO_POST
        ]
        slots_text = (
            ', '.join(available_names)
            if available_names
            else 'нет свободных'
        )
        time_str = draft.start_datetime.strftime('%H:%M')

        await message.answer(
            text=(
                f'На {time_str} свободны: {slots_text} или без поста.\n'
                'Выберите рабочий пост:'
            ),
            reply_markup=get_post_selector_kb(
                posts=check_result.available_posts,
                public_id=draft.draft_id,
            ),
        )
        return

    if not check_result.is_available:
        await state.set_data({'draft': draft.model_dump()})
        await state.set_state(BookingState.waiting_for_post_selection)

        conflict = check_result.conflicting_appointment
        if conflict:
            conflict_start = conflict.start_datetime.astimezone(timezone)
            conflict_end = conflict.end_datetime.astimezone(timezone)
            conflict_date_str = conflict_start.strftime('%d.%m')
            conflict_from = conflict_start.strftime('%H:%M')
            conflict_to = conflict_end.strftime('%H:%M')
            conflict_info = (
                f'{conflict_date_str} с {conflict_from} до {conflict_to}'
            )
        else:
            conflict_info = 'указанное время'

        conflict_car = f' ({conflict.car_model})' if conflict else ''
        post_label = (
            POST_NAMES.get(draft.post_code, str(draft.post_code))
            if draft.post_code
            else 'Пост'
        )

        await message.answer(
            text=(
                f'{post_label} занят {conflict_info}{conflict_car}. '
                'Выберите вариант:'
            ),
            reply_markup=get_post_conflict_kb(
                posts=check_result.available_posts,
                public_id=draft.draft_id,
            ),
        )
        return

    await state.update_data({'draft': draft.model_dump()})
    await state.set_state(BookingState.waiting_for_confirmation)

    await message.answer(
        text=draft.format_telegram_card(),
        reply_markup=get_confirmation_kb(public_id=draft.draft_id),
    )


@router.callback_query(SundayChoiceAction.filter())
async def handle_sunday_decision(
    callback: CallbackQuery,
    callback_data: SundayChoiceAction,
    state: FSMContext,
    booking_service: BookingService,
    session: AsyncSession,
) -> None:
    """Обрабатывает выбор действия при записи на воскресенье по BR-002.

    Args:
        callback: Запрос обратного вызова Telegram.
        callback_data: Данные действия.
        state: Контекст FSM.
        booking_service: Сервис бронирования.
        session: Асинхронная сессия базы данных.
    """
    data = await state.get_data()
    if 'draft' not in data:
        await callback.answer('Черновик устарел.', show_alert=True)
        return

    draft = AppointmentDraft(**data['draft'])

    if callback_data.action == 'confirm_sunday':
        draft.is_sunday_confirmed = True
        await state.update_data({'draft': draft.model_dump()})
        if callback.message:
            await callback.message.edit_text(
                'Запись на воскресенье подтверждена мастером.',
            )
            await progress_appointment_draft(
                message=callback.message,
                state=state,
                draft=draft,
                booking_service=booking_service,
                session=session,
            )
        await callback.answer()
    elif callback_data.action == 'shift_monday':
        current_dt = draft.start_datetime or datetime.datetime.now()
        days_ahead = (7 - current_dt.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 1
        new_dt = current_dt + datetime.timedelta(days=days_ahead)
        draft.start_datetime = new_dt
        draft.is_sunday_confirmed = False
        await state.update_data({'draft': draft.model_dump()})
        if callback.message:
            await callback.message.edit_text(
                f'Дата записи перенесена на понедельник ({new_dt.strftime("%d.%m.%Y")}).',
            )
            await progress_appointment_draft(
                message=callback.message,
                state=state,
                draft=draft,
                booking_service=booking_service,
                session=session,
            )
        await callback.answer()
    else:
        await state.clear()
        if callback.message:
            await callback.message.edit_text('Создание записи отменено.')
        await callback.answer('Отменено.')


@router.callback_query(OvertimeChoiceAction.filter())
async def handle_overtime_decision(
    callback: CallbackQuery,
    callback_data: OvertimeChoiceAction,
    state: FSMContext,
    booking_service: BookingService,
    session: AsyncSession,
) -> None:
    """Обрабатывает решение по сверхурочной записи по BR-010.

    Args:
        callback: Запрос обратного вызова Telegram.
        callback_data: Данные действия.
        state: Контекст FSM.
        booking_service: Сервис бронирования.
        session: Асинхронная сессия базы данных.
    """
    data = await state.get_data()
    if 'draft' not in data:
        await callback.answer('Черновик устарел.', show_alert=True)
        return

    draft = AppointmentDraft(**data['draft'])

    if callback_data.action == 'confirm_overtime':
        draft.is_overtime_confirmed = True
        await state.update_data({'draft': draft.model_dump()})
        if callback.message:
            await callback.message.edit_text(
                'Сверхурочная работа подтверждена.',
            )
            await progress_appointment_draft(
                message=callback.message,
                state=state,
                draft=draft,
                booking_service=booking_service,
                session=session,
            )
        await callback.answer()
    elif callback_data.action == 'shift_tomorrow':
        if draft.start_datetime:
            draft.start_datetime += datetime.timedelta(days=1)
        draft.is_overtime_confirmed = False
        await state.update_data({'draft': draft.model_dump()})
        if callback.message:
            await callback.message.edit_text('Запись сдвинута на следующий день.')
            await progress_appointment_draft(
                message=callback.message,
                state=state,
                draft=draft,
                booking_service=booking_service,
                session=session,
            )
        await callback.answer()
    elif callback_data.action == 'change_time':
        await state.set_state(BookingState.waiting_for_new_time)
        if callback.message:
            await callback.message.answer(
                text='Введите другое время записи (например: 14:00):',
                reply_markup=get_cancel_only_kb(draft.draft_id),
            )
        await callback.answer()
    else:
        await state.clear()
        if callback.message:
            await callback.message.edit_text('Создание записи отменено.')
        await callback.answer('Отменено.')


@router.callback_query(MasterOverlapChoiceAction.filter())
async def handle_master_overlap_decision(
    callback: CallbackQuery,
    callback_data: MasterOverlapChoiceAction,
    state: FSMContext,
    booking_service: BookingService,
    session: AsyncSession,
) -> None:
    """Обрабатывает решение мастера о пересечении времени по BR-009.

    Args:
        callback: Запрос обратного вызова Telegram.
        callback_data: Данные действия.
        state: Контекст FSM.
        booking_service: Сервис бронирования.
        session: Асинхронная сессия базы данных.
    """
    data = await state.get_data()
    if 'draft' not in data:
        await callback.answer('Черновик устарел.', show_alert=True)
        return

    draft = AppointmentDraft(**data['draft'])

    if callback_data.action == 'confirm_anyway':
        draft.is_master_overlap_confirmed = True
        await state.update_data({'draft': draft.model_dump()})
        if callback.message:
            await callback.message.edit_text(
                'Параллельная занятость мастера подтверждена.',
            )
            await progress_appointment_draft(
                message=callback.message,
                state=state,
                draft=draft,
                booking_service=booking_service,
                session=session,
            )
        await callback.answer()
    elif callback_data.action == 'change_time':
        await state.set_state(BookingState.waiting_for_new_time)
        if callback.message:
            await callback.message.answer(
                text='Введите другое время записи (например: 15:30):',
                reply_markup=get_cancel_only_kb(draft.draft_id),
            )
        await callback.answer()
    else:
        await state.clear()
        if callback.message:
            await callback.message.edit_text('Создание записи отменено.')
        await callback.answer('Отменено.')


@router.callback_query(DraftMasterAction.filter())
async def handle_draft_master_selection(
    callback: CallbackQuery,
    callback_data: DraftMasterAction,
    state: FSMContext,
    booking_service: BookingService,
    session: AsyncSession,
) -> None:
    """Назначает выбранного мастера на создаваемый продавцом черновик.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        callback_data: Данные выбранного мастера.
        state: Контекст FSM с черновиком.
        booking_service: Сервис управления бронированием.
        session: Асинхронная сессия базы данных.
    """
    data = await state.get_data()
    if 'draft' not in data:
        await callback.answer(
            'Черновик устарел. Создайте запись заново.',
            show_alert=True,
        )
        return

    user_repo = UserRepository(session)
    selected_master = await user_repo.get_by_id(callback_data.master_id)
    if selected_master is None:
        await callback.answer('Мастер не найден.', show_alert=True)
        return

    draft = AppointmentDraft(**data['draft'])
    draft.master_id = selected_master.id
    draft.master_name = selected_master.full_name
    draft.master_telegram_id = selected_master.telegram_id

    await state.update_data({'draft': draft.model_dump()})

    if callback.message:
        await callback.message.edit_text(
            text=f'Ответственный мастер назначен: <b>{selected_master.full_name}</b>.',
        )
        await progress_appointment_draft(
            message=callback.message,
            state=state,
            draft=draft,
            booking_service=booking_service,
            session=session,
        )
    await callback.answer()


@router.callback_query(BookingAction.filter(F.action == 'confirm'))
async def confirm_booking(
    callback: CallbackQuery,
    state: FSMContext,
    current_user: User,
    booking_service: BookingService,
) -> None:
    """Подтверждает бронь и сохраняет её в системе и календаре.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        state: Контекст FSM с данными черновика.
        current_user: Авторизованный сотрудник.
        booking_service: Экземпляр сервиса управления бронированием.
    """
    data = await state.get_data()
    if 'draft' not in data:
        await callback.answer(
            'Черновик устарел. Создайте запись заново.',
            show_alert=True,
        )
        return

    draft = AppointmentDraft(**data['draft'])

    try:
        created = await booking_service.confirm_and_create(
            draft=draft,
            user_telegram_id=current_user.telegram_id,
        )
        if callback.message:
            await callback.message.edit_text(
                text=(
                    f'Запись <b>[{created.public_id}] ({created.car_model})</b> успешно '
                    'подтверждена и внесена в график цеха.'
                ),
            )
        await state.clear()
        await callback.answer('Запись создана.')
    except BookingError as exc:
        escaped_error = html.escape(str(exc))
        if callback.message:
            await callback.message.answer(
                text=(
                    '<b>Сбой при сохранении в Google Календарь:</b>\n'
                    f'<code>{escaped_error}</code>\n\n'
                    'Запись не подтверждена. Проверьте права доступа '
                    'сервисного аккаунта к календарю и нажмите кнопку '
                    '«Подтвердить» повторно.'
                ),
            )
        await callback.answer(
            text='Ошибка синхронизации с Google Календарём.',
            show_alert=True,
        )


@router.callback_query(BookingAction.filter(F.action == 'edit'))
async def edit_booking(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    """Переводит бота в состояние ожидания ручных правок.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        state: Контекст FSM.
    """
    await state.set_state(BookingState.waiting_for_edit)
    if callback.message:
        await callback.message.answer(
            text=(
                'Напишите или надиктуйте голосом, что требуется изменить '
                '(например: <i>«Машина Лада Веста, время на 14:00»</i> '
                'или <i>«Длительность 2 часа»</i>):'
            ),
        )
    await callback.answer()


@router.callback_query(BookingAction.filter(F.action == 'change_time'))
async def handle_change_time_action(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    """Запрашивает у мастера новое время для записи при занятом посте.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        state: Контекст FSM.
    """
    await state.set_state(BookingState.waiting_for_new_time)
    data = await state.get_data()
    draft_dict = data.get('draft', {})
    draft_id = draft_dict.get('draft_id', '')

    if callback.message:
        await callback.message.answer(
            text=(
                'На какое время перенести запись? Напишите или надиктуйте '
                'голосом (Шаг записи — 30 минут):'
            ),
            reply_markup=get_cancel_only_kb(draft_id),
        )
    await callback.answer()


@router.callback_query(BookingAction.filter(F.action == 'cancel'))
async def cancel_booking(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    """Отменяет текущий процесс создания или редактирования бронирования.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        state: Контекст FSM.
    """
    await state.clear()
    if callback.message:
        await callback.message.edit_text(
            text='Создание записи отменено.',
        )
    await callback.answer('Черновик удален.')


@router.callback_query(PostAction.filter())
async def handle_post_selection(
    callback: CallbackQuery,
    callback_data: PostAction,
    state: FSMContext,
    booking_service: BookingService,
    session: AsyncSession,
) -> None:
    """Назначает выбранный пост и переводит черновик на валидацию.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        callback_data: Данные выбранного рабочего поста.
        state: Контекст FSM.
        booking_service: Сервис бронирования.
        session: Асинхронная сессия базы данных.
    """
    data = await state.get_data()
    if 'draft' not in data:
        await callback.answer(
            'Черновик устарел. Создайте запись заново.',
            show_alert=True,
        )
        return

    draft = AppointmentDraft(**data['draft'])
    draft.post_code = PostCode(callback_data.post_code)
    await state.update_data({'draft': draft.model_dump()})

    if callback.message:
        await callback.message.edit_text(
            text=f'Выбран пост: <b>{POST_NAMES.get(draft.post_code, str(draft.post_code))}</b>.',
        )
        await progress_appointment_draft(
            message=callback.message,
            state=state,
            draft=draft,
            booking_service=booking_service,
            session=session,
        )
    await callback.answer()


@router.message(BookingState.waiting_for_missing_field, F.text | F.voice)
async def process_missing_field_input(
    message: Message,
    bot: Bot,
    state: FSMContext,
    ai_service: AIService,
    booking_service: BookingService,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Обрабатывает ввод недостающего обязательного поля со сбросом при отмене.

    Args:
        message: Сообщение с недостающими данными.
        bot: Клиент Telegram Bot API.
        state: Контекст FSM.
        ai_service: Сервис искусственного интеллекта.
        booking_service: Сервис бронирования.
        current_user: Авторизованный сотрудник.
        session: Асинхронная сессия базы данных.
    """
    draft, raw_text = await _load_active_draft_or_handle_cancel(
        message=message,
        bot=bot,
        state=state,
        ai_service=ai_service,
    )
    if draft is None or raw_text is None:
        return

    data = await state.get_data()
    missing_field = data.get('missing_field')

    if missing_field == 'client_phone':
        draft.client_phone = raw_text
    elif missing_field == 'car_model':
        draft.car_model = raw_text
    elif missing_field == 'work_description':
        draft.work_description = raw_text
    elif missing_field == 'start_datetime':
        target_time_str, target_date_str = await _resolve_time_and_date(
            raw_text=raw_text,
            ai_service=ai_service,
        )
        if not target_time_str:
            await message.answer(
                text=(
                    'Не удалось определить время. Укажите, например: 14:00 '
                    '(или нажмите Отменить):'
                ),
                reply_markup=get_cancel_only_kb(draft.draft_id),
            )
            return

        timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
        current_date = datetime.datetime.now(timezone).date()
        if not await _apply_parsed_datetime(
            message=message,
            draft=draft,
            target_time_str=target_time_str,
            target_date_str=target_date_str,
            fallback_date=current_date,
        ):
            return

    await progress_appointment_draft(
        message=message,
        state=state,
        draft=draft,
        booking_service=booking_service,
        current_user=current_user,
        session=session,
    )


@router.message(BookingState.waiting_for_new_time, F.text | F.voice)
async def process_new_time_input(
    message: Message,
    bot: Bot,
    state: FSMContext,
    ai_service: AIService,
    booking_service: BookingService,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Применяет новое время к текущему черновику записи с поддержкой отмены.

    Args:
        message: Сообщение с новым временем.
        bot: Клиент Telegram Bot API.
        state: Контекст FSM.
        ai_service: Сервис искусственного интеллекта.
        booking_service: Сервис бронирования.
        current_user: Авторизованный сотрудник.
        session: Асинхронная сессия базы данных.
    """
    draft, raw_text = await _load_active_draft_or_handle_cancel(
        message=message,
        bot=bot,
        state=state,
        ai_service=ai_service,
    )
    if draft is None or raw_text is None:
        return

    target_time_str, target_date_str = await _resolve_time_and_date(
        raw_text=raw_text,
        ai_service=ai_service,
    )
    if not target_time_str:
        await message.answer(
            text=(
                'Не удалось распознать время. Укажите, например: 11:30 '
                '(или нажмите Отменить):'
            ),
            reply_markup=get_cancel_only_kb(draft.draft_id),
        )
        return

    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    fallback_date = (
        draft.start_datetime.date()
        if draft.start_datetime
        else datetime.datetime.now(timezone).date()
    )
    if not await _apply_parsed_datetime(
        message=message,
        draft=draft,
        target_time_str=target_time_str,
        target_date_str=target_date_str,
        fallback_date=fallback_date,
    ):
        return

    await progress_appointment_draft(
        message=message,
        state=state,
        draft=draft,
        booking_service=booking_service,
        current_user=current_user,
        session=session,
    )


@router.message(BookingState.waiting_for_edit, F.text | F.voice)
async def process_manual_edit(
    message: Message,
    bot: Bot,
    state: FSMContext,
    ai_service: AIService,
    booking_service: BookingService,
    current_user: User,
    session: AsyncSession,
) -> None:
    """Применяет текстовые или голосовые правки мастера к черновику.

    Args:
        message: Сообщение с исправленными данными.
        bot: Клиент Telegram Bot API.
        state: Контекст FSM.
        ai_service: Сервис искусственного интеллекта.
        booking_service: Сервис бронирования.
        current_user: Авторизованный сотрудник.
        session: Асинхронная сессия базы данных.
    """
    draft, raw_text = await _load_active_draft_or_handle_cancel(
        message=message,
        bot=bot,
        state=state,
        ai_service=ai_service,
        cancel_message='Редактирование черновика отменено.',
    )
    if draft is None or raw_text is None:
        return

    try:
        extraction = await ai_service.extract_appointment(raw_text=raw_text)
        if extraction.car_model:
            draft.car_model = extraction.car_model
        if extraction.client_phone:
            draft.client_phone = extraction.client_phone
        if extraction.client_name:
            draft.client_name = extraction.client_name
        if extraction.license_plate:
            draft.license_plate = extraction.license_plate
        if extraction.vin:
            draft.vin = extraction.vin
        if extraction.work_description:
            draft.work_description = extraction.work_description
        if extraction.work_items:
            draft.work_items = extraction.work_items
        if extraction.suggested_duration_minutes:
            draft.planned_duration_minutes = (
                extraction.suggested_duration_minutes
            )
        if extraction.post_code:
            draft.post_code = extraction.post_code

        fast_time = _parse_time_fast(raw_text)
        chosen_time = extraction.start_time or fast_time

        if extraction.start_date and chosen_time:
            timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
            parsed_dt = datetime.datetime.strptime(
                f'{extraction.start_date} {chosen_time}',
                '%Y-%m-%d %H:%M',
            ).replace(tzinfo=timezone)
            draft.start_datetime = parsed_dt
        elif chosen_time and draft.start_datetime:
            timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
            current_date_str = draft.start_datetime.date().strftime('%Y-%m-%d')
            parsed_dt = datetime.datetime.strptime(
                f'{current_date_str} {chosen_time}',
                '%Y-%m-%d %H:%M',
            ).replace(tzinfo=timezone)
            draft.start_datetime = parsed_dt
    except (AIServiceError, ValueError):
        draft.work_description = raw_text

    await progress_appointment_draft(
        message=message,
        state=state,
        draft=draft,
        booking_service=booking_service,
        current_user=current_user,
        session=session,
    )
