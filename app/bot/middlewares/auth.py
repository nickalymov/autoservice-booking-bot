"""Модуль мидлвари авторизации и проверки доступа.

Обеспечивает перехват входящих запросов Telegram, проверку наличия
и активности пользователя в белом списке и внедрение текущего пользователя.
"""

from collections.abc import Awaitable
from collections.abc import Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.types import TelegramObject
from aiogram.types import Update
from aiogram.types import User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database.repositories import UserRepository


class AuthMiddleware(BaseMiddleware):
    """Мидлварь для проверки авторизации и белого списка Telegram ID."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """Перехватывает событие, проверяет права и передает управление.

        Args:
            handler: Следующий обработчик в цепочке выполнения.
            event: Входящий объект Telegram (Update, Message, CallbackQuery).
            data: Словарь контекста события.

        Returns:
            Результат выполнения хэндлера или прерывание при отказе в доступе.
        """
        telegram_user: TelegramUser | None = data.get('event_from_user')
        if telegram_user is None:
            telegram_user = getattr(event, 'from_user', None)

        if telegram_user is None:
            return await handler(event, data)

        session: AsyncSession | None = data.get('session')
        if session is None:
            return await handler(event, data)

        settings = get_settings()
        user_repo = UserRepository(session)
        await user_repo.ensure_whitelist_users(
            settings.whitelist_admin_ids,
        )
        db_user = await user_repo.get_by_telegram_id(telegram_user.id)

        if db_user is None or not db_user.is_active:
            access_error_text = (
                'Доступ ограничен. Обратитесь к администратору.'
            )
            target_event = event
            if isinstance(event, Update):
                target_event = event.message or event.callback_query

            if isinstance(target_event, Message):
                await target_event.answer(text=access_error_text)
            elif isinstance(target_event, CallbackQuery):
                await target_event.answer(
                    text=access_error_text,
                    show_alert=True,
                )
            return None

        data['current_user'] = db_user
        return await handler(event, data)
