"""Модуль тестов структурированного извлечения данных заявки и схем ИИ.

Проверяет валидность JSON-схемы OpenAI/VseGPT, сборку системного промпта,
десериализацию фраз мастеров из ТЗ и методы черновика AppointmentDraft.
"""

from __future__ import annotations

import datetime
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
import zoneinfo

import pytest

from app.config import PostCode
from app.config import Settings
from app.schemas.appointment import ActionIntent
from app.schemas.appointment import AppointmentDraft
from app.schemas.appointment import AppointmentExtraction
from app.schemas.appointment import AppointmentSource
from app.schemas.appointment import format_duration_human
from app.schemas.appointment import to_strict_json_schema
from app.services import ai_service


def test_json_schema_validity() -> None:
    """Проверяет соответствие сгенерированной JSON-схемы спецификации."""
    schema = AppointmentExtraction.get_strict_json_schema()

    assert schema['type'] == 'object'
    assert schema['additionalProperties'] is False

    properties = schema.get('properties', {})
    required_fields = schema.get('required', [])

    assert set(properties.keys()) == set(required_fields)

    assert 'intent' in properties
    assert 'car_model' in properties
    assert 'start_date' in properties
    assert 'start_time' in properties
    assert 'client_phone' in properties
    assert 'post_code' in properties
    assert 'suggested_duration_minutes' in properties
    assert 'work_description' in properties
    assert 'assigned_master_name' in properties

    for prop_name, prop_schema in properties.items():
        assert 'default' not in prop_schema, f'Найден default в {prop_name}'


def test_to_strict_json_schema_removes_defs_and_defaults() -> None:
    """Проверяет устранение $defs и флагов default в строгой схеме."""
    raw_schema = {
        '$defs': {
            'StatusEnum': {
                'type': 'string',
                'enum': ['ONE', 'TWO'],
            }
        },
        'type': 'object',
        'properties': {
            'status': {
                '$ref': '#/$defs/StatusEnum',
                'default': 'ONE',
            },
            'note': {
                'type': 'string',
                'default': None,
            },
        },
    }

    strict = to_strict_json_schema(raw_schema)

    assert '$defs' not in strict
    assert strict['additionalProperties'] is False
    assert set(strict['required']) == {'status', 'note'}
    assert 'default' not in strict['properties']['status']
    assert 'default' not in strict['properties']['note']
    assert strict['properties']['status']['enum'] == ['ONE', 'TWO']


def test_system_prompt_builder() -> None:
    """Проверяет включение правил ТЗ и контекста даты в системный промпт."""
    test_dt = datetime.datetime(
        2026,
        9,
        9,
        14,
        30,
        tzinfo=zoneinfo.ZoneInfo('Europe/Moscow'),
    )
    prompt = ai_service.build_system_prompt(test_dt)

    assert '2026-09-09 14:30' in prompt
    assert 'среда' in prompt
    assert 'Воскресенье — выходной' in prompt
    assert 'P1' in prompt
    assert 'P2' in prompt
    assert 'P3' in prompt
    assert 'P4' in prompt
    assert 'NO_POST' in prompt
    assert '30 минут' in prompt


def test_parse_tz_full_voice_message() -> None:
    """Проверяет разбор эталонного сообщения мастера по разделу 10.1 ТЗ."""
    extraction_data = {
        'intent': 'CREATE',
        'car_model': 'Kia Rio',
        'start_date': '2026-09-10',
        'start_time': '10:00',
        'client_phone': '+7 928 123-45-67',
        'client_name': None,
        'license_plate': None,
        'vin': None,
        'work_description': 'замена стоек стабилизатора',
        'work_items': ['замена стоек стабилизатора'],
        'suggested_duration_minutes': 90,
        'post_code': 'P2',
        'assigned_master_name': 'Вова',
        'clarification_needed': None,
        'target_car_for_action': None,
        'reschedule_new_date': None,
        'reschedule_new_time': None,
        'reschedule_new_post': None,
        'completion_actual_time': None,
    }

    extraction = AppointmentExtraction.model_validate(extraction_data)
    assert extraction.intent == ActionIntent.CREATE
    assert extraction.car_model == 'Kia Rio'
    assert extraction.post_code == PostCode.P2
    assert extraction.suggested_duration_minutes == 90
    assert extraction.assigned_master_name == 'Вова'

    timezone = zoneinfo.ZoneInfo('Europe/Moscow')
    start_dt = datetime.datetime(2026, 9, 10, 10, 0, tzinfo=timezone)

    draft = AppointmentDraft(
        draft_id='B209093036',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.VOICE,
        car_model=extraction.car_model,
        client_phone=extraction.client_phone,
        work_description=extraction.work_description,
        work_items=extraction.work_items,
        start_datetime=start_dt,
        planned_duration_minutes=extraction.suggested_duration_minutes,
        post_code=extraction.post_code,
    )

    assert draft.is_ready_for_confirmation() is True
    assert draft.missing_required_fields() == []
    assert draft.source == AppointmentSource.VOICE

    expected_end = datetime.datetime(2026, 9, 10, 11, 30, tzinfo=timezone)
    assert draft.end_datetime == expected_end

    card_html = draft.format_telegram_card()
    assert 'Kia Rio' in card_html
    assert '10:00–11:30' in card_html
    assert '1 ч 30 мин' in card_html
    assert 'Вова' in card_html


