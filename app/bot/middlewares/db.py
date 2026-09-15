"""Модуль мидлвари управления сессиями базы данных.

Обеспечивает автоматическое создание, внедрение в контекст обработчиков
и безопасное завершение транзакций сессий SQLAlchemy на каждое событие.
"""

from collections.abc import Awaitable
from collections.abc import Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.database.session import get_async_session


class DbSessionMiddleware(BaseMiddleware):
    """Мидлварь управления жизненным циклом сессии базы данных.

    Открывает асинхронную сессию SQLAlchemy для каждого входящего
    события, внедряет ее в контекст данных и закрывает с фиксацией транзакции.

    Attributes:
        _session_factory: Фабрика создания асинхронных сессий базы данных.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        """Инициализирует мидлварь заданной фабрикой сессий.

        Args:
            session_factory: Фабрика асинхронных сессий SQLAlchemy.
        """
        self._session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """Внедряет асинхронную сессию в контекст и передает управление.

        Args:
            handler: Следующий обработчик в цепочке выполнения.
            event: Входящий объект события Telegram.
            data: Контекстный словарь данных события.

        Returns:
            Результат выполнения цепочки обработчиков.
        """
        async with get_async_session(self._session_factory) as session:
            data['session'] = session
            return await handler(event, data)
