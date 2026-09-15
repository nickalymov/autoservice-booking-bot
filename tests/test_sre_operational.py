"""Модуль автоматизированного тестирования SRE и эксплуатационной готовности.

Проверяет работу фонового планировщика напоминаний, дедупликацию уведомлений
мастерам и логику ранней самодиагностики системы (SystemDiagnostics).
"""

from __future__ import annotations

import datetime
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
import zoneinfo

from aiogram import Bot
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import PostCode
from app.config import Settings
from app.config import TIMEZONE_NAME
from app.core.booking_service import BookingService
from app.core.diagnostics import SystemDiagnostics
from app.database.models.history_log import HistoryActionType
from app.database.models.history_log import HistoryLog
from app.schemas.appointment import AppointmentDraft
from app.schemas.appointment import AppointmentSource
from app.services.ai_service import AIService
from app.services.calendar_service import GoogleCalendarService
from app.services.scheduler_service import SchedulerService


@pytest.mark.asyncio
async def test_scheduler_reminders_delivery_and_deduplication(
    booking_service: BookingService,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Проверяет отправку напоминания за 30 минут и защиту от повторного спама.

    Args:
        booking_service: Экземпляр сервиса управления бронированием.
        session_factory: Фабрика асинхронных сессий базы данных.
    """
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    now_dt = datetime.datetime.now(timezone)
    appointment_start = now_dt + datetime.timedelta(minutes=30)

    draft = AppointmentDraft(
        draft_id='SRE-REM-01',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.VOICE,
        car_model='Kia Cerato',
        client_phone='+79998881122',
        work_description='Замена масла',
        work_items=['Масло'],
        start_datetime=appointment_start,
        planned_duration_minutes=60,
        post_code=PostCode.P1,
    )
    created = await booking_service.confirm_and_create(
        draft=draft,
        user_telegram_id=101,
    )

    mock_bot = MagicMock(spec=Bot)
    mock_bot.send_message = AsyncMock()

    scheduler = SchedulerService(
        bot=mock_bot,
        session_factory=session_factory,
    )

    await scheduler._check_upcoming_appointments()

    mock_bot.send_message.assert_called_once()
    sent_args = mock_bot.send_message.call_args[1]
    assert sent_args['chat_id'] == 101
    assert 'Kia Cerato' in sent_args['text']
    assert 'Через 30 минут' in sent_args['text']

    async with session_factory() as session:
        stmt = select(HistoryLog).where(
            HistoryLog.appointment_id == created.id,
            HistoryLog.action_type == HistoryActionType.UPDATED,
            HistoryLog.field_name == 'reminder_sent',
        )
        log_entry = await session.scalar(stmt)
        assert log_entry is not None
        assert log_entry.new_value == 'True'

    await scheduler._check_upcoming_appointments()
    assert mock_bot.send_message.call_count == 1


@pytest.mark.asyncio
async def test_system_diagnostics_all_systems_healthy(
    session_factory: async_sessionmaker[AsyncSession],
    setup_test_data: None,
) -> None:
    """Проверяет успешное прохождение всех проверок самодиагностики при старте.

    Args:
        session_factory: Фабрика асинхронных сессий базы данных.
        setup_test_data: Фикстура наполнения базовых данных.
    """
    del setup_test_data
    mock_bot = MagicMock(spec=Bot)
    mock_bot.get_me = AsyncMock(
        return_value=MagicMock(username='autoservice_bot', id=777),
    )

    mock_ai = MagicMock(spec=AIService)
    mock_ai.client = MagicMock()
    mock_ai.client.models = MagicMock()
    mock_ai.client.models.list = AsyncMock(
        return_value=MagicMock(data=[1, 2, 3]),
    )

    mock_cal = MagicMock(spec=GoogleCalendarService)
    mock_cal.service_account_email = 'service@serviceaccount.com'
    mock_cal.verify_calendars_access = AsyncMock(
        return_value={'P1': None, 'P2': None, 'Обзорный': None},
    )

    diagnostics = SystemDiagnostics(
        bot=mock_bot,
        session_factory=session_factory,
        ai_service=mock_ai,
        settings=Settings(),
        calendar_service=mock_cal,
    )

    await diagnostics.run_startup_checks()


@pytest.mark.asyncio
async def test_system_diagnostics_fails_fast_on_database_down() -> None:
    """Проверяет аварийную остановку бота при недоступности базы данных."""
    mock_bot = MagicMock(spec=Bot)
    mock_bot.get_me = AsyncMock(
        return_value=MagicMock(username='autoservice_bot', id=777),
    )

    faulty_session_factory = MagicMock()
    faulty_session_factory.side_effect = ConnectionRefusedError(
        'PostgreSQL connection refused',
    )

    mock_ai = MagicMock(spec=AIService)
    mock_ai.client = MagicMock()
    mock_ai.client.models = MagicMock()
    mock_ai.client.models.list = AsyncMock(return_value=MagicMock(data=[1]))

    diagnostics = SystemDiagnostics(
        bot=mock_bot,
        session_factory=faulty_session_factory,
        ai_service=mock_ai,
        settings=Settings(),
        calendar_service=None,
    )

    with pytest.raises(RuntimeError) as exc_info:
        await diagnostics.run_startup_checks()

    assert 'Критический сбой самодиагностики' in str(exc_info.value)
