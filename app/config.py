"""Модуль конфигурации приложения автосервиса.

Содержит константы предметной области, перечисления постов и ролей,
а также валидацию переменных окружения через Pydantic Settings.
"""

from __future__ import annotations

import enum
import functools
import pathlib

from pydantic import Field
from pydantic import SecretStr
from pydantic import computed_field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

TIMEZONE_NAME: str = 'Europe/Moscow'
SCHEDULE_STEP_MINUTES: int = 30
WORK_DAY_START_HOUR: int = 9
WORK_DAY_END_HOUR: int = 20


class PostCode(str, enum.Enum):
    """Коды рабочих постов автосервиса."""

    P1 = 'P1'
    P2 = 'P2'
    P3 = 'P3'
    P4 = 'P4'
    NO_POST = 'NO_POST'


class UserRole(str, enum.Enum):
    """Роли пользователей автосервиса с разграничением прав."""

    OWNER = 'OWNER'
    MECHANIC = 'MECHANIC'
    SALES = 'SALES'


POST_NAMES: dict[PostCode, str] = {
    PostCode.P1: 'Пост 1 (Обычная яма)',
    PostCode.P2: 'Пост 2 (Подъемник 1)',
    PostCode.P3: 'Пост 3 (Подъемник 2)',
    PostCode.P4: 'Пост 4 (Яма / сход-развал)',
    PostCode.NO_POST: 'Без поста',
}


class Settings(BaseSettings):
    """Основные настройки конфигурации приложения.

    Attributes:
        bot_token: Токен Telegram-бота.
        telegram_proxy: Опциональный URL прокси для подключения к Telegram.
        whitelist_admin_ids: Список идентификаторов Telegram с доступом.
        vsegpt_api_key: Ключ доступа к сервису VseGPT.
        vsegpt_base_url: Базовый адрес API VseGPT.
        vsegpt_chat_model: Модель для текстового анализа и извлечения данных.
        vsegpt_stt_model: Модель для транскрибации речи по старому эндпоинту.
        vsegpt_use_audioinput: Флаг распознавания речи через чат-эндпоинт VseGPT.
        vsegpt_audioinput_model: Мультимодальная модель для распознавания речи.
        deepgram_api_key: Резервный API-ключ Deepgram.
        deepgram_base_url: Адрес эндпоинта Deepgram API.
        deepgram_model: Модель распознавания речи Deepgram.
        groq_api_key: Резервный API-ключ Groq при наличии прокси.
        groq_base_url: Базовый адрес API Groq.
        groq_stt_model: Модель Whisper на инфраструктуре Groq.
        db_host: Хост сервера базы данных PostgreSQL.
        db_port: Порт сервера базы данных PostgreSQL.
        db_user: Имя пользователя базы данных.
        db_password: Пароль пользователя базы данных.
        db_name: Название базы данных.
        db_echo: Флаг вывода SQL-запросов в журнал.
        google_credentials_path: Путь к JSON-файлу сервисного аккаунта.
        google_calendar_p1_id: Идентификатор календаря поста P1.
        google_calendar_p2_id: Идентификатор календаря поста P2.
        google_calendar_p3_id: Идентификатор календаря поста P3.
        google_calendar_p4_id: Идентификатор календаря поста P4.
        google_calendar_overview_id: Идентификатор календаря для записей без поста.
    """

    bot_token: SecretStr = Field(
        default=SecretStr(''),
        description='Токен Telegram-бота',
    )
    telegram_proxy: str | None = Field(
        default=None,
        description='Прокси для Telegram',
    )
    whitelist_admin_ids: list[int] = Field(
        default_factory=lambda: [426497153, 393014603],
        description='Белый список Telegram ID сотрудников',
    )

    vsegpt_api_key: SecretStr = Field(
        default=SecretStr(''),
        description='API-ключ для шлюза VseGPT',
    )
    vsegpt_base_url: str = Field(
        default='https://api.vsegpt.ru/v1',
        description='Базовый URL эндпоинта VseGPT',
    )
    vsegpt_chat_model: str = Field(
        default='openai/gpt-4o-mini',
        description='Идентификатор модели LLM для извлечения данных',
    )
    vsegpt_stt_model: str = Field(
        default='stt-openai/whisper-1',
        description='Идентификатор модели для транскрибации речи в VseGPT',
    )
    vsegpt_use_audioinput: bool = Field(
        default=True,
        description='Использовать мультимодальный Chat API VseGPT для распознавания',
    )
    vsegpt_audioinput_model: str = Field(
        default='google/gemini-3.1-flash-lite',
        description='Мультимодальная модель для распознавания речи в VseGPT',
    )

    deepgram_api_key: SecretStr | None = Field(
        default=None,
        description='API-ключ для распознавания речи через Deepgram',
    )
    deepgram_base_url: str = Field(
        default='https://api.deepgram.com/v1/listen',
        description='Базовый URL эндпоинта Deepgram STT API',
    )
    deepgram_model: str = Field(
        default='nova-2',
        description='Модель распознавания речи Deepgram',
    )

    groq_api_key: SecretStr | None = Field(
        default=None,
        description='API-ключ для скоростной транскрибации речи Groq',
    )
    groq_base_url: str = Field(
        default='https://api.groq.com/openai/v1',
        description='Базовый URL эндпоинта Groq API',
    )
    groq_stt_model: str = Field(
        default='whisper-large-v3-turbo',
        description='Модель транскрибации Whisper на мощностях Groq',
    )

    db_host: str = Field(
        default='localhost',
        description='Хост PostgreSQL',
    )
    db_port: int = Field(
        default=5432,
        description='Порт PostgreSQL',
    )
    db_user: str = Field(
        default='postgres',
        description='Пользователь PostgreSQL',
    )
    db_password: SecretStr = Field(
        default=SecretStr('postgres'),
        description='Пароль PostgreSQL',
    )
    db_name: str = Field(
        default='autoservice_db',
        description='Имя базы данных PostgreSQL',
    )
    db_echo: bool = Field(
        default=False,
        description='Логирование SQL-запросов',
    )

    google_credentials_path: pathlib.Path = Field(
        default=pathlib.Path('credentials.json'),
        description='Путь к ключу сервисного аккаунта Google',
    )
    google_calendar_p1_id: str | None = Field(
        default=None,
        description='ID Google-календаря для поста P1',
    )
    google_calendar_p2_id: str | None = Field(
        default=None,
        description='ID Google-календаря для поста P2',
    )
    google_calendar_p3_id: str | None = Field(
        default=None,
        description='ID Google-календаря для поста P3',
    )
    google_calendar_p4_id: str | None = Field(
        default=None,
        description='ID Google-календаря для поста P4',
    )
    google_calendar_overview_id: str | None = Field(
        default=None,
        description='ID Google-календаря для записей без поста',
    )

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @computed_field
    @property
    def async_database_url(self) -> str:
        """Формирует строку подключения к PostgreSQL для asyncpg."""
        password = self.db_password.get_secret_value()
        return (
            f'postgresql+asyncpg://{self.db_user}:{password}'
            f'@{self.db_host}:{self.db_port}/{self.db_name}'
        )


@functools.lru_cache
def get_settings() -> Settings:
    """Возвращает кэшированный экземпляр конфигурации приложения."""
    return Settings()
