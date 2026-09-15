"""Модуль комплексной самодиагностики автосервиса при старте.

Выполняет проверку доступности базы данных, токена Telegram Bot API,
нейросетевого шлюза VseGPT и прав доступа к Google Календарям всех постов.
"""

import logging

from aiogram import Bot
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import Settings
from app.services.ai_service import AIService
from app.services.calendar_service import GoogleCalendarService

logger = logging.getLogger('diagnostics')


class SystemDiagnostics:
    """Подсистема валидации внешних подключений и сервисов."""

    def __init__(
        self,
        bot: Bot,
        session_factory: async_sessionmaker[AsyncSession],
        ai_service: AIService,
        settings: Settings,
        calendar_service: GoogleCalendarService | None = None,
    ) -> None:
        """Инициализирует модуль самодиагностики компонентами системы.

        Args:
            bot: Клиент Telegram Bot API.
            session_factory: Фабрика асинхронных сессий базы данных.
            ai_service: Сервис интеграции со шлюзом VseGPT.
            settings: Настройки приложения.
            calendar_service: Сервис интеграции с Google Календарём.
        """
        self._bot = bot
        self._session_factory = session_factory
        self._ai_service = ai_service
        self._settings = settings
        self._calendar_service = calendar_service

    async def check_database(self) -> bool:
        """Проверяет подключение к базе данных PostgreSQL.

        Returns:
            True при успешном подключении, иначе False.
        """
        try:
            async with self._session_factory() as session:
                await session.execute(text('SELECT 1'))
            logger.info('База данных PostgreSQL: соединение успешно.')
            return True
        except Exception as exc:
            logger.critical(
                'База данных PostgreSQL недоступна! Ошибка: %s',
                exc,
            )
            return False

    async def check_telegram(self) -> bool:
        """Проверяет валидность токена и доступ к Telegram Bot API.

        Returns:
            True при успешной авторизации бота, иначе False.
        """
        try:
            bot_user = await self._bot.get_me()
            logger.info(
                'Telegram Bot API: авторизован бот @%s (id=%d).',
                bot_user.username,
                bot_user.id,
            )
            return True
        except Exception as exc:
            logger.critical(
                'Ошибка авторизации Telegram-бота! Проверьте BOT_TOKEN: %s',
                exc,
            )
            return False

    async def check_vsegpt(self) -> bool:
        """Проверяет соединение с API VseGPT и валидность ключа.

        Returns:
            True при успешной проверке шлюза, иначе False.
        """
        try:
            models_response = await self._ai_service.client.models.list()
            models_count = len(models_response.data)
            logger.info(
                'Соединение успешно (доступно моделей: %d).',
                models_count,
            )
            return True
        except Exception as exc:
            logger.error(
                'Ошибка соединения с VseGPT! Проверьте VSEGPT_API_KEY: %s',
                exc,
            )
            return False

    async def check_google_calendar(self) -> bool:
        """Проверяет доступность каждого календаря поста Google API.

        Returns:
            True, если ко всем календарям есть доступ, иначе False.
        """
        if self._calendar_service is None:
            logger.warning(
                'Google Календарь не инициализирован (файл ключа отсутствует).',
            )
            return False

        logger.info(
            'Google Календарь: сервисный аккаунт %s. '
            'Проверка прав доступа к постам...',
            self._calendar_service.service_account_email,
        )

        access_results = (
            await self._calendar_service.verify_calendars_access()
        )
        has_errors = False

        for cal_name, error_text in access_results.items():
            if error_text is None:
                logger.info('• %s: доступ подтвержден.', cal_name)
            else:
                has_errors = True
                logger.error(
                    '• %s: ОШИБКА ДОСТУПА!\n  Причина: %s',
                    cal_name,
                    error_text,
                )

        if has_errors:
            logger.warning(
                'ВНИМАНИЕ! Для исправления ошибок Google Календаря:\n'
                '1. Откройте Google Календарь в браузере.\n'
                '2. Нажмите «Настройки и общий доступ» проблемного календаря.\n'
                '3. В разделе «Доступ для отдельных пользователей» добавьте '
                'email сервисного аккаунта: %s\n'
                '4. Установите право: «Внесение изменений в мероприятия».',
                self._calendar_service.service_account_email,
            )
            return False

        logger.info('Все календари Google успешно прошли валидацию.')
        return True

    async def run_startup_checks(self) -> None:
        """Выполняет полный цикл самодиагностики системы перед запуском."""
        logger.info('Запуск процедуры комплексной самодиагностики системы...')

        db_ok = await self.check_database()
        tg_ok = await self.check_telegram()
        vsegpt_ok = await self.check_vsegpt()
        calendar_ok = await self.check_google_calendar()

        status_text = (
            f'\n{"="*60}\n'
            f'ИТОГ САМОДИАГНОСТИКИ СИСТЕМЫ ПРИ СТАРТЕ:\n'
            f'• База данных PostgreSQL: {"РАБОТАЕТ" if db_ok else "СБОЙ"}\n'
            f'• Telegram Bot API:       {"РАБОТАЕТ" if tg_ok else "СБОЙ"}\n'
            f'• Шлюз ИИ (VseGPT):       {"РАБОТАЕТ" if vsegpt_ok else "СБОЙ"}\n'
            f'• Google Календари:       {"РАБОТАЮТ" if calendar_ok else "ТРЕБУЕТСЯ НАСТРОЙКА"}\n'
            f'{"="*60}'
        )
        logger.info(status_text)

        if not db_ok or not tg_ok:
            raise RuntimeError(
                'Критический сбой самодиагностики: запуск бота остановлен.',
            )
