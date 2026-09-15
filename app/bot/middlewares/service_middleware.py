"""Мидлварь для внедрения сервисов в контекст обработчиков."""

from collections.abc import Awaitable
from collections.abc import Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ServiceMiddleware(BaseMiddleware):
    """Внедряет сервисы бизнес-логики в словарь данных (data)."""

    def __init__(self, **services: Any) -> None:
        self.services = services

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data.update(self.services)
        return await handler(event, data)
