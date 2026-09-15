"""Базовый модуль декларативных моделей базы данных.

Определяет корневой декларативный класс SQLAlchemy, соглашение
об именовании ограничений базы данных и миксин временных меток аудита.
"""

import datetime

from sqlalchemy import DateTime
from sqlalchemy import MetaData
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


NAMING_CONVENTION: dict[str, str] = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}


class Base(DeclarativeBase):
    """Базовый декларативный класс для всех моделей базы данных.

    Attributes:
        metadata: Метаданные с единым соглашением об именовании ограничений.
    """

    metadata = MetaData(naming_convention=NAMING_CONVENTION)

    def __repr__(self) -> str:
        """Формирует строковое представление экземпляра модели.

        Returns:
            Строка с именем класса и первичным идентификатором.
        """
        identifier = getattr(self, 'id', None)
        if identifier is not None:
            return f'<{self.__class__.__name__}(id={identifier!r})>'
        return f'<{self.__class__.__name__}>'


class TimestampMixin:
    """Миксин для добавления временных меток создания и изменения записи.

    Attributes:
        created_at: Дата и время первоначального создания записи в БД.
        updated_at: Дата и время последнего обновления записи в БД.
    """

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
