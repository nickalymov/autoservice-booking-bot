"""Модуль схем данных для записей на ремонт автосервиса.

Содержит статусы жизненного цикла, источники создания, модели извлечения данных
из текста нейросетью, функции преобразования схемы в строгий формат OpenAI
и структуры черновиков для пользовательского интерфейса.
"""

from __future__ import annotations

import copy
import datetime
import enum
from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import computed_field

from app.config import POST_NAMES
from app.config import PostCode


class ActionIntent(str, enum.Enum):
    """Категория намерения мастера при отправке сообщения."""

    CREATE = 'CREATE'
    RESCHEDULE = 'RESCHEDULE'
    COMPLETE = 'COMPLETE'


class AppointmentSource(str, enum.Enum):
    """Источник создания записи на обслуживание."""

    VOICE = 'VOICE'
    TEXT = 'TEXT'
    MANUAL = 'MANUAL'
    GOOGLE_CALENDAR = 'GOOGLE_CALENDAR'


class AppointmentStatus(str, enum.Enum):
    """Статусы жизненного цикла записи на ремонт."""

    DRAFT = 'DRAFT'
    CONFIRMED = 'CONFIRMED'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    NO_SHOW = 'NO_SHOW'
    CANCELLED = 'CANCELLED'
    WAITING_TRANSFER = 'WAITING_TRANSFER'


STATUS_NAMES: dict[AppointmentStatus, str] = {
    AppointmentStatus.DRAFT: 'Черновик',
    AppointmentStatus.CONFIRMED: 'Ожидает',
    AppointmentStatus.IN_PROGRESS: 'В работе',
    AppointmentStatus.DONE: 'Готово',
    AppointmentStatus.NO_SHOW: 'Не приехал',
    AppointmentStatus.CANCELLED: 'Отменено',
    AppointmentStatus.WAITING_TRANSFER: 'Ожидает принятия передачи',
}


def format_duration_human(minutes: int) -> str:
    """Преобразует длительность в минутах в текст на русском языке.

    Args:
        minutes: Длительность в минутах.

    Returns:
        Отформатированная строка с часами и минутами.
    """
    hours = minutes // 60
    rem_minutes = minutes % 60
    result: list[str] = []
    if hours > 0:
        result.append(f'{hours} ч')
    if rem_minutes > 0:
        result.append(f'{rem_minutes} мин')
    return ' '.join(result) if result else '0 мин'


