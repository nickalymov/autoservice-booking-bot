"""Модуль сервиса интеграции с Google Календарём.

Обеспечивает синхронизацию подтвержденных записей на ремонт
с облачными календарями рабочих постов и общим обзорным календарём.
"""

from __future__ import annotations

import asyncio
from typing import Any

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.config import POST_NAMES
from app.config import PostCode
from app.config import Settings
from app.config import TIMEZONE_NAME
from app.config import get_settings
from app.database.models import Appointment
from app.database.models import Post


class CalendarServiceError(Exception):
    """Базовое исключение для ошибок интеграции с Google Календарём."""


def _build_event_body(
    appointment: Appointment,
    master_name: str | None = None,
) -> dict[str, Any]:
    """Формирует тело запроса события для Google Calendar API.

    Args:
        appointment: Объект записи на обслуживание.
        master_name: Опциональное явно переданное имя мастера.

    Returns:
        Словарь структуры данных события Google Календаря.
    """
    resolved_master_name = master_name
    if resolved_master_name is None:
        if 'master' in appointment.__dict__ and appointment.master is not None:
            resolved_master_name = appointment.master.full_name
        else:
            resolved_master_name = 'Мастер'

    summary = (
        f'[{appointment.public_id}] {appointment.car_model} '
        f'({resolved_master_name})'
    )
    description_parts: list[str] = [
        f'Клиент: {appointment.client_name or "Не указано"}',
        f'Телефон: {appointment.client_phone}',
        f'Работы: {appointment.work_description}',
    ]
    if appointment.license_plate:
        description_parts.append(
            f'Госномер: {appointment.license_plate}',
        )
    if appointment.vin:
        description_parts.append(f'VIN: {appointment.vin}')

    return {
        'summary': summary,
        'description': '\n'.join(description_parts),
        'start': {
            'dateTime': appointment.start_datetime.isoformat(),
            'timeZone': TIMEZONE_NAME,
        },
        'end': {
            'dateTime': appointment.end_datetime.isoformat(),
            'timeZone': TIMEZONE_NAME,
        },
    }


