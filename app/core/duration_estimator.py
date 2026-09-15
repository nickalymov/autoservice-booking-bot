"""Модуль нормативной оценки длительности сервисных работ.

Обеспечивает предварительный расчет времени ремонта по ключевым словам
и операциям с соблюдением обязательной кратности шагу расписания сервиса.
"""

import math

from app.config import SCHEDULE_STEP_MINUTES

_DEFAULT_DURATION_MINUTES: int = 60

_OPERATION_NORMS: tuple[tuple[tuple[str, ...], int], ...] = (
    (
        ('грм', 'цепи', 'цепей', 'сцеплен'),
        180,
    ),
    (
        (
            'стойк',
            'стабилизатор',
            'рычаг',
            'сайлентблок',
            'подвеск',
            'ходова',
            'амортизатор',
            'пружин',
        ),
        90,
    ),
    (
        (
            'колодк',
            'тормоз',
            'диск',
            'сход-развал',
            'развал',
            'схождение',
            'диагностик',
            'осмотр',
            'поиск',
            'стук',
        ),
        60,
    ),
    (
        (
            'масл',
            'фильтр',
            'свеч',
            'лампочк',
            'свет',
            'фара',
            'габарит',
            'дворник',
        ),
        30,
    ),
)


def _round_to_schedule_step(minutes: int) -> int:
    """Округляет длительность в большую сторону до шага расписания.

    Args:
        minutes: Исходное расчетное время в минутах.

    Returns:
        Длительность в минутах, кратная SCHEDULE_STEP_MINUTES.
    """
    step = max(1, SCHEDULE_STEP_MINUTES)
    snapped = math.ceil(max(1, minutes) / step) * step
    return max(step, snapped)


def estimate_duration_minutes(
    work_description: str | None = None,
    work_items: list[str] | None = None,
) -> int:
    """Оценивает плановую длительность ремонта по видам работ.

    Анализирует описание неисправности и технологические операции,
    сопоставляя их с нормативной базой типовых услуг сервиса.

    Args:
        work_description: Текстовое описание проблемы от мастера.
        work_items: Список конкретных операций, извлеченных ИИ.

    Returns:
        Плановая длительность в минутах с шагом SCHEDULE_STEP_MINUTES.
    """
    text_parts: list[str] = []
    if work_description:
        text_parts.append(work_description.lower())
    if work_items:
        text_parts.extend(item.lower() for item in work_items)

    combined_text = ' '.join(text_parts).strip()
    if not combined_text:
        return _DEFAULT_DURATION_MINUTES

    estimated_minutes = 0
    for keywords, norm_duration in _OPERATION_NORMS:
        for keyword in keywords:
            if keyword in combined_text:
                estimated_minutes = max(
                    estimated_minutes,
                    norm_duration,
                )
                break

    if estimated_minutes == 0:
        estimated_minutes = _DEFAULT_DURATION_MINUTES

    return _round_to_schedule_step(estimated_minutes)
