"""Модуль обработчиков интерактивных действий с черновиками записей.

Обеспечивает подтверждение нарядов, выбор свободных постов цеха,
ручное редактирование реквизитов текстом и голосом, дозапрос пропущенных
обязательных полей, а также отмену.
"""

from __future__ import annotations

import datetime
import html
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
from app.bot.keyboards.inline import PostAction
from app.bot.keyboards.inline import get_confirmation_kb
from app.bot.keyboards.inline import get_draft_master_selector_kb
from app.bot.keyboards.inline import get_post_conflict_kb
from app.bot.keyboards.inline import get_post_selector_kb
from app.bot.states.booking_states import BookingState
from app.config import POST_NAMES
from app.config import TIMEZONE_NAME
from app.config import PostCode
from app.config import UserRole
from app.core.booking_service import BookingError
from app.core.booking_service import BookingService
from app.database.models import User
from app.database.repositories import UserRepository
from app.schemas.appointment import AppointmentDraft
from app.services.ai_service import AIService
from app.services.ai_service import AIServiceError

router = Router()


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
        await message.answer('Укажите марку и модель автомобиля:')
        return

    if draft.start_datetime is None:
        await state.set_data({
            'draft': draft.model_dump(),
            'missing_field': 'start_datetime',
        })
        await state.set_state(BookingState.waiting_for_missing_field)
        await message.answer(
            'Во сколько записать? Шаг записи — 30 минут (например: на 10:00):'
        )
        return

    if not draft.client_phone:
        await state.set_data({
            'draft': draft.model_dump(),
            'missing_field': 'client_phone',
        })
        await state.set_state(BookingState.waiting_for_missing_field)
        await message.answer('Укажите номер телефона клиента для связи:')
        return

    if not draft.work_description and not draft.work_items:
        await state.set_data({
            'draft': draft.model_dump(),
            'missing_field': 'work_description',
        })
        await state.set_state(BookingState.waiting_for_missing_field)
        await message.answer('Укажите причину обращения или перечень работ:')
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

    duration = draft.planned_duration_minutes or 30
    end_dt = draft.start_datetime + datetime.timedelta(minutes=duration)
    check_result = await booking_service.check_slot(
        post_code=draft.post_code,
        start_dt=draft.start_datetime,
        end_dt=end_dt,
    )

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
        timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
        if conflict:
            conflict_start = conflict.start_datetime.astimezone(timezone)
            conflict_end = conflict.end_datetime.astimezone(timezone)
            conflict_from = conflict_start.strftime('%H:%M')
            conflict_to = conflict_end.strftime('%H:%M')
        else:
            conflict_from = '—'
            conflict_to = '—'

        conflict_car = f' ({conflict.car_model})' if conflict else ''
        post_label = (
            POST_NAMES.get(draft.post_code, str(draft.post_code))
            if draft.post_code
            else 'Пост'
        )

        await message.answer(
            text=(
                f'{post_label} занят с {conflict_from} '
                f'до {conflict_to}{conflict_car}. Выберите вариант:'
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
        callback: Входящий запрос обратного вызова.
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
                    f'Запись <b>{created.public_id}</b> успешно '
                    f'подтверждена и внесена в график цеха.'
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
    if callback.message:
        await callback.message.answer(
            text=(
                'На какое время перенести запись? Напишите или надиктуйте '
                'голосом (Шаг записи — 30 минут):'
            ),
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
) -> None:
    """Назначает выбранный пост и переводит черновик на подтверждение.

    Args:
        callback: Входящий запрос обратного вызова Telegram.
        callback_data: Данные выбранного рабочего поста.
        state: Контекст FSM.
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

    if draft.is_ready_for_confirmation():
        await state.set_state(BookingState.waiting_for_confirmation)
        if callback.message:
            await callback.message.edit_text(
                text=draft.format_telegram_card(),
                reply_markup=get_confirmation_kb(public_id=draft.draft_id),
            )
    else:
        missing = ', '.join(draft.missing_required_fields())
        if callback.message:
            await callback.message.edit_text(
                text=(
                    f'Пост выбран: {draft.post_code}.\n'
                    f'Не заполнено: {missing}'
                ),
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
    """Обрабатывает ввод недостающего обязательного поля по п. 10.2 ТЗ.

    Args:
        message: Сообщение с недостающими данными.
        bot: Клиент Telegram Bot API.
        state: Контекст FSM.
        ai_service: Сервис искусственного интеллекта.
        booking_service: Сервис бронирования.
        current_user: Авторизованный сотрудник.
        session: Асинхронная сессия базы данных.
    """
    draft, raw_text = await _load_draft_and_extract_text(
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
        try:
            extraction = await ai_service.extract_appointment(raw_text=raw_text)
            if extraction.start_time:
                timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
                current_date = datetime.datetime.now(timezone).date()
                target_date_str = (
                    extraction.start_date or current_date.strftime('%Y-%m-%d')
                )
                parsed_dt = datetime.datetime.strptime(
                    f'{target_date_str} {extraction.start_time}',
                    '%Y-%m-%d %H:%M',
                ).replace(tzinfo=timezone)
                draft.start_datetime = parsed_dt
        except (AIServiceError, ValueError):
            await message.answer(
                'Не удалось определить время. Укажите, например: 10:00',
            )
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
    """Применяет новое время к текущему черновику записи из текста или голоса.

    Args:
        message: Сообщение с новым временем.
        bot: Клиент Telegram Bot API.
        state: Контекст FSM.
        ai_service: Сервис искусственного интеллекта.
        booking_service: Сервис бронирования.
        current_user: Авторизованный сотрудник.
        session: Асинхронная сессия базы данных.
    """
    draft, raw_text = await _load_draft_and_extract_text(
        message=message,
        bot=bot,
        state=state,
        ai_service=ai_service,
    )
    if draft is None or raw_text is None:
        return

    try:
        extraction = await ai_service.extract_appointment(raw_text=raw_text)
        if extraction.start_time:
            timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
            current_date = (
                draft.start_datetime.date()
                if draft.start_datetime
                else datetime.datetime.now(timezone).date()
            )
            target_date_str = extraction.start_date or current_date.strftime(
                '%Y-%m-%d'
            )
            parsed_dt = datetime.datetime.strptime(
                f'{target_date_str} {extraction.start_time}',
                '%Y-%m-%d %H:%M',
            ).replace(tzinfo=timezone)
            draft.start_datetime = parsed_dt
    except (AIServiceError, ValueError):
        await message.answer(
            'Не удалось распознать время. Укажите, например: 11:30',
        )
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
    draft, raw_text = await _load_draft_and_extract_text(
        message=message,
        bot=bot,
        state=state,
        ai_service=ai_service,
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
        if extraction.start_date and extraction.start_time:
            timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
            parsed_dt = datetime.datetime.strptime(
                f'{extraction.start_date} {extraction.start_time}',
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
