"""Пакет схем данных и моделей валидации приложения автосервиса.

Экспортирует Pydantic-схемы для извлечения параметров нарядов,
черновиков бронирования и управления учетными записями сотрудников.
"""

from app.schemas.appointment import AppointmentDraft
from app.schemas.appointment import AppointmentExtraction
from app.schemas.appointment import AppointmentStatus
from app.schemas.appointment import STATUS_NAMES
from app.schemas.appointment import format_duration_human
from app.schemas.user import UserBase
from app.schemas.user import UserCreate
from app.schemas.user import UserRead
from app.schemas.user import UserUpdate
from app.schemas.user import WhitelistConfig
from app.schemas.user import WhitelistEntry

__all__: tuple[str, ...] = (
    'AppointmentDraft',
    'AppointmentExtraction',
    'AppointmentStatus',
    'STATUS_NAMES',
    'UserBase',
    'UserCreate',
    'UserRead',
    'UserUpdate',
    'WhitelistConfig',
    'WhitelistEntry',
    'format_duration_human',
)
