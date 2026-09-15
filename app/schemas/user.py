"""Модуль схем данных сотрудников и ролевой модели автосервиса.

Содержит Pydantic-модели для валидации реквизитов пользователей,
управления доступом, обновления профиля и инициализации белого списка.
"""

import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.config import UserRole


class UserBase(BaseModel):
    """Базовая схема данных сотрудника автосервиса.

    Attributes:
        telegram_id: Уникальный идентификатор пользователя в Telegram.
        full_name: Полное имя или отображаемый псевдоним.
        role: Системная роль сотрудника с набором прав доступа.
        is_active: Флаг активного статуса учетной записи.
        reminders_enabled: Флаг отправки напоминаний за 30 минут.
    """

    telegram_id: int = Field(
        description='Telegram ID сотрудника',
    )
    full_name: str = Field(
        min_length=1,
        max_length=128,
        description='Имя или псевдоним сотрудника',
    )
    role: UserRole = Field(
        default=UserRole.MECHANIC,
        description='Роль сотрудника в автосервисе',
    )
    is_active: bool = Field(
        default=True,
        description='Флаг активности учетной записи',
    )
    reminders_enabled: bool = Field(
        default=True,
        description='Флаг отправки напоминаний о записях',
    )


class UserCreate(UserBase):
    """Схема для создания нового сотрудника в системе."""


class UserUpdate(BaseModel):
    """Схема для частичного обновления данных сотрудника.

    Attributes:
        full_name: Новое имя или псевдоним сотрудника.
        role: Новая системная роль.
        is_active: Новый статус активности.
        reminders_enabled: Новый статус отправки напоминаний.
    """

    full_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=128,
        description='Новое имя сотрудника',
    )
    role: UserRole | None = Field(
        default=None,
        description='Новая роль в сервисе',
    )
    is_active: bool | None = Field(
        default=None,
        description='Новый флаг активности',
    )
    reminders_enabled: bool | None = Field(
        default=None,
        description='Новый флаг напоминаний',
    )


class UserRead(UserBase):
    """Схема чтения данных пользователя из базы данных.

    Attributes:
        id: Первичный ключ записи в базе данных.
        created_at: Дата и время регистрации пользователя.
        updated_at: Дата и время последнего обновления данных.
    """

    id: int = Field(
        description='Первичный ключ пользователя в БД',
    )
    created_at: datetime.datetime = Field(
        description='Дата и время создания записи',
    )
    updated_at: datetime.datetime = Field(
        description='Дата и время последнего изменения',
    )

    model_config = ConfigDict(from_attributes=True)


class WhitelistEntry(BaseModel):
    """Запись белого списка для начальной инициализации команды.

    Attributes:
        telegram_id: Идентификатор Telegram.
        full_name: Имя сотрудника (Вова, Коля, Рамазан и др.).
        role: Назначенная роль.
    """

    telegram_id: int = Field(
        description='Telegram ID сотрудника',
    )
    full_name: str = Field(
        description='Имя сотрудника',
    )
    role: UserRole = Field(
        default=UserRole.MECHANIC,
        description='Назначенная роль сотрудника',
    )


class WhitelistConfig(BaseModel):
    """Схема конфигурации белого списка доступа команды автосервиса.

    Attributes:
        users: Список предопределенных сотрудников сервиса.
    """

    users: list[WhitelistEntry] = Field(
        default_factory=list,
        description='Список сотрудников белого списка',
    )
