"""Модуль стресс-тестирования отказоустойчивости и изоляции внешних сбоев.

Проверяет корректность отката транзакций базы данных при сбоях Google Calendar,
каскадное переключение моделей Whisper при таймаутах и повторные попытки
при разрывах сетевых соединений с Telegram Bot API.
"""

from __future__ import annotations

import datetime
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
import zoneinfo

from aiogram.exceptions import TelegramNetworkError
from aiogram.methods import GetMe
from openai import OpenAIError
import pytest
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.bot.session import ResilientAiohttpSession
from app.config import PostCode
from app.config import Settings
from app.config import TIMEZONE_NAME
from app.core.booking_service import BookingError
from app.core.booking_service import BookingService
from app.database.models.appointment import Appointment
from app.schemas.appointment import AppointmentDraft
from app.schemas.appointment import AppointmentSource
from app.services.ai_service import AIService
from app.services.calendar_service import CalendarServiceError
from app.services.calendar_service import GoogleCalendarService


def _get_future_workday(
    days_ahead: int = 2,
    hour: int = 10,
    minute: int = 0,
) -> datetime.datetime:
    """Возвращает будущую дату рабочего дня для тестов надежности."""
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    now_dt = datetime.datetime.now(timezone)
    candidate_dt = now_dt + datetime.timedelta(days=days_ahead)
    while candidate_dt.weekday() == 6:
        candidate_dt += datetime.timedelta(days=1)
    return candidate_dt.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )


@pytest.mark.asyncio
async def test_google_calendar_failure_rolls_back_database(
    session_factory: async_sessionmaker[AsyncSession],
    setup_test_data: None,
) -> None:
    """Проверяет откат создания записи в базе данных при сбое календаря Google.

    Args:
        session_factory: Фабрика асинхронных сессий базы данных.
        setup_test_data: Фикстура наполнения базовых данных.
    """
    del setup_test_data
    mock_calendar_service = MagicMock(spec=GoogleCalendarService)
    mock_calendar_service.create_event = AsyncMock(
        side_effect=CalendarServiceError('503 Service Unavailable: Google API'),
    )

    booking_service = BookingService(
        session_factory=session_factory,
        calendar_service=mock_calendar_service,
    )

    start_time = _get_future_workday(days_ahead=2, hour=10, minute=0)

    draft = AppointmentDraft(
        draft_id='CHAOS-CAL-01',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.VOICE,
        car_model='Toyota Camry',
        client_phone='+79280001122',
        work_description='Диагностика подвески',
        work_items=['Диагностика'],
        start_datetime=start_time,
        planned_duration_minutes=60,
        post_code=PostCode.P2,
    )

    with pytest.raises(BookingError) as exc_info:
        await booking_service.confirm_and_create(
            draft=draft,
            user_telegram_id=101,
        )

    assert 'Google Календаре' in str(exc_info.value)

    async with session_factory() as session:
        query = select(func.count()).select_from(Appointment)
        total_appointments = await session.scalar(query)
        assert total_appointments == 0


@pytest.mark.asyncio
async def test_ai_service_cascades_to_fallback_on_stt_timeout() -> None:
    """Проверяет автоматический каскадный переход на резервную модель STT."""
    mock_settings = Settings()
    service = AIService(settings=mock_settings)

    mock_success_transcription = MagicMock()
    mock_success_transcription.text = 'Запиши Kia Rio на 14:00'

    call_count = 0

    async def mock_transcription_create(
        *_args: object,
        **_kwargs: object,
    ) -> MagicMock:
        _ = (_args, _kwargs)
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise OpenAIError('504 Gateway Timeout: provider is overloaded')
        return mock_success_transcription

    with patch.object(
        service.client.audio.transcriptions,
        'create',
        side_effect=mock_transcription_create,
    ):
        result_text = await service.transcribe_audio(
            audio_bytes=b'fake_voice_audio_bytes',
        )

        assert call_count == 2
        assert result_text == 'Запиши Kia Rio на 14:00'


@pytest.mark.asyncio
async def test_resilient_telegram_session_recovers_after_network_error() -> None:
    """Проверяет прозрачное восстановление HTTP-сессии при сетевых сбоях."""
    session = ResilientAiohttpSession()
    mock_bot = MagicMock()
    mock_method = GetMe()

    attempt_counter = 0

    async def faulty_make_request(
        *_args: object,
        **_kwargs: object,
    ) -> MagicMock:
        _ = (_args, _kwargs)
        nonlocal attempt_counter
        attempt_counter += 1
        if attempt_counter < 3:
            raise TelegramNetworkError(
                method=mock_method,
                message='Connection reset by peer',
            )
        return MagicMock(id=123456789, is_bot=True, username='test_bot')

    with patch(
        'aiogram.client.session.aiohttp.AiohttpSession.make_request',
        side_effect=faulty_make_request,
    ):
        with patch('asyncio.sleep', new_callable=AsyncMock):
            bot_user = await session.make_request(
                bot=mock_bot,
                method=mock_method,
            )
            assert attempt_counter == 3
            assert bot_user.username == 'test_bot'
