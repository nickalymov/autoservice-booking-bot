"""Точка входа для запуска Telegram-бота автосервиса.

Модуль выполняет инициализацию базы данных, сервисов бизнес-логики,
интеграции с Google Календарём, настройку цепочки мидлварей, регистрацию
роутеров обработчиков и запуск цикла опроса обновлений Telegram Bot API.
"""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.bot.handlers import booking
from app.bot.handlers import common
from app.bot.handlers import management
from app.bot.handlers import schedule
from app.bot.handlers import voice
from app.bot.middlewares.auth import AuthMiddleware
from app.bot.middlewares.db import DbSessionMiddleware
from app.bot.middlewares.service_middleware import ServiceMiddleware
from app.bot.session import ResilientAiohttpSession
from app.config import get_settings
from app.core.booking_service import BookingService
from app.core.diagnostics import SystemDiagnostics
from app.database.repositories import PostRepository
from app.database.repositories import UserRepository
from app.database.session import close_database
from app.database.session import create_engine_and_sessionmaker
from app.database.session import init_database
from app.services.ai_service import AIService
from app.services.calendar_service import CalendarServiceError
from app.services.calendar_service import GoogleCalendarService
from app.services.scheduler_service import SchedulerService


async def _init_system_data(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Инициализирует справочные данные базы данных при запуске.

    Args:
        session_factory: Фабрика сессий базы данных SQLAlchemy.
    """
    async with session_factory() as session:
        post_repo = PostRepository(session)
        user_repo = UserRepository(session)
        await post_repo.ensure_default_posts()
        await user_repo.ensure_default_staff()
        await session.commit()


async def main() -> None:
    """Инициализирует и запускает все подсистемы бота и фоновые службы."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )

    settings = get_settings()
    engine, session_factory = create_engine_and_sessionmaker(settings)

    await init_database(engine)
    await _init_system_data(session_factory)

    calendar_service: GoogleCalendarService | None = None
    try:
        calendar_service = GoogleCalendarService(settings)
        logging.info('Интеграция с Google Календарём инициализирована.')
    except CalendarServiceError as exc:
        logging.warning(
            'Google Календарь отключен. Работа в локальном режиме: %s',
            exc,
        )

    session = ResilientAiohttpSession(
        proxy=settings.telegram_proxy,
    )
    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    booking_service = BookingService(
        session_factory=session_factory,
        calendar_service=calendar_service,
    )
    ai_service = AIService(settings)
    scheduler_service = SchedulerService(
        bot=bot,
        session_factory=session_factory,
        settings=settings,
    )

    diagnostics = SystemDiagnostics(
        bot=bot,
        session_factory=session_factory,
        ai_service=ai_service,
        settings=settings,
        calendar_service=calendar_service,
    )
    await diagnostics.run_startup_checks()

    dp.update.outer_middleware(DbSessionMiddleware(session_factory))
    dp.update.outer_middleware(AuthMiddleware())
    dp.update.outer_middleware(
        ServiceMiddleware(
            booking_service=booking_service,
            ai_service=ai_service,
        )
    )

    dp.include_router(common.router)
    dp.include_router(voice.router)
    dp.include_router(booking.router)
    dp.include_router(management.router)
    dp.include_router(schedule.router)

    await bot.set_my_commands([
        BotCommand(
            command='start',
            description='Главное меню и быстрая панель',
        ),
        BotCommand(
            command='summary',
            description='Вечерняя сводка загрузки сервиса',
        ),
        BotCommand(
            command='reminders',
            description='Включить или выключить напоминания',
        ),
        BotCommand(
            command='users',
            description='Управление персоналом и доступом',
        ),
    ])

    await scheduler_service.start()

    try:
        await dp.start_polling(bot)
    finally:
        await scheduler_service.stop()
        await close_database(engine)
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
