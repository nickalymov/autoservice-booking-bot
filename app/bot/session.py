"""Модуль отказоустойчивой HTTP-сессии для Telegram Bot API.

Реализует механизм автоматических повторных попыток при сетевых сбоях,
таймаутах и разрывах соединений с серверами api.telegram.org.
"""

import asyncio
import logging
from typing import Any

from aiohttp import ClientError
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramNetworkError
from aiogram.methods.base import TelegramMethod
from aiogram.methods.base import TelegramType

logger = logging.getLogger('bot_session')

_MAX_RETRIES: int = 3
_BACKOFF_SECONDS: float = 1.0


class ResilientAiohttpSession(AiohttpSession):
    """HTTP-сессия с защитой от разрывов TCP-соединений с Telegram."""

    async def make_request(
        self,
        bot: Any,
        method: TelegramMethod[TelegramType],
        timeout: int | None = None,
    ) -> TelegramType:
        """Отправляет запрос к Bot API с повтором при сетевых ошибках.

        Args:
            bot: Экземпляр бота.
            method: Метод Telegram Bot API.
            timeout: Лимит времени на выполнение запроса.

        Returns:
            Результат ответа Telegram Bot API.

        Raises:
            TelegramNetworkError: Если все попытки подключения исчерпаны.
        """
        last_exception: Exception | None = None

        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                return await super().make_request(
                    bot=bot,
                    method=method,
                    timeout=timeout,
                )
            except (TelegramNetworkError, ClientError, TimeoutError) as exc:
                last_exception = exc
                if attempt == _MAX_RETRIES:
                    logger.error(
                        'Не удалось соединиться с Telegram API после %d попыток: %s',
                        _MAX_RETRIES,
                        exc,
                    )
                    raise

                delay = _BACKOFF_SECONDS * attempt
                logger.warning(
                    'Разрыв соединения с api.telegram.org (попытка %d/%d). '
                    'Повторная отправка через %.1f сек...',
                    attempt,
                    _MAX_RETRIES,
                    delay,
                )
                await asyncio.sleep(delay)

        raise TelegramNetworkError(
            method=method,
            message=f'Сетевой сбой Telegram API: {last_exception}',
        )
