"""Модуль сервиса искусственного интеллекта автосервиса.

Обеспечивает асинхронную транскрибацию голосовых сообщений
с механизмом быстрого каскадного переключения моделей и извлечение
структурированных параметров записи через модели VseGPT.
"""

import asyncio
import datetime
import io
import logging
from typing import Any
from typing import cast
import zoneinfo

from openai import AsyncOpenAI
from openai import OpenAIError
from openai.types.chat import completion_create_params
from pydantic import ValidationError

from app.config import Settings
from app.config import TIMEZONE_NAME
from app.config import get_settings
from app.schemas.appointment import AppointmentExtraction

logger = logging.getLogger('ai_service')

_DEFAULT_STT_TIMEOUT_SECONDS: float = 25.0

_FALLBACK_STT_MODELS: tuple[str, ...] = (
    'stt-openai/gpt-4o-mini-transcribe',
    'stt-deepgram/nova-3',
    'stt-openai/whisper-1',
)

_WEEKDAY_NAMES: tuple[str, ...] = (
    'понедельник',
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
    'воскресенье',
)


class AIServiceError(Exception):
    """Базовое исключение для ошибок модуля искусственного интеллекта."""


def build_system_prompt(current_dt: datetime.datetime) -> str:
    """Формирует системный промпт с текущим временным контекстом.

    Args:
        current_dt: Текущая дата и время в часовом поясе сервиса.

    Returns:
        Текст системного промпта для языковой модели.
    """
    weekday_name = _WEEKDAY_NAMES[current_dt.weekday()]
    date_str = current_dt.strftime('%Y-%m-%d')
    time_str = current_dt.strftime('%H:%M')
    return (
        'Ты — интеллектуальный ассистент автосервиса, принимающий '
        'заявки на ремонт от мастеров и продавцов.\n'
        f'Текущая дата и время (Москва): {date_str} {time_str}, '
        f'день недели: {weekday_name}.\n'
        'График работы сервиса: понедельник–суббота. Воскресенье — выходной!\n\n'
        'Твоя задача — классифицировать намерение мастера (intent):\n'
        '1. CREATE — создание новой записи.\n'
        '2. RESCHEDULE — перенос или изменение существующей записи.\n'
        '3. COMPLETE — завершение работ по автомобилю.\n\n'
        'Правила для намерения CREATE:\n'
        '- Извлеки car_model, start_date, start_time, client_phone, '
        'work_description, work_items, suggested_duration_minutes, post_code.\n'
        '- Шаг времени: 30 минут.\n'
        '- Нормативы длительности работ сервиса:\n'
        '  * замена ГРМ, сцепления: 180 мин (3 часа);\n'
        '  * подвеска, стойки стабилизатора, рычаги: 90 мин (1.5 часа);\n'
        '  * замена тормозных колодок, тормозных дисков, сход-развал: 60 мин;\n'
        '  * замена масла, фильтров, свечей, лампочек: 30 мин;\n'
        '  * если мастер не назвал точное время, используй эти нормы!\n'
        '- Если дата выпадает на воскресенье, укажи в clarification_needed: '
        '"Воскресенье — выходной день автосервиса. Выберите рабочий день."\n'
        '- Сопоставление постов: яма -> P1; первый подъемник -> P2; '
        'второй подъемник -> P3; сход-развал -> P4; '
        'мелкие работы без бокса -> NO_POST. Если не указан — оставь null.\n\n'
        'Правила для намерения RESCHEDULE:\n'
        '- Извлеки target_car_for_action (марка переносимой машины).\n'
        '- Извлеки reschedule_new_date, reschedule_new_time, '
        'reschedule_new_post.\n\n'
        'Правила для намерения COMPLETE:\n'
        '- Извлеки target_car_for_action (марка завершаемой машины).\n'
        '- Извлеки completion_actual_time (время завершения, если названо).'
    )


def _extract_text_from_transcription_response(response: Any) -> str:
    """Извлекает строку текста из ответа любого типа шлюза транскрибации.

    Args:
        response: Ответ API (объект модели, словарь или строка).

    Returns:
        Очищенная строка с распознанным текстом.
    """
    if hasattr(response, 'text'):
        return str(response.text).strip()
    if isinstance(response, dict) and 'text' in response:
        return str(response['text']).strip()
    return str(response).strip()


