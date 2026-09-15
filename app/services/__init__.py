"""Пакет внешних сервисов и интеграций приложения.

Экспортирует сервисы взаимодействия со шлюзом нейросетей VseGPT,
календарями Google API и планировщиком фоновых уведомлений.
"""

from app.services.ai_service import AIService
from app.services.ai_service import AIServiceError
from app.services.calendar_service import CalendarServiceError
from app.services.calendar_service import GoogleCalendarService
from app.services.scheduler_service import SchedulerService

__all__: tuple[str, ...] = (
    'AIService',
    'AIServiceError',
    'CalendarServiceError',
    'GoogleCalendarService',
    'SchedulerService',
)
