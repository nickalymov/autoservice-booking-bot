"""Модуль модульных и интеграционных тестов бизнес-правил автосервиса.

Проверяет контроль коллизий по постам, логику слотов без поста,
кратность шагу 30 минут, ролевую модель RBAC, управление сотрудниками,
перенос и неявку клиентов.
"""

from __future__ import annotations

import datetime
import zoneinfo

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import PostCode
from app.config import TIMEZONE_NAME
from app.config import UserRole
from app.core.booking_service import BookingError
from app.core.booking_service import BookingService
from app.core.booking_service import PermissionDeniedError
from app.core.booking_service import SlotConflictError
from app.core.duration_estimator import estimate_duration_minutes
from app.core.permissions import can_force_modify
from app.core.permissions import can_manage_appointment
from app.core.permissions import can_manage_users
from app.core.permissions import can_transfer_appointment
from app.database.models.appointment import Appointment
from app.database.models.user import User
from app.database.repositories.user_repo import UserRepository
from app.schemas.appointment import AppointmentDraft
from app.schemas.appointment import AppointmentSource
from app.schemas.appointment import AppointmentStatus


def test_duration_estimator_norms() -> None:
    """Проверяет соблюдение нормативной базы времени и кратность 30 минутам."""
    assert estimate_duration_minutes(
        work_description='замена стоек стабилизатора',
    ) == 90

    assert estimate_duration_minutes(
        work_description='замена тормозных колодок',
    ) == 60

    assert estimate_duration_minutes(
        work_description='замена масла и масляного фильтра',
    ) == 30

    assert estimate_duration_minutes(
        work_description='замена комплекта ГРМ и сцепления',
    ) == 180

    assert estimate_duration_minutes(
        work_description='какой-то нестандартный звук',
    ) == 60


@pytest.mark.asyncio
async def test_user_management_by_owner(
    session_factory: async_sessionmaker[AsyncSession],
    setup_test_data: None,
) -> None:
    """Проверяет регистрацию мастера и смену активности владельцем."""
    del setup_test_data
    async with session_factory() as session:
        user_repo = UserRepository(session)
        ramazan = await user_repo.upsert_user(
            telegram_id=103,
            full_name='Рамазан',
            role=UserRole.MECHANIC,
        )
        assert ramazan.id is not None
        assert ramazan.full_name == 'Рамазан'

        toggled = await user_repo.toggle_active(telegram_id=103)
        assert toggled is not None
        assert toggled.is_active is False