def test_parse_tz_incomplete_voice_message() -> None:
    """Проверяет выявление недостающих полей по разделу 10.2 ТЗ."""
    extraction = AppointmentExtraction(
        car_model='Hyundai',
        work_description='ходовая',
        suggested_duration_minutes=90,
    )

    draft = AppointmentDraft(
        draft_id='DRAFT-002',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.VOICE,
        car_model=extraction.car_model,
        work_description=extraction.work_description,
        planned_duration_minutes=extraction.suggested_duration_minutes,
    )

    assert draft.is_ready_for_confirmation() is False
    missing = draft.missing_required_fields()

    assert 'Дата и время начала' in missing
    assert 'Рабочий пост' in missing
    assert 'Телефон клиента' in missing


def test_draft_update_from_voice_edit() -> None:
    """Проверяет обновление полей черновика при голосовой корректировке."""
    timezone = zoneinfo.ZoneInfo('Europe/Moscow')
    start_dt = datetime.datetime(2026, 9, 10, 10, 0, tzinfo=timezone)

    draft = AppointmentDraft(
        draft_id='DRAFT-EDIT',
        master_telegram_id=101,
        master_name='Вова',
        source=AppointmentSource.VOICE,
        car_model='Kia Rio',
        client_phone='+79281234567',
        work_description='Диагностика',
        start_datetime=start_dt,
        planned_duration_minutes=60,
        post_code=PostCode.P1,
    )

    edit_extraction = AppointmentExtraction(
        car_model='Lada Vesta',
        suggested_duration_minutes=120,
        post_code=PostCode.P2,
    )

    if edit_extraction.car_model:
        draft.car_model = edit_extraction.car_model
    if edit_extraction.suggested_duration_minutes:
        draft.planned_duration_minutes = (
            edit_extraction.suggested_duration_minutes
        )
    if edit_extraction.post_code:
        draft.post_code = edit_extraction.post_code

    assert draft.car_model == 'Lada Vesta'
    assert draft.planned_duration_minutes == 120
    assert draft.post_code == PostCode.P2

    expected_end = datetime.datetime(2026, 9, 10, 12, 0, tzinfo=timezone)
    assert draft.end_datetime == expected_end


@pytest.mark.asyncio
async def test_ai_service_extract_appointment_mocked() -> None:
    """Проверяет изолированную работу AIService.extract_appointment."""
    mock_settings = Settings()
    service_instance = ai_service.AIService(settings=mock_settings)

    mock_json_content = (
        '{"intent": "CREATE", "car_model": "Lada Vesta", '
        '"start_date": "2026-09-11", "start_time": "11:00", '
        '"client_phone": "+79991112233", "client_name": null, '
        '"license_plate": null, "vin": null, '
        '"work_description": "замена масла", "work_items": ["замена масла"], '
        '"suggested_duration_minutes": 60, "post_code": "P2", '
        '"assigned_master_name": "Коля", '
        '"clarification_needed": null, "target_car_for_action": null, '
        '"reschedule_new_date": null, "reschedule_new_time": null, '
        '"reschedule_new_post": null, "completion_actual_time": null}'
    )

    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = mock_json_content
    mock_response.choices = [mock_choice]

    with patch.object(
        service_instance.client.chat.completions,
        'create',
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        result = await service_instance.extract_appointment(
            raw_text='Поставь завтра на 11 Ладу Весту на масло на час мастеру Коле',
        )

        assert result.intent == ActionIntent.CREATE
        assert result.car_model == 'Lada Vesta'
        assert result.suggested_duration_minutes == 60
        assert result.post_code == PostCode.P2
        assert result.assigned_master_name == 'Коля'


@pytest.mark.asyncio
async def test_ai_service_transcribe_mocked() -> None:
    """Проверяет транскрибацию аудиозаписи в текст через Whisper."""
    mock_settings = Settings()
    service_instance = ai_service.AIService(settings=mock_settings)

    mock_transcription = MagicMock()
    mock_transcription.text = 'Запиши Киа Рио на 10 утра'

    with patch.object(
        service_instance.client.audio.transcriptions,
        'create',
        new_callable=AsyncMock,
        return_value=mock_transcription,
    ):
        text = await service_instance.transcribe_audio(
            audio_bytes=b'fake_ogg_bytes',
        )
        assert text == 'Запиши Киа Рио на 10 утра'


def test_format_duration_human() -> None:
    """Проверяет форматирование длительности в читаемую строку."""
    assert format_duration_human(30) == '30 мин'
    assert format_duration_human(60) == '1 ч'
    assert format_duration_human(90) == '1 ч 30 мин'
    assert format_duration_human(120) == '2 ч'
    assert format_duration_human(180) == '3 ч'
    assert format_duration_human(0) == '0 мин'
