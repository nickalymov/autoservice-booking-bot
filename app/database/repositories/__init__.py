"""Пакет репозиториев базы данных автосервиса.

Экспортирует классы для взаимодействия с таблицами пользователей,
рабочих постов, записей на обслуживание и журнала аудита действий.
"""

from app.database.repositories.appointment_repo import AppointmentRepository
from app.database.repositories.history_log_repo import HistoryLogRepository
from app.database.repositories.post_repo import PostRepository
from app.database.repositories.user_repo import UserRepository

__all__: tuple[str, ...] = (
    'AppointmentRepository',
    'HistoryLogRepository',
    'PostRepository',
    'UserRepository',
)
