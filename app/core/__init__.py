"""Пакет ядра чистой бизнес-логики автосервиса.

Экспортирует сервис управления бронированием, функции расчета
длительности работ и правила разграничения прав доступа.
"""

from app.core.booking_service import BookingError
from app.core.booking_service import BookingService
from app.core.booking_service import DayScheduleOverview
from app.core.booking_service import EntityNotFoundError
from app.core.booking_service import PermissionDeniedError
from app.core.booking_service import PostScheduleItem
from app.core.booking_service import SlotCheckResult
from app.core.booking_service import SlotConflictError
from app.core.duration_estimator import estimate_duration_minutes
from app.core.permissions import can_force_modify
from app.core.permissions import can_manage_appointment
from app.core.permissions import can_manage_users
from app.core.permissions import can_transfer_appointment

__all__: tuple[str, ...] = (
    'BookingError',
    'BookingService',
    'DayScheduleOverview',
    'EntityNotFoundError',
    'PermissionDeniedError',
    'PostScheduleItem',
    'SlotCheckResult',
    'SlotConflictError',
    'can_force_modify',
    'can_manage_appointment',
    'can_manage_users',
    'can_transfer_appointment',
    'estimate_duration_minutes',
)
