"""Модуль управления сессиями и подключениями к базе данных.

Обеспечивает создание асинхронного движка SQLAlchemy, фабрики сессий,
контекстное управление транзакциями и инициализацию таблиц.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
import contextlib

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import Settings
from app.config import get_settings
from app.database.models.base import Base


def create_engine_and_sessionmaker(
    settings: Settings | None = None,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """Создает асинхронный движок PostgreSQL и фабрику сессий.

    Args:
        settings: Экземпляр настроек приложения.

    Returns:
        Кортеж из настроенного асинхронного движка и фабрики сессий.
    """
    app_settings = settings or get_settings()
    engine = create_async_engine(
        app_settings.async_database_url,
        echo=app_settings.db_echo,
        pool_size=10,
        max_overflow=20,
    )
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    return engine, session_factory


async def init_database(engine: AsyncEngine) -> None:
    """Создает все таблицы базы данных при их отсутствии.

    Args:
        engine: Асинхронный движок SQLAlchemy для подключения к БД.
    """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def close_database(engine: AsyncEngine) -> None:
    """Корректно закрывает пул соединений с базой данных.

    Args:
        engine: Асинхронный движок SQLAlchemy для освобождения ресурсов.
    """
    await engine.dispose()


@contextlib.asynccontextmanager
async def get_async_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """Предоставляет асинхронную сессию с контролем транзакции.

    Args:
        session_factory: Фабрика создания асинхронных сессий.

    Yields:
        Активная асинхронная сессия SQLAlchemy.

    Raises:
        Exception: Любая ошибка выполнения транзакции для отката изменений.
    """
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