class AIService:
    """Сервис интеграции с нейросетевыми моделями шлюза VseGPT.

    Attributes:
        _settings: Настройки приложения.
        _client: Асинхронный клиент OpenAI API.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        """Инициализирует клиент VseGPT с заданными параметрами.

        Args:
            settings: Экземпляр конфигурации приложения.
        """
        self._settings = settings or get_settings()
        self._client = AsyncOpenAI(
            api_key=self._settings.vsegpt_api_key.get_secret_value(),
            base_url=self._settings.vsegpt_base_url,
        )

    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        filename: str = 'voice.ogg',
    ) -> str:
        """Преобразует аудиозапись речи в текст на русском языке.

        Использует каскадный перебор моделей с ограничением по времени,
        чтобы исключить зависания при перегрузке сторонних провайдеров.

        Args:
            audio_bytes: Бинарные данные аудиофайла.
            filename: Имя файла с расширением для заголовков multipart.

        Returns:
            Распознанный текст на русском языке.

        Raises:
            AIServiceError: Если все доступные модели не смогли ответить.
        """
        candidate_models: list[str] = [self._settings.vsegpt_stt_model]
        for fallback_model in _FALLBACK_STT_MODELS:
            if fallback_model not in candidate_models:
                candidate_models.append(fallback_model)

        last_error: Exception | None = None

        for model_name in candidate_models:
            audio_buffer = io.BytesIO(audio_bytes)
            audio_buffer.name = filename

            try:
                raw_response = await asyncio.wait_for(
                    self._client.audio.transcriptions.create(
                        model=model_name,
                        file=audio_buffer,
                        language='ru',
                        response_format='json',
                    ),
                    timeout=_DEFAULT_STT_TIMEOUT_SECONDS,
                )
                text_result = _extract_text_from_transcription_response(
                    raw_response,
                )
                if text_result:
                    return text_result
            except (asyncio.TimeoutError, OpenAIError, Exception) as exc:
                last_error = exc
                logger.warning(
                    'Модель STT %s вернула ошибку или превысила таймаут '
                    '(%.1f с): %s. Попытка переключения на резервную модель...',
                    model_name,
                    _DEFAULT_STT_TIMEOUT_SECONDS,
                    exc,
                )

        raise AIServiceError(
            f'Не удалось распознать речь доступными моделями: {last_error}'
        )

    async def extract_appointment(
        self,
        raw_text: str,
    ) -> AppointmentExtraction:
        """Извлекает параметры заявки из свободного текста мастера.

        Args:
            raw_text: Исходный текст сообщения или расшифровки.

        Returns:
            Структурированные параметры записи в виде Pydantic-схемы.

        Raises:
            AIServiceError: В случае сбоя обращения к модели или валидации.
        """
        timezone = zoneinfo.ZoneInfo(TIMEZONE_NAME)
        current_dt = datetime.datetime.now(timezone)
        system_prompt = build_system_prompt(current_dt)

        strict_schema = AppointmentExtraction.get_strict_json_schema()

        json_schema_format = cast(
            completion_create_params.ResponseFormat,
            {
                'type': 'json_schema',
                'json_schema': {
                    'name': 'appointment_extraction',
                    'schema': strict_schema,
                    'strict': True,
                },
            },
        )

        try:
            response = await self._client.chat.completions.create(
                model=self._settings.vsegpt_chat_model,
                temperature=0.1,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': raw_text},
                ],
                response_format=json_schema_format,
            )
            choice = response.choices[0]
            content = choice.message.content
            if not content:
                raise AIServiceError(
                    'Модель вернула пустой текстовый ответ.'
                )
            return AppointmentExtraction.model_validate_json(content)
        except (OpenAIError, ValidationError) as exc:
            raise AIServiceError(
                f'Ошибка извлечения параметров записи: {exc}'
            ) from exc

    @property
    def client(self) -> AsyncOpenAI:
        """Возвращает клиент для взаимодействия с нейросетевым шлюзом.

        Returns:
            Инициализированный клиент для выполнения запросов.
        """
        return self._client
