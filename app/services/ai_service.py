"""Модуль сервиса искусственного интеллекта автосервиса.

Обеспечивает асинхронную транскрибацию голосовых сообщений
через мультимодальный Chat API VseGPT (audioinput) с каскадным
переключением на внешние шлюзы и структурированное извлечение параметров.
"""

from __future__ import annotations

import asyncio
import base64
import datetime
import io
import logging
from typing import Any
from typing import cast
import zoneinfo

import httpx
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
        'График работы сервиса: понедельник–суббота (09:00–20:00). '
        'Воскресенье обычно выходной.\n\n'
        'КРИТИЧЕСКИЕ ПРАВИЛА ИЗВЛЕЧЕНИЯ ДАННЫХ:\n'
        '1. СТРОЖАЙШИЙ ЗАПРЕТ НА ВЫДУМЫВАНИЕ ВРЕМЕНИ:\n'
        '   - Если пользователь НЕ назвал точное время в сообщении, '
        'поле start_time ОБЯЗАНО быть null!\n'
        '   - Категорически запрещено подставлять 09:00, начало смены '
        'или текущее время, если времени нет в тексте пользователя!\n'
        '   - Если время названо (например, 21:00) — извлеки ровно его.\n\n'
        '2. ДАТА:\n'
        '   - Если дата не названа, но названо только время: если сегодня '
        'воскресенье, укажи дату воскресенья, не сдвигай самовольно на понедельник!\n'
        '   - Если пользователь говорит "завтра" в субботу, укажи дату воскресенья.\n\n'
        '3. КЛАССИФИКАЦИЯ НАМЕРЕНИЙ (intent):\n'
        '   - CREATE — создание новой записи.\n'
        '   - RESCHEDULE — перенос или изменение существующей записи.\n'
        '   - COMPLETE — завершение работ по автомобилю.\n\n'
        '4. ПРАВИЛА ДЛЯ CREATE:\n'
        '   - Извлеки car_model, start_date, start_time, client_phone, '
        'work_description, work_items, suggested_duration_minutes, post_code.\n'
        '   - Нормативы длительности работ сервиса:\n'
        '     * замена ГРМ, сцепления: 180 мин (3 часа);\n'
        '     * подвеска, стойки стабилизатора, рычаги: 90 мин (1.5 часа);\n'
        '     * замена тормозных колодок, тормозных дисков, сход-развал: 60 мин;\n'
        '     * замена масла, фильтров, свечей, лампочек: 30 мин;\n'
        '     * если мастер не назвал длительность, используй эти нормы.\n'
        '   - Сопоставление постов: яма -> P1; первый подъемник -> P2; '
        'второй подъемник -> P3; сход-развал -> P4; '
        'мелкие работы без бокса -> NO_POST. Если не указан — null.\n\n'
        '5. ПРАВИЛА ДЛЯ RESCHEDULE:\n'
        '   - Извлеки target_car_for_action (марка переносимой машины).\n'
        '   - Извлеки reschedule_new_date, reschedule_new_time, reschedule_new_post.\n\n'
        '6. ПРАВИЛА ДЛЯ COMPLETE:\n'
        '   - Извлеки target_car_for_action (марка завершаемой машины).\n'
        '   - Извлеки completion_actual_time (время завершения, если названо).'
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
    """Сервис интеграции с нейросетевыми моделями VseGPT, Deepgram и Groq.

    Attributes:
        _settings: Настройки приложения.
        _client: Асинхронный клиент OpenAI API для основного шлюза VseGPT.
        _groq_client: Асинхронный клиент для шлюза Groq при его доступности.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        """Инициализирует клиенты нейросетей с заданными параметрами.

        Args:
            settings: Экземпляр конфигурации приложения.
        """
        self._settings = settings or get_settings()
        self._client = AsyncOpenAI(
            api_key=self._settings.vsegpt_api_key.get_secret_value(),
            base_url=self._settings.vsegpt_base_url,
        )
        self._groq_client: AsyncOpenAI | None = None
        if (
            self._settings.groq_api_key
            and self._settings.groq_api_key.get_secret_value()
        ):
            self._groq_client = AsyncOpenAI(
                api_key=self._settings.groq_api_key.get_secret_value(),
                base_url=self._settings.groq_base_url,
            )

    async def _transcribe_with_vsegpt_audioinput(
        self,
        audio_bytes: bytes,
    ) -> str | None:
        """Транскрибирует речь через мультимодальный Chat API VseGPT.

        Args:
            audio_bytes: Бинарные данные аудиофайла из Telegram.

        Returns:
            Распознанный текст на русском языке или None при ошибке.
        """
        if not self._settings.vsegpt_use_audioinput:
            return None

        encoded_audio = base64.b64encode(audio_bytes).decode('utf-8')
        prompt_text = (
            'Ты — ассистент автосервиса. Твоя единственная задача — дословно '
            'расшифровать голосовое сообщение мастера на русском языке. '
            'Точно сохрани все марки машин, числа, телефонные номера и термины. '
            'Выведи ТОЛЬКО распознанный текст без кавычек, вводных слов и пояснений.'
        )

        candidate_models = (
            self._settings.vsegpt_audioinput_model,
            'google/gemini-3.1-flash-lite',
            'google/gemini-3.1-flash-lite-pre',
            'google/gemini-3.5-flash',
        )

        for model_name in candidate_models:
            try:
                response = await asyncio.wait_for(
                    self._client.chat.completions.create(
                        model=model_name,
                        messages=[{
                            'role': 'user',
                            'content': [
                                {
                                    'type': 'input_audio',
                                    'input_audio': {
                                        'data': encoded_audio,
                                        'format': 'mp3',
                                    },
                                },
                                {
                                    'type': 'text',
                                    'text': prompt_text,
                                },
                            ],
                        }],
                        temperature=0.0,
                        max_tokens=400,
                    ),
                    timeout=20.0,
                )
                content = response.choices[0].message.content
                if content and content.strip():
                    return content.strip().strip('"').strip("'")
            except Exception as exc:
                logger.warning(
                    'Модель VseGPT audioinput %s вернула ошибку: %s',
                    model_name,
                    exc,
                )

        return None

    async def _transcribe_with_deepgram(
        self,
        audio_bytes: bytes,
    ) -> str | None:
        """Транскрибирует аудиозапись через REST API Deepgram.

        Args:
            audio_bytes: Бинарные данные аудиофайла.

        Returns:
            Распознанный текст на русском языке или None при ошибке.
        """
        if (
            not self._settings.deepgram_api_key
            or not self._settings.deepgram_api_key.get_secret_value()
        ):
            return None

        url = (
            f'{self._settings.deepgram_base_url}?'
            f'model={self._settings.deepgram_model}&'
            'language=ru&'
            'smart_format=true'
        )
        headers = {
            'Authorization': (
                f'Token {self._settings.deepgram_api_key.get_secret_value()}'
            ),
            'Content-Type': 'audio/ogg',
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as http_client:
                response = await http_client.post(
                    url=url,
                    headers=headers,
                    content=audio_bytes,
                )
                if response.status_code == 200:
                    payload = response.json()
                    channels = payload.get('results', {}).get('channels', [])
                    if channels:
                        alts = channels[0].get('alternatives', [])
                        if alts:
                            transcript = alts[0].get('transcript', '')
                            if transcript.strip():
                                return transcript.strip()
                logger.warning(
                    'Deepgram вернул статус %d: %s',
                    response.status_code,
                    response.text,
                )
        except Exception as exc:
            logger.warning('Сбой соединения с Deepgram API: %s', exc)

        return None

    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        filename: str = 'voice.ogg',
    ) -> str:
        """Преобразует аудиозапись речи в текст на русском языке.

        Использует приоритетный вызов VseGPT audioinput (Gemini),
        затем Deepgram, Groq и каскад классических моделей STT.

        Args:
            audio_bytes: Бинарные данные аудиофайла.
            filename: Имя файла с расширением для заголовков multipart.

        Returns:
            Распознанный текст на русском языке.

        Raises:
            AIServiceError: Если все доступные сервисы не смогли ответить.
        """
        vsegpt_audio_result = await self._transcribe_with_vsegpt_audioinput(
            audio_bytes,
        )
        if vsegpt_audio_result:
            return vsegpt_audio_result

        deepgram_result = await self._transcribe_with_deepgram(audio_bytes)
        if deepgram_result:
            return deepgram_result

        if self._groq_client is not None:
            audio_buffer = io.BytesIO(audio_bytes)
            audio_buffer.name = filename
            try:
                raw_response = await asyncio.wait_for(
                    self._groq_client.audio.transcriptions.create(
                        model=self._settings.groq_stt_model,
                        file=audio_buffer,
                        language='ru',
                        response_format='json',
                    ),
                    timeout=15.0,
                )
                text_result = _extract_text_from_transcription_response(
                    raw_response,
                )
                if text_result:
                    return text_result
            except Exception as exc:
                logger.warning(
                    'Groq STT вернул ошибку: %s. Переключение на VseGPT...',
                    exc,
                )

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
            f'Не удалось распознать речь доступными сервисами: {last_error}'
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
