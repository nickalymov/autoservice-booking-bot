"""Модуль стресс-тестирования состояния гонки и параллелизма бронирования.

Проверяет математическую невозможность овербукинга физических постов сервиса
при одновременном поступлении параллельных запросов на один и тот же слот.
"""

from __future__ import annotations

import asyncio
import datetime
import zoneinfo

import pytest
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import PostCode
from app.config import TIMEZONE_NAME
from app.core.booking_service import BookingService
from app.core.booking_service import SlotConflictError
from app.database.models.appointment import Appointment
from app.schemas.appointment import AppointmentDraft
from app.schemas.appointment import AppointmentSource


@pytest.mark.asyncio
async def test_concurrent_booking_same_post_race_condition(
    booking_service: BookingService,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Проверяет недопустимость двойной записи при параллельных запросах.

    Args:
        booking_service: Сервис бизнес-логики управления бронированием.
        session_factory: Фабрика сессий тестовой базы данных.
    """
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    start_time = datetime.datetime(2026, 9, 16, 10, 0, tzinfo=timezone)

    async def attempt_booking(index: int) -> Appointment:
        draft = AppointmentDraft(
            draft_id=f'RACE-{index}',
            master_telegram_id=101,
            master_name='Вова',
            source=AppointmentSource.TEXT,
            car_model=f'Car-{index}',
            client_phone=f'+7928111000{index}',
            work_description='Замена масла',
            work_items=['Масло'],
            start_datetime=start_time,
            planned_duration_minutes=60,
            post_code=PostCode.P2,
        )
        return await booking_service.confirm_and_create(
            draft=draft,
            user_telegram_id=101,
        )

    tasks = [attempt_booking(i) for i in range(5)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    success_results: list[Appointment] = []
    conflict_errors: list[SlotConflictError] = []
    other_errors: list[Exception] = []

    for result in results:
        if isinstance(result, Appointment):
            success_results.append(result)
        elif isinstance(result, SlotConflictError):
            conflict_errors.append(result)
        elif isinstance(result, Exception):
            other_errors.append(result)

    assert not other_errors
    assert len(success_results) == 1
    assert len(conflict_errors) == 4

    async with session_factory() as session:
        query = select(func.count()).select_from(Appointment)
        total_created = await session.scalar(query)
        assert total_created == 1


@pytest.mark.asyncio
async def test_concurrent_booking_different_posts(
    booking_service: BookingService,
) -> None:
    """Проверяет параллельное создание записей на разные посты в одно время.

    Args:
        booking_service: Сервис бизнес-логики управления бронированием.
    """
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    start_time = datetime.datetime(2026, 9, 16, 11, 0, tzinfo=timezone)

    draft_p1 = AppointmentDraft(
        draft_id='DIFF-P1',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.TEXT,
        car_model='Lada Vesta',
        client_phone='+79281234501',
        work_description='Осмотр на яме',
        work_items=['Осмотр'],
        start_datetime=start_time,
        planned_duration_minutes=60,
        post_code=PostCode.P1,
    )

    draft_p2 = AppointmentDraft(
        draft_id='DIFF-P2',
        master_telegram_id=102,
        master_name='Коля',
        source=AppointmentSource.VOICE,
        car_model='Kia Sportage',
        client_phone='+79281234502',
        work_description='Замена колодок',
        work_items=['Колодки'],
        start_datetime=start_time,
        planned_duration_minutes=60,
        post_code=PostCode.P2,
    )

    results = await asyncio.gather(
        booking_service.confirm_and_create(draft_p1, user_telegram_id=101),
        booking_service.confirm_and_create(draft_p2, user_telegram_id=102),
        return_exceptions=True,
    )

    assert not any(isinstance(res, Exception) for res in results)
    assert len(results) == 2
    assert results[0].post is not None
    assert results[0].post.code == PostCode.P1
    assert results[1].post is not None
    assert results[1].post.code == PostCode.P2


@pytest.mark.asyncio
async def test_concurrent_no_post_bookings(
    booking_service: BookingService,
) -> None:
    """Проверяет параллельное создание записей без поста без взаимных блокировок.

    Args:
        booking_service: Сервис бизнес-логики управления бронированием.
    """
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    start_time = datetime.datetime(2026, 9, 16, 14, 0, tzinfo=timezone)

    drafts = [
        AppointmentDraft(
            draft_id=f'NOPOST-PAR-{i}',
            master_telegram_id=101,
            master_name='Вова',
            source=AppointmentSource.TEXT,
            car_model=f'Car-Quick-{i}',
            client_phone=f'+7928999000{i}',
            work_description='Замена лампочки',
            work_items=['Лампа'],
            start_datetime=start_time,
            planned_duration_minutes=30,
            post_code=PostCode.NO_POST,
        )
        for i in range(3)
    ]

    tasks = [
        booking_service.confirm_and_create(draft, user_telegram_id=101)
        for draft in drafts
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    assert not any(isinstance(res, Exception) for res in results)
    assert len(results) == 3
