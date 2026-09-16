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

from app.database.repositories import UserRepository


def extract_telegram_user_title(user: TelegramUser) -> str:
    """Формирует отображаемое имя по правилу: Имя Фамилия -> @username -> ID.

    Args:
        user: Экземпляр пользователя Telegram.

    Returns:
        Строка с именем и фамилией, никнеймом или идентификатором.
    """
    name_parts = [user.first_name, user.last_name]
    full_name = ' '.join(part for part in name_parts if part).strip()
    if full_name:
        return full_name
    if user.username:
        return f'@{user.username}'
    return str(user.id)


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
            event: Входящий объект Telegram.
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

        user_repo = UserRepository(session)
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
        data['telegram_user_title'] = extract_telegram_user_title(
            telegram_user,
        )
        return await handler(event, data)
