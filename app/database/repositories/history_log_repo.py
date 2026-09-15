"""Модуль репозитория журнала аудита и истории изменений записей.

Обеспечивает фиксацию событий над заявками, выборку хронологии действий
по конкретной записи и получение журнала последних операций.
"""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database.models.history_log import HistoryActionType
from app.database.models.history_log import HistoryLog


class HistoryLogRepository:
    """Репозиторий для выполнения операций с таблицей журнала аудита.

    Attributes:
        _session: Асинхронная сессия SQLAlchemy для выполнения запросов.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Инициализирует репозиторий с заданной сессией базы данных.

        Args:
            session: Асинхронная сессия базы данных.
        """
        self._session = session

    async def log_action(
        self,
        appointment_id: int,
        action_type: HistoryActionType,
        user_id: int | None = None,
        field_name: str | None = None,
        old_value: str | None = None,
        new_value: str | None = None,
        comment: str | None = None,
    ) -> HistoryLog:
        """Создает и фиксирует запись действия в журнале аудита.

        Args:
            appointment_id: Первичный ключ связанной записи на ремонт.
            action_type: Категория совершаемого действия.
            user_id: Опциональный ID пользователя, выполнившего действие.
            field_name: Опциональное имя изменившегося атрибута.
            old_value: Опциональное предыдущее значение атрибута.
            new_value: Опциональное новое значение атрибута.
            comment: Опциональный текстовый комментарий к событию.

        Returns:
            Созданный и добавленный в сессию объект журнала аудита.
        """
        log_entry = HistoryLog(
            appointment_id=appointment_id,
            user_id=user_id,
            action_type=action_type,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            comment=comment,
        )
        self._session.add(log_entry)
        await self._session.flush()
        return log_entry

    async def get_by_appointment_id(
        self,
        appointment_id: int,
    ) -> Sequence[HistoryLog]:
        """Возвращает историю изменений для указанной заявки.

        Args:
            appointment_id: Первичный ключ записи на ремонт.

        Returns:
            Последовательность записей аудита, отсортированная по времени.
        """
        stmt = (
            select(HistoryLog)
            .options(joinedload(HistoryLog.user))
            .where(HistoryLog.appointment_id == appointment_id)
            .order_by(HistoryLog.created_at.asc())
        )
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_recent_logs(
        self,
        limit: int = 50,
    ) -> Sequence[HistoryLog]:
        """Возвращает последние события аудита в системе.

        Args:
            limit: Максимальное количество возвращаемых записей.

        Returns:
            Последовательность недавних событий журнала аудита.
        """
        stmt = (
            select(HistoryLog)
            .options(
                joinedload(HistoryLog.user),
                joinedload(HistoryLog.appointment),
            )
            .order_by(HistoryLog.created_at.desc())
            .limit(limit)
        )
        result = await self._session.scalars(stmt)
        return result.all()