@pytest.mark.asyncio
async def test_sales_booking_assigns_mechanic(
    booking_service: BookingService,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Проверяет назначение мастера при создании записи продавцом магазина."""
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    start_time = datetime.datetime(2026, 9, 15, 10, 0, tzinfo=timezone)

    async with session_factory() as session:
        user_repo = UserRepository(session)
        vova = await user_repo.get_by_telegram_id(101)
        assert vova is not None

    draft = AppointmentDraft(
        draft_id='SALES-01',
        master_telegram_id=101,
        master_name='Вова',
        master_id=vova.id,
        source=AppointmentSource.TEXT,
        car_model='Nissan Qashqai',
        client_phone='+79289998877',
        work_description='Замена масла',
        work_items=['Масло'],
        start_datetime=start_time,
        planned_duration_minutes=30,
        post_code=PostCode.P2,
    )

    created = await booking_service.confirm_and_create(
        draft=draft,
        user_telegram_id=201,
    )
    assert created.master_id == vova.id
    assert created.created_by_user_id != vova.id


@pytest.mark.asyncio
async def test_sunday_is_off_validation(
    booking_service: BookingService,
) -> None:
    """Проверяет запрет записи на воскресенье согласно п. 5 ТЗ."""
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    sunday_dt = datetime.datetime(2026, 9, 20, 10, 0, tzinfo=timezone)

    draft = AppointmentDraft(
        draft_id='TEST-SUN',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.VOICE,
        car_model='Kia Rio',
        client_phone='+79281234567',
        work_description='Замена масла',
        work_items=['Масло'],
        start_datetime=sunday_dt,
        planned_duration_minutes=60,
        post_code=PostCode.P1,
    )

    with pytest.raises(BookingError) as exc_info:
        await booking_service.confirm_and_create(
            draft=draft,
            user_telegram_id=101,
        )
    assert 'Воскресенье' in str(exc_info.value)


@pytest.mark.asyncio
async def test_reschedule_flow(
    booking_service: BookingService,
) -> None:
    """Проверяет перенос записи на новый временной слот и пост (п. 10.4 ТЗ)."""
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    start_time = datetime.datetime(2026, 9, 15, 10, 0, tzinfo=timezone)

    draft = AppointmentDraft(
        draft_id='RESCH-01',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.TEXT,
        car_model='Kia Rio',
        client_phone='+79281234567',
        work_description='Замена стоек',
        work_items=['Замена стоек'],
        start_datetime=start_time,
        planned_duration_minutes=90,
        post_code=PostCode.P3,
    )
    created = await booking_service.confirm_and_create(
        draft=draft,
        user_telegram_id=101,
    )
    assert created.source == AppointmentSource.TEXT

    new_time = datetime.datetime(2026, 9, 15, 12, 0, tzinfo=timezone)
    rescheduled = await booking_service.reschedule_appointment(
        public_id=created.public_id,
        new_start_dt=new_time,
        new_post_code=PostCode.P2,
        user_telegram_id=101,
    )

    assert rescheduled.start_datetime == new_time
    assert rescheduled.post is not None
    assert rescheduled.post.code == PostCode.P2


@pytest.mark.asyncio
async def test_mark_no_show_flow(
    booking_service: BookingService,
) -> None:
    """Проверяет смену статуса на NO_SHOW при неявке клиента (п. 10.8 ТЗ)."""
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    start_time = datetime.datetime(2026, 9, 15, 10, 0, tzinfo=timezone)

    draft = AppointmentDraft(
        draft_id='NOSHOW-01',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.VOICE,
        car_model='Lada Granta',
        client_phone='+79281234567',
        work_description='Замена свечей',
        work_items=['Свечи'],
        start_datetime=start_time,
        planned_duration_minutes=30,
        post_code=PostCode.P1,
    )
    created = await booking_service.confirm_and_create(
        draft=draft,
        user_telegram_id=101,
    )

    updated = await booking_service.mark_no_show(
        public_id=created.public_id,
        user_telegram_id=101,
    )
    assert updated.status == AppointmentStatus.NO_SHOW

    check_free = await booking_service.check_slot(
        post_code=PostCode.P1,
        start_dt=start_time,
        end_dt=start_time + datetime.timedelta(minutes=30),
    )
    assert check_free.is_available is True


@pytest.mark.asyncio
async def test_post_collisions_and_adjacent_slots(
    booking_service: BookingService,
) -> None:
    """Проверяет недопустимость пересечений на одном посту."""
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    start_time = datetime.datetime(2026, 9, 15, 10, 0, tzinfo=timezone)

    draft = AppointmentDraft(
        draft_id='TEST-001',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.VOICE,
        car_model='Kia Rio',
        client_phone='+79281234567',
        work_description='Замена стоек',
        work_items=['Замена стоек'],
        start_datetime=start_time,
        planned_duration_minutes=90,
        post_code=PostCode.P1,
    )

    created = await booking_service.confirm_and_create(
        draft=draft,
        user_telegram_id=101,
    )
    assert created.id is not None

    overlap_start = datetime.datetime(2026, 9, 15, 10, 30, tzinfo=timezone)
    overlap_end = datetime.datetime(2026, 9, 15, 11, 0, tzinfo=timezone)
    check_result = await booking_service.check_slot(
        post_code=PostCode.P1,
        start_dt=overlap_start,
        end_dt=overlap_end,
    )
    assert check_result.is_available is False
    assert check_result.conflicting_appointment is not None

    overlap_draft = AppointmentDraft(
        draft_id='TEST-002',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.VOICE,
        car_model='Lada Vesta',
        client_phone='+79287654321',
        work_description='Диагностика',
        work_items=['Диагностика'],
        start_datetime=overlap_start,
        planned_duration_minutes=30,
        post_code=PostCode.P1,
    )
    with pytest.raises(SlotConflictError):
        await booking_service.confirm_and_create(
            draft=overlap_draft,
            user_telegram_id=101,
        )

    adjacent_start = datetime.datetime(2026, 9, 15, 11, 30, tzinfo=timezone)
    adjacent_end = datetime.datetime(2026, 9, 15, 12, 30, tzinfo=timezone)
    adjacent_check = await booking_service.check_slot(
        post_code=PostCode.P1,
        start_dt=adjacent_start,
        end_dt=adjacent_end,
    )
    assert adjacent_check.is_available is True

    parallel_check = await booking_service.check_slot(
        post_code=PostCode.P2,
        start_dt=start_time,
        end_dt=datetime.datetime(2026, 9, 15, 11, 30, tzinfo=timezone),
    )
    assert parallel_check.is_available is True


@pytest.mark.asyncio
async def test_no_post_overlap_allowed(
    booking_service: BookingService,
) -> None:
    """Проверяет правило параллельной записи на виртуальный пост «Без поста»."""
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    start_time = datetime.datetime(2026, 9, 15, 14, 0, tzinfo=timezone)

    draft1 = AppointmentDraft(
        draft_id='NO-POST-1',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.VOICE,
        car_model='Lada Granta',
        client_phone='+79281112233',
        work_description='Замена лампочек',
        work_items=['Лампы'],
        start_datetime=start_time,
        planned_duration_minutes=30,
        post_code=PostCode.NO_POST,
    )
    created1 = await booking_service.confirm_and_create(
        draft=draft1,
        user_telegram_id=101,
    )
    assert created1.id is not None

    draft2 = AppointmentDraft(
        draft_id='NO-POST-2',
        master_telegram_id=102,
        master_name='Коля',
        source=AppointmentSource.TEXT,
        car_model='Hyundai Solaris',
        client_phone='+79284445566',
        work_description='Долив антифриза',
        work_items=['Антифриз'],
        start_datetime=start_time,
        planned_duration_minutes=30,
        post_code=PostCode.NO_POST,
    )
    created2 = await booking_service.confirm_and_create(
        draft=draft2,
        user_telegram_id=102,
    )
    assert created2.id is not None


@pytest.mark.asyncio
async def test_appointment_transfer_flow(
    booking_service: BookingService,
) -> None:
    """Проверяет двухэтапный сценарий успешной передачи заявки."""
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    start_time = datetime.datetime(2026, 9, 16, 12, 0, tzinfo=timezone)

    draft = AppointmentDraft(
        draft_id='TRANS-01',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.VOICE,
        car_model='Renault Duster',
        client_phone='+79998887766',
        work_description='Замена колодок',
        work_items=['Колодки'],
        start_datetime=start_time,
        planned_duration_minutes=60,
        post_code=PostCode.P2,
    )
    created = await booking_service.confirm_and_create(
        draft=draft,
        user_telegram_id=101,
    )

    requested = await booking_service.request_transfer(
        public_id=created.public_id,
        sender_telegram_id=101,
        target_master_telegram_id=102,
    )
    assert requested.status == AppointmentStatus.WAITING_TRANSFER

    accepted = await booking_service.accept_transfer(
        public_id=created.public_id,
        receiver_telegram_id=102,
    )
    assert accepted.status == AppointmentStatus.CONFIRMED
    assert accepted.master_id != created.master_id


def test_rbac_permissions() -> None:
    """Проверяет разграничение прав доступа по ролям."""
    master_vova = User(
        id=1,
        telegram_id=101,
        full_name='Вова',
        role=UserRole.MECHANIC,
        is_active=True,
    )
    master_kolya = User(
        id=2,
        telegram_id=102,
        full_name='Коля',
        role=UserRole.MECHANIC,
        is_active=True,
    )
    sales_user = User(
        id=3,
        telegram_id=201,
        full_name='Иван',
        role=UserRole.SALES,
        is_active=True,
    )
    owner_user = User(
        id=4,
        telegram_id=301,
        full_name='Заказчик',
        role=UserRole.OWNER,
        is_active=True,
    )

    vova_appointment = Appointment(
        id=10,
        public_id='B260915001',
        source=AppointmentSource.VOICE,
        master_id=1,
        created_by_user_id=1,
    )

    assert can_manage_appointment(master_vova, vova_appointment) is True
    assert can_manage_appointment(master_kolya, vova_appointment) is False
    assert can_manage_appointment(sales_user, vova_appointment) is True
    assert can_manage_appointment(owner_user, vova_appointment) is True

    assert can_transfer_appointment(master_vova, vova_appointment) is True
    assert can_transfer_appointment(master_kolya, vova_appointment) is False
    assert can_transfer_appointment(owner_user, vova_appointment) is True

    assert can_force_modify(sales_user) is True
    assert can_force_modify(owner_user) is True
    assert can_force_modify(master_vova) is False

    assert can_manage_users(owner_user) is True
    assert can_manage_users(sales_user) is False
    assert can_manage_users(master_vova) is False


@pytest.mark.asyncio
async def test_mechanic_cannot_manage_other_mechanic_appointment_in_service(
    booking_service: BookingService,
) -> None:
    """Проверяет блокировку изменения чужих нарядов мастером в сервисе."""
    timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
    start_time = datetime.datetime(2026, 9, 15, 10, 0, tzinfo=timezone)

    draft = AppointmentDraft(
        draft_id='RBAC-SVC-01',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.VOICE,
        car_model='Skoda Octavia',
        client_phone='+79281230000',
        work_description='Замена масла',
        work_items=['Масло'],
        start_datetime=start_time,
        planned_duration_minutes=30,
        post_code=PostCode.P1,
    )
    created = await booking_service.confirm_and_create(
        draft=draft,
        user_telegram_id=101,
    )

    with pytest.raises(PermissionDeniedError):
        await booking_service.start_appointment(
            public_id=created.public_id,
            user_telegram_id=102,
        )

    with pytest.raises(PermissionDeniedError):
        await booking_service.reschedule_appointment(
            public_id=created.public_id,
            new_start_dt=start_time + datetime.timedelta(hours=1),
            new_post_code=PostCode.P1,
            user_telegram_id=102,
        )

    with pytest.raises(PermissionDeniedError):
        await booking_service.mark_no_show(
            public_id=created.public_id,
            user_telegram_id=102,
        )

    with pytest.raises(PermissionDeniedError):
        await booking_service.complete_appointment(
            public_id=created.public_id,
            user_telegram_id=102,
        )

    with pytest.raises(PermissionDeniedError):
        await booking_service.cancel_appointment(
            public_id=created.public_id,
            user_telegram_id=102,
        )

    sales_updated = await booking_service.reschedule_appointment(
        public_id=created.public_id,
        new_start_dt=start_time + datetime.timedelta(hours=2),
        new_post_code=PostCode.P1,
        user_telegram_id=201,
    )
    assert sales_updated.start_datetime == (
        start_time + datetime.timedelta(hours=2)
    )

    owner_started = await booking_service.start_appointment(
        public_id=created.public_id,
        user_telegram_id=301,
    )
    assert owner_started.status == AppointmentStatus.IN_PROGRESS
