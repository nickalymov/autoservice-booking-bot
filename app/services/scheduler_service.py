"""Модуль сервиса фонового планировщика уведомлений.

Обеспечивает периодическую проверку предстоящих записей на ремонт
и отправку напоминаний мастерам за 30 минут до начала обслуживания.
"""

import datetime
import zoneinfo

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import TIMEZONE_NAME
from app.config import Settings
from app.config import get_settings
from app.database.models import HistoryActionType
from app.database.repositories import AppointmentRepository
from app.database.repositories import HistoryLogRepository
from app.database.session import get_async_session


class SchedulerService:
    """Сервис планировщика для отправки автоматических напоминаний.

    Attributes:
        _bot: Экземпляр бота aiogram для отправки сообщений.
        _session_factory: Фабрика сессий базы данных.
        _settings: Настройки приложения.
        _scheduler: Асинхронный планировщик задач APScheduler.
    """

    def __init__(
        self,
        bot: Bot,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings | None = None,
    ) -> None:
        """Инициализирует планировщик с ботом и фабрикой сессий.

        Args:
            bot: Экземпляр бота aiogram.
            session_factory: Фабрика создания сессий SQLAlchemy.
            settings: Экземпляр настроек приложения.
        """
        self._bot = bot
        self._session_factory = session_factory
        self._settings = settings or get_settings()
        timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
        self._scheduler = AsyncIOScheduler(timezone=timezone)

    async def start(self) -> None:
        """Запускает фоновый планировщик и регистрирует задачу проверки."""
        self._scheduler.add_job(
            self._check_upcoming_appointments,
            trigger='interval',
            seconds=60,
            id='appointment_reminders_job',
            replace_existing=True,
        )
        self._scheduler.start()

    async def stop(self) -> None:
        """Корректно останавливает фоновый планировщик."""
        if self._scheduler.running:
            self._scheduler.shutdown()

    async def _check_upcoming_appointments(self) -> None:
        """Проверяет предстоящие записи и отправляет напоминания мастерам."""
        timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
        now_dt = datetime.datetime.now(timezone)
        window_start = now_dt + datetime.timedelta(minutes=25)
        window_end = now_dt + datetime.timedelta(minutes=35)

        async with get_async_session(self._session_factory) as session:
            appt_repo = AppointmentRepository(session)
            history_repo = HistoryLogRepository(session)

            upcoming_appts = await appt_repo.get_upcoming_for_reminders(
                window_start=window_start,
                window_end=window_end,
            )

            for appointment in upcoming_appts:
                logs = await history_repo.get_by_appointment_id(
                    appointment.id,
                )
                already_reminded = any(
                    log.action_type == HistoryActionType.UPDATED
                    and log.field_name == 'reminder_sent'
                    for log in logs
                )
                if already_reminded:
                    continue

                master = appointment.master
                if master is None or not master.telegram_id:
                    continue

                post_label = (
                    f'{appointment.post.code} — {appointment.post.name}'
                    if appointment.post
                    else 'Без поста'
                )
                start_msk = appointment.start_datetime.astimezone(timezone)
                end_msk = appointment.end_datetime.astimezone(timezone)
                start_time_str = start_msk.strftime('%H:%M')
                end_time_str = end_msk.strftime('%H:%M')

                message_text = (
                    f'Через 30 минут: {appointment.car_model}, '
                    f'{post_label}, план {start_time_str}–{end_time_str}'
                )

                try:
                    await self._bot.send_message(
                        chat_id=master.telegram_id,
                        text=message_text,
                    )
                    await history_repo.log_action(
                        appointment_id=appointment.id,
                        action_type=HistoryActionType.UPDATED,
                        user_id=master.id,
                        field_name='reminder_sent',
                        old_value='False',
                        new_value='True',
                        comment='Отправлено напоминание за 30 минут',
                    )
                except TelegramAPIError:
                    pass
