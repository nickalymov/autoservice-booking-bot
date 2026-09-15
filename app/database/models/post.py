"""Модуль модели рабочего поста автосервиса.

Определяет сущность рабочего поста, физические и виртуальные мощности,
связку с Google Календарём и возможность закрепления мастера.
"""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.config import PostCode
from app.database.models.base import Base
from app.database.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.database.models.appointment import Appointment


class Post(Base, TimestampMixin):
    """Модель рабочего поста автосервиса.

    Attributes:
        id: Первичный ключ записи поста.
        code: Уникальный код поста (P1, P2, P3, P4, NO_POST).
        name: Наименование поста на русском языке.
        post_type: Физический тип поста (яма, подъемник и др.).
        description: Правила использования и допустимые работы.
        is_active: Флаг доступности поста для планирования.
        google_calendar_id: Идентификатор связанного Google-календаря.
        default_master_id: Внешний ключ закрепленного мастера.
        appointments: Список запланированных на данный пост записей.
        default_master: Объект закрепленного за постом мастера.
    """

    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    code: Mapped[PostCode] = mapped_column(
        Enum(PostCode, native_enum=False, length=16),
        unique=True,
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    post_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    google_calendar_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    default_master_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
    )

    appointments: Mapped[list['Appointment']] = relationship(
        back_populates='post',
    )
    default_master: Mapped['User | None'] = relationship()
