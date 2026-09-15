"""Корневой модуль общих фикстур тестового пакета.

Предоставляет переиспользуемые фикстуры базы данных, изоляции транзакций,
наполнения справочников и экземпляра сервиса бронирования.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import UserRole
from app.core.booking_service import BookingService
from app.database.models.base import Base
from app.database.repositories.post_repo import PostRepository
from app.database.repositories.user_repo import UserRepository


@pytest_asyncio.fixture
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Создает тестовый асинхронный движок SQLite в оперативной памяти.

    Yields:
        Экземпляр AsyncEngine для тестовой базы данных.
    """
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=False)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session_factory(
    test_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """Создает фабрику сессий для тестовой базы данных.

    Args:
        test_engine: Тестовый асинхронный движок БД.

    Returns:
        Фабрика сессий SQLAlchemy.
    """
    return async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


@pytest_asyncio.fixture
async def setup_test_data(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Заполняет тестовую базу данных базовыми постами и сотрудниками.

    Args:
        session_factory: Фабрика сессий БД.
    """
    async with session_factory() as session:
        post_repo = PostRepository(session)
        user_repo = UserRepository(session)

        await post_repo.ensure_default_posts()
        await user_repo.ensure_default_staff()

        await user_repo.create(
            telegram_id=101,
            full_name='Вова',
            role=UserRole.MECHANIC,
        )
        await user_repo.create(
            telegram_id=102,
            full_name='Коля',
            role=UserRole.MECHANIC,
        )
        await user_repo.create(
            telegram_id=201,
            full_name='Продавец Иван',
            role=UserRole.SALES,
        )
        await user_repo.create(
            telegram_id=301,
            full_name='Заказчик',
            role=UserRole.OWNER,
        )
        await session.commit()


@pytest_asyncio.fixture
async def booking_service(
    session_factory: async_sessionmaker[AsyncSession],
    setup_test_data: None,
) -> BookingService:
    """Инициализирует экземпляр сервиса бронирования.

    Args:
        session_factory: Фабрика сессий БД.
        setup_test_data: Фикстура предварительного наполнения БД.

    Returns:
        Сконфигурированный экземпляр BookingService.
    """
    del setup_test_data
    return BookingService(session_factory=session_factory)