class GoogleCalendarService:
    """Сервис для синхронизации записей с календарями Google API.

    Attributes:
        _settings: Настройки приложения.
        _client: Клиент для работы с Google Calendar API.
        service_account_email: Email сервисного аккаунта из файла ключей.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        """Инициализирует сервис календаря и авторизует клиент Google.

        Args:
            settings: Экземпляр настроек приложения.

        Raises:
            CalendarServiceError: Если файл учетных данных недоступен.
        """
        self._settings = settings or get_settings()
        creds_path = self._settings.google_credentials_path
        if not creds_path.exists():
            raise CalendarServiceError(
                f'Файл ключа Google API не найден по пути: {creds_path}',
            )
        try:
            credentials = (
                service_account.Credentials.from_service_account_file(
                    filename=str(creds_path),
                    scopes=['https://www.googleapis.com/auth/calendar'],
                )
            )
            self.service_account_email: str = getattr(
                credentials,
                'service_account_email',
                'не определен',
            )
            self._client = build(
                serviceName='calendar',
                version='v3',
                credentials=credentials,
                cache_discovery=False,
            )
        except Exception as exc:
            raise CalendarServiceError(
                f'Не удалось инициализировать клиент Google Calendar: {exc}',
            ) from exc

    def _get_calendar_id(self, post_code: PostCode | None) -> str:
        """Определяет ID календаря Google на основе кода поста.

        Args:
            post_code: Код рабочего поста.

        Returns:
            Идентификатор календаря Google в виде строки.
        """
        overview_id = (
            self._settings.google_calendar_overview_id or 'primary'
        )
        if post_code == PostCode.P1:
            return self._settings.google_calendar_p1_id or overview_id
        if post_code == PostCode.P2:
            return self._settings.google_calendar_p2_id or overview_id
        if post_code == PostCode.P3:
            return self._settings.google_calendar_p3_id or overview_id
        if post_code == PostCode.P4:
            return self._settings.google_calendar_p4_id or overview_id
        return overview_id

    async def verify_calendars_access(self) -> dict[str, str | None]:
        """Проверяет доступность всех сконфигурированных календарей.

        Returns:
            Словарь, где ключ — название календаря, а значение — текст ошибки
            или None при успешном доступе.
        """
        calendars_to_check: list[tuple[str, str | None]] = [
            (POST_NAMES[PostCode.P1], self._settings.google_calendar_p1_id),
            (POST_NAMES[PostCode.P2], self._settings.google_calendar_p2_id),
            (POST_NAMES[PostCode.P3], self._settings.google_calendar_p3_id),
            (POST_NAMES[PostCode.P4], self._settings.google_calendar_p4_id),
            (
                'Автосервис — Обзорная загрузка',
                self._settings.google_calendar_overview_id,
            ),
        ]

        results: dict[str, str | None] = {}
        loop = asyncio.get_running_loop()

        for name, calendar_id in calendars_to_check:
            if not calendar_id:
                results[name] = 'Идентификатор календаря не задан в .env'
                continue

            try:
                await loop.run_in_executor(
                    None,
                    lambda cid=calendar_id: self._client.events()
                    .list(calendarId=cid, maxResults=1)
                    .execute(),
                )
                results[name] = None
            except HttpError as exc:
                if exc.resp.status == 404:
                    results[name] = (
                        f'Календарь не найден (404). Сервисному аккаунту '
                        f'{self.service_account_email} не предоставлен '
                        'доступ в настройках календаря.'
                    )
                else:
                    results[name] = (
                        f'Ошибка HTTP {exc.resp.status}: {exc.reason}'
                    )
            except Exception as exc:
                results[name] = f'Ошибка соединения: {exc}'

        return results

    async def create_event(
        self,
        appointment: Appointment,
        post: Post | None,
        master_name: str | None = None,
    ) -> str:
        """Создает событие подтвержденной записи в Google Календаре.

        Args:
            appointment: Объект записи на ремонт.
            post: Объект рабочего поста.
            master_name: Опционально имя мастера.

        Returns:
            Уникальный идентификатор созданного события Google Calendar.

        Raises:
            CalendarServiceError: В случае ошибки API Google.
        """
        post_code: PostCode | None = post.code if post else None
        calendar_id = self._get_calendar_id(post_code)
        event_body = _build_event_body(
            appointment=appointment,
            master_name=master_name,
        )

        try:
            request = self._client.events().insert(
                calendarId=calendar_id,
                body=event_body,
            )
            response = request.execute()
            event_id = response.get('id')
            if not event_id:
                raise CalendarServiceError(
                    'Google API не вернул идентификатор созданного события.',
                )
            return str(event_id)
        except HttpError as exc:
            raise CalendarServiceError(
                f'Ошибка HTTP при создании события в календаре: {exc}',
            ) from exc
        except Exception as exc:
            raise CalendarServiceError(
                f'Не удалось создать событие в Google Календаре: {exc}',
            ) from exc

    async def update_event(
        self,
        event_id: str,
        appointment: Appointment,
        post: Post | None,
        master_name: str | None = None,
    ) -> bool:
        """Обновляет существующее событие в Google Календаре.

        Args:
            event_id: Идентификатор события Google Calendar.
            appointment: Объект записи на ремонт с обновленными данными.
            post: Объект рабочего поста.
            master_name: Опционально имя мастера.

        Returns:
            True в случае успешного обновления.

        Raises:
            CalendarServiceError: В случае ошибки API Google.
        """
        post_code: PostCode | None = post.code if post else None
        calendar_id = self._get_calendar_id(post_code)
        event_body = _build_event_body(
            appointment=appointment,
            master_name=master_name,
        )

        try:
            request = self._client.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event_body,
            )
            request.execute()
            return True
        except HttpError as exc:
            raise CalendarServiceError(
                f'Ошибка HTTP при обновлении события в календаре: {exc}',
            ) from exc
        except Exception as exc:
            raise CalendarServiceError(
                f'Не удалось обновить событие в Google Календаре: {exc}',
            ) from exc

    async def delete_event(
        self,
        event_id: str,
        post_code: PostCode | None = None,
    ) -> bool:
        """Удаляет событие из Google Календаря при отмене записи.

        Args:
            event_id: Идентификатор события Google Calendar.
            post_code: Код поста для определения целевого календаря.

        Returns:
            True в случае успешного удаления.

        Raises:
            CalendarServiceError: В случае ошибки API Google.
        """
        calendar_id = self._get_calendar_id(post_code)
        try:
            request = self._client.events().delete(
                calendarId=calendar_id,
                eventId=event_id,
            )
            request.execute()
            return True
        except HttpError as exc:
            if exc.resp.status == 404:
                return True
            raise CalendarServiceError(
                f'Ошибка HTTP при удалении события из календаря: {exc}',
            ) from exc
        except Exception as exc:
            raise CalendarServiceError(
                f'Не удалось удалить событие из Google Календаря: {exc}',
            ) from exc

    async def clear_all_events(self) -> dict[str, int]:
        """Удаляет все существующие события из всех рабочих календарей сервиса.

        Returns:
            Словарь со статистикой удаленных событий по каждому календарю.

        Raises:
            CalendarServiceError: При критическом сбое обращения к Google API.
        """
        calendar_ids: list[tuple[str, str | None]] = [
            ('P1', self._settings.google_calendar_p1_id),
            ('P2', self._settings.google_calendar_p2_id),
            ('P3', self._settings.google_calendar_p3_id),
            ('P4', self._settings.google_calendar_p4_id),
            ('Обзорный', self._settings.google_calendar_overview_id),
        ]

        deleted_counts: dict[str, int] = {}
        loop = asyncio.get_running_loop()

        def _purge_calendar(cal_id: str) -> int:
            events_result = (
                self._client.events()
                .list(calendarId=cal_id, maxResults=250)
                .execute()
            )
            items = events_result.get('items', [])
            deleted_count = 0
            for item in items:
                event_id = item.get('id')
                if event_id:
                    try:
                        self._client.events().delete(
                            calendarId=cal_id,
                            eventId=event_id,
                        ).execute()
                        deleted_count += 1
                    except HttpError:
                        pass
            return deleted_count

        for name, cid in calendar_ids:
            if not cid:
                deleted_counts[name] = 0
                continue
            try:
                purged_count = await loop.run_in_executor(
                    None,
                    lambda target_cid=cid: _purge_calendar(target_cid),
                )
                deleted_counts[name] = purged_count
            except Exception as exc:
                raise CalendarServiceError(
                    f'Ошибка при очистке календаря {name}: {exc}',
                ) from exc

        return deleted_counts
