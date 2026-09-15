"""Модуль модели пользователя базы данных.

Определяет сущность сотрудника автосервиса, управление доступом,
ролевую модель и параметры персональных уведомлений.
"""

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.config import UserRole
from app.database.models.base import Base
from app.database.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.database.models.appointment import Appointment
    from app.database.models.history_log import HistoryLog


class User(Base, TimestampMixin):
    """Модель сотрудника автосервиса и прав доступа.

    Attributes:
        id: Первичный ключ учетной записи сотрудника.
        telegram_id: Уникальный идентификатор пользователя в Telegram.
        full_name: Полное имя или отображаемый псевдоним сотрудника.
        role: Системная роль с набором прав доступа.
        is_active: Флаг активного статуса учетной записи.
        reminders_enabled: Флаг отправки напоминаний за 30 минут.
        appointments: Список назначенных на мастера записей.
        history_logs: Журнал зафиксированных действий пользователя.
    """

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=False,
    )
    full_name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False, length=32),
        default=UserRole.MECHANIC,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    reminders_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    appointments: Mapped[list['Appointment']] = relationship(
        primaryjoin='User.id == Appointment.master_id',
        back_populates='master',
        cascade='all, delete-orphan',
    )
    history_logs: Mapped[list['HistoryLog']] = relationship(
        back_populates='user',
    )
