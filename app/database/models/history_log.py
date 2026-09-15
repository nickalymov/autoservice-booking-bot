"""Модуль модели журнала аудита и истории изменений записей.

Определяет сущность фиксации действий пользователей и системы над заявками,
включая создание, изменение реквизитов, передачу и смену статусов.
"""

import datetime
import enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.models.base import Base

if TYPE_CHECKING:
    from app.database.models.appointment import Appointment


class HistoryActionType(str, enum.Enum):
    """Типы действий над записью на ремонт в журнале аудита."""

    CREATED = 'CREATED'
    UPDATED = 'UPDATED'
    STATUS_CHANGED = 'STATUS_CHANGED'
    TRANSFER_REQUESTED = 'TRANSFER_REQUESTED'
    TRANSFER_ACCEPTED = 'TRANSFER_ACCEPTED'
    TRANSFER_REJECTED = 'TRANSFER_REJECTED'
    EARLY_COMPLETED = 'EARLY_COMPLETED'
    CANCELLED = 'CANCELLED'


ACTION_TYPE_NAMES: dict[HistoryActionType, str] = {
    HistoryActionType.CREATED: 'Создание',
    HistoryActionType.UPDATED: 'Изменение реквизитов',
    HistoryActionType.STATUS_CHANGED: 'Смена статуса',
    HistoryActionType.TRANSFER_REQUESTED: 'Запрос передачи',
    HistoryActionType.TRANSFER_ACCEPTED: 'Принятие передачи',
    HistoryActionType.TRANSFER_REJECTED: 'Отклонение передачи',
    HistoryActionType.EARLY_COMPLETED: 'Досрочное завершение',
    HistoryActionType.CANCELLED: 'Отмена',
}


class HistoryLog(Base):
    """Модель записи журнала аудита действий над заявкой.

    Attributes:
        id: Первичный ключ записи журнала аудита.
        appointment_id: Внешний ключ связанной записи на ремонт.
        user_id: Внешний ключ пользователя, выполнившего действие.
        action_type: Категория совершенного действия.
        field_name: Наименование изменившегося реквизита или параметра.
        old_value: Значение параметра до изменения.
        new_value: Значение параметра после изменения.
        comment: Текстовый комментарий или детализация действия.
        created_at: Дата и время фиксации события в системе.
        appointment: Связанный объект заявки на ремонт.
        user: Связанный объект пользователя, выполнившего действие.
    """

    __tablename__ = 'history_logs'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    appointment_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('appointments.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey('users.id', ondelete='SET NULL'),
        index=True,
        nullable=True,
    )
    action_type: Mapped[HistoryActionType] = mapped_column(
        Enum(HistoryActionType, native_enum=False, length=32),
        nullable=False,
    )
    field_name: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )
    old_value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    new_value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    appointment: Mapped['Appointment'] = relationship(
        back_populates='history_logs',
    )
    user: Mapped['User | None'] = relationship(
        back_populates='history_logs',
    )