def to_strict_json_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Преобразует схему Pydantic в строгий формат OpenAI Structured Outputs.

    Args:
        schema: Исходный словарь схемы, сгенерированный Pydantic.

    Returns:
        Словарь схемы, соответствующий правилам OpenAI Strict Schema.
    """
    strict_schema = copy.deepcopy(schema)
    definitions = strict_schema.pop('$defs', {})

    def _resolve_and_sanitize(node: Any) -> Any:
        if isinstance(node, list):
            return [_resolve_and_sanitize(item) for item in node]
        if not isinstance(node, dict):
            return node

        if '$ref' in node:
            ref_path = node['$ref']
            ref_name = ref_path.split('/')[-1]
            if ref_name in definitions:
                resolved_definition = copy.deepcopy(definitions[ref_name])
                return _resolve_and_sanitize(resolved_definition)

        cleaned_node: dict[str, Any] = {}
        for key, value in node.items():
            if key == 'default':
                continue
            cleaned_node[key] = _resolve_and_sanitize(value)

        if cleaned_node.get('type') == 'object' or 'properties' in cleaned_node:
            cleaned_node['type'] = 'object'
            cleaned_node['additionalProperties'] = False
            properties = cleaned_node.get('properties', {})
            cleaned_node['required'] = list(properties.keys())

        return cleaned_node

    return _resolve_and_sanitize(strict_schema)


class AppointmentExtraction(BaseModel):
    """Результат комплексного анализа сообщения мастера нейросетью.

    Attributes:
        intent: Распознанное намерение сотрудника.
        car_model: Марка и модель автомобиля для новой записи.
        start_date: Дата начала в формате YYYY-MM-DD.
        start_time: Время начала в формате HH:MM (шаг 30 минут).
        client_phone: Номер телефона клиента.
        client_name: Имя клиента.
        license_plate: Государственный номер автомобиля.
        vin: Идентификационный номер (VIN) автомобиля.
        work_description: Описание неисправности или перечень работ.
        work_items: Список конкретных операций для калькуляции времени.
        suggested_duration_minutes: Оценка длительности в минутах.
        post_code: Выбранный или названный рабочий пост.
        assigned_master_name: Названное имя ответственного мастера.
        clarification_needed: Текст уточняющего вопроса при сомнениях.
        target_car_for_action: Марка машины для изменения или завершения.
        reschedule_new_date: Новая дата при переносе (YYYY-MM-DD).
        reschedule_new_time: Новое время начала при переносе (HH:MM).
        reschedule_new_post: Новый пост при переносе.
        completion_actual_time: Фактическое время завершения при закрытии.
    """

    model_config = ConfigDict(extra='forbid')

    intent: ActionIntent = Field(
        default=ActionIntent.CREATE,
        description='Тип действия: создание, перенос или завершение',
    )
    car_model: str | None = Field(
        default=None,
        description='Марка и модель автомобиля для создания записи',
    )
    start_date: str | None = Field(
        default=None,
        description='Календарная дата в формате YYYY-MM-DD',
    )
    start_time: str | None = Field(
        default=None,
        description='Время начала в формате HH:MM (шаг 30 минут)',
    )
    client_phone: str | None = Field(
        default=None,
        description='Номер телефона клиента',
    )
    client_name: str | None = Field(
        default=None,
        description='Имя клиента',
    )
    license_plate: str | None = Field(
        default=None,
        description='Государственный номер автомобиля',
    )
    vin: str | None = Field(
        default=None,
        description='VIN-номер автомобиля',
    )
    work_description: str | None = Field(
        default=None,
        description='Причина обращения или суть неисправности',
    )
    work_items: list[str] = Field(
        default_factory=list,
        description='Список конкретных технологических операций',
    )
    suggested_duration_minutes: int | None = Field(
        default=None,
        description='Плановая длительность работ в минутах (кратно 30)',
    )
    post_code: PostCode | None = Field(
        default=None,
        description='Идентификатор рабочего поста или NO_POST',
    )
    assigned_master_name: str | None = Field(
        default=None,
        description='Имя назначенного мастера (Вова, Коля, Рамазан)',
    )
    clarification_needed: str | None = Field(
        default=None,
        description='Вопрос к мастеру при неоднозначности данных',
    )
    target_car_for_action: str | None = Field(
        default=None,
        description='Автомобиль для поиска существующей записи',
    )
    reschedule_new_date: str | None = Field(
        default=None,
        description='Новая дата при переносе (YYYY-MM-DD)',
    )
    reschedule_new_time: str | None = Field(
        default=None,
        description='Новое время начала при переносе (HH:MM)',
    )
    reschedule_new_post: PostCode | None = Field(
        default=None,
        description='Новый рабочий пост при переносе',
    )
    completion_actual_time: str | None = Field(
        default=None,
        description='Фактическое время завершения при закрытии наряда',
    )

    @classmethod
    def get_strict_json_schema(cls) -> dict[str, Any]:
        """Возвращает JSON-схему модели, совместимую со строгим режимом OpenAI.

        Returns:
            Словарь строгой JSON-схемы для параметра response_format.
        """
        raw_schema = cls.model_json_schema()
        return to_strict_json_schema(raw_schema)


class AppointmentDraft(BaseModel):
    """Черновик записи на ремонт в оперативной памяти бота.

    Attributes:
        draft_id: Уникальный номер черновика.
        master_telegram_id: Telegram ID ответственного мастера.
        master_name: Имя ответственного мастера.
        master_id: Внутренний первичный ключ мастера в базе данных.
        source: Канал создания записи.
        status: Текущий статус заявки.
        raw_transcription: Исходная текстовая расшифровка речи мастера.
        car_model: Марка и модель транспортного средства.
        client_phone: Телефон клиента для связи.
        client_name: Имя клиента.
        license_plate: Госномер автомобиля.
        vin: VIN-код автомобиля.
        work_description: Заявленная неисправность или причина визита.
        work_items: Перечень конкретных работ.
        start_datetime: Дата и время начала обслуживания.
        planned_duration_minutes: Плановое время обслуживания в минутах.
        post_code: Назначенный рабочий пост.
        clarification_question: Текущий уточняющий вопрос системы.
        is_sunday_confirmed: Подтверждена ли запись на воскресенье.
        is_overtime_confirmed: Подтверждена ли сверхурочная работа.
        is_master_overlap_confirmed: Подтверждено ли пересечение времени мастера.
        master_overlap_info: Сведения о пересекающейся заявке мастера.
    """

    draft_id: str = Field(
        description='Уникальный номер записи',
    )
    master_telegram_id: int = Field(
        description='Идентификатор Telegram мастера',
    )
    master_name: str = Field(
        description='Имя мастера, создавшего запись',
    )
    master_id: int | None = Field(
        default=None,
        description='Внутренний идентификатор мастера в БД',
    )
    source: AppointmentSource = Field(
        default=AppointmentSource.VOICE,
        description='Источник создания записи',
    )
    status: AppointmentStatus = Field(
        default=AppointmentStatus.DRAFT,
        description='Статус заявки',
    )
    raw_transcription: str | None = Field(
        default=None,
        description='Исходный текст голосового сообщения',
    )
    car_model: str | None = Field(
        default=None,
        description='Марка и модель автомобиля',
    )
    client_phone: str | None = Field(
        default=None,
        description='Телефон клиента',
    )
    client_name: str | None = Field(
        default=None,
        description='Имя клиента',
    )
    license_plate: str | None = Field(
        default=None,
        description='Госномер автомобиля',
    )
    vin: str | None = Field(
        default=None,
        description='VIN-номер',
    )
    work_description: str | None = Field(
        default=None,
        description='Описание жалобы или причины визита',
    )
    work_items: list[str] = Field(
        default_factory=list,
        description='Список работ',
    )
    start_datetime: datetime.datetime | None = Field(
        default=None,
        description='Дата и время начала работ',
    )
    planned_duration_minutes: int | None = Field(
        default=None,
        description='Плановая длительность в минутах',
    )
    post_code: PostCode | None = Field(
        default=None,
        description='Код рабочего поста',
    )
    clarification_question: str | None = Field(
        default=None,
        description='Уточняющий вопрос',
    )
    is_sunday_confirmed: bool = Field(
        default=False,
        description='Флаг подтверждения записи на воскресенье',
    )
    is_overtime_confirmed: bool = Field(
        default=False,
        description='Флаг подтверждения сверхурочной работы',
    )
    is_master_overlap_confirmed: bool = Field(
        default=False,
        description='Флаг подтверждения накладки у мастера',
    )
    master_overlap_info: str | None = Field(
        default=None,
        description='Информация о пересекающейся заявке мастера',
    )

    @property
    def start_time(self) -> datetime.datetime | None:
        """Возвращает время начала для обратной совместимости."""
        return self.start_datetime

    @property
    def duration(self) -> datetime.timedelta | None:
        """Возвращает плановую длительность в виде объекта timedelta."""
        if self.planned_duration_minutes is None:
            return None
        return datetime.timedelta(minutes=self.planned_duration_minutes)

    @property
    def post_id(self) -> str | None:
        """Возвращает код рабочего поста в виде строкового значения."""
        return self.post_code.value if self.post_code else None

    @computed_field
    @property
    def end_datetime(self) -> datetime.datetime | None:
        """Вычисляет расчетную дату и время окончания работ."""
        if (
            self.start_datetime is None
            or self.planned_duration_minutes is None
        ):
            return None
        delta = datetime.timedelta(
            minutes=self.planned_duration_minutes,
        )
        return self.start_datetime + delta

    def missing_required_fields(self) -> list[str]:
        """Возвращает список незаполненных обязательных полей.

        Returns:
            Список наименований недостающих обязательных полей.
        """
        missing: list[str] = []
        if not self.car_model:
            missing.append('Автомобиль (марка/модель)')
        if self.start_datetime is None:
            missing.append('Дата и время начала')
        if self.planned_duration_minutes is None:
            missing.append('Плановая длительность')
        if self.post_code is None:
            missing.append('Рабочий пост')
        if not self.client_phone:
            missing.append('Телефон клиента')
        if not self.work_description and not self.work_items:
            missing.append('Тип работ / жалоба')
        return missing

    def is_ready_for_confirmation(self) -> bool:
        """Проверяет полноту обязательных данных для бронирования.

        Returns:
            True, если все обязательные поля заполнены, иначе False.
        """
        return not self.missing_required_fields()

    def format_telegram_card(self) -> str:
        """Формирует карточку записи для подтверждения в Telegram.

        Returns:
            Отформатированный HTML-текст карточки черновика.
        """
        post_label = (
            POST_NAMES.get(self.post_code, str(self.post_code))
            if self.post_code
            else 'Не выбран'
        )
        time_label = 'Не указано'
        if self.start_datetime and self.end_datetime:
            start_str = self.start_datetime.strftime('%d.%m.%Y, %H:%M')
            end_str = self.end_datetime.strftime('%H:%M')
            time_label = f'{start_str}–{end_str}'
        duration_label = (
            format_duration_human(self.planned_duration_minutes)
            if self.planned_duration_minutes
            else 'Не определена'
        )
        lines: list[str] = [
            '<b>Черновик записи</b>',
            f'<b>ID:</b> {self.draft_id} ({self.car_model or "Авто не указано"})',
            f'<b>Мастер:</b> {self.master_name}',
            f'<b>Пост:</b> {post_label}',
            f'<b>Время:</b> {time_label}',
            f'<b>Автомобиль:</b> {self.car_model or "Не указан"}',
            f'<b>Телефон:</b> {self.client_phone or "Не указан"}',
        ]
        if self.client_name:
            lines.append(f'<b>Имя клиента:</b> {self.client_name}')
        if self.license_plate:
            lines.append(f'<b>Госномер:</b> {self.license_plate}')
        if self.vin:
            lines.append(f'<b>VIN:</b> {self.vin}')
        work_text = self.work_description or ', '.join(self.work_items)
        lines.append(f'<b>Причина/работы:</b> {work_text or "Не указано"}')
        lines.append(f'<b>Плановая длительность:</b> {duration_label}')

        if self.master_overlap_info and not self.is_master_overlap_confirmed:
            lines.append(
                f'\n⚠️ <b>Внимание:</b> {self.master_overlap_info}'
            )

        return '\n'.join(lines)
