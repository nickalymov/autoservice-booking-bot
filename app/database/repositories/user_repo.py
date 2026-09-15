"""Модуль репозитория сотрудников и пользователей автосервиса.

Обеспечивает доступ к базе данных для проверки прав доступа,
получения списков мастеров, регистрации, управления ролями и настройками.
"""

from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import UserRole
from app.database.models.user import User

_DEFAULT_STAFF: tuple[dict[str, str | int | UserRole], ...] = (
    {
        'telegram_id': 1001,
        'full_name': 'Вова',
        'role': UserRole.MECHANIC,
    },
    {
        'telegram_id': 1002,
        'full_name': 'Коля',
        'role': UserRole.MECHANIC,
    },
    {
        'telegram_id': 1003,
        'full_name': 'Рамазан',
        'role': UserRole.MECHANIC,
    },
)


class UserRepository:
    """Репозиторий для выполнения операций с таблицей пользователей.

    Attributes:
        _session: Асинхронная сессия SQLAlchemy для выполнения запросов.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Инициализирует репозиторий с заданной сессией базы данных.

        Args:
            session: Асинхронная сессия базы данных.
        """
        self._session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Возвращает пользователя по его идентификатору Telegram.

        Args:
            telegram_id: Идентификатор пользователя в Telegram.

        Returns:
            Найденный пользователь или None, если запись отсутствует.
        """
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self._session.scalars(stmt)
        return result.first()

    async def get_by_id(self, user_id: int) -> User | None:
        """Возвращает пользователя по первичному ключу базы данных.

        Args:
            user_id: Первичный ключ пользователя.

        Returns:
            Найденный пользователь или None, если запись отсутствует.
        """
        stmt = select(User).where(User.id == user_id)
        result = await self._session.scalars(stmt)
        return result.first()

    async def find_mechanic_by_name(self, name_query: str) -> User | None:
        """Ищет активного мастера по подстроке имени.

        Args:
            name_query: Имя или фрагмент имени мастера.

        Returns:
            Объект найденного мастера или None.
        """
        pattern = f'%{name_query.strip()}%'
        stmt = select(User).where(
            User.role == UserRole.MECHANIC,
            User.is_active.is_(True),
            User.full_name.ilike(pattern),
        )
        result = await self._session.scalars(stmt)
        return result.first()

    async def get_active_mechanics(
        self,
        exclude_telegram_id: int | None = None,
    ) -> Sequence[User]:
        """Возвращает список всех активных мастеров автосервиса.

        Args:
            exclude_telegram_id: Опциональный ID для исключения из списка.

        Returns:
            Последовательность активных мастеров, отсортированная по имени.
        """
        stmt = select(User).where(
            User.role == UserRole.MECHANIC,
            User.is_active.is_(True),
        )
        if exclude_telegram_id is not None:
            stmt = stmt.where(User.telegram_id != exclude_telegram_id)
        stmt = stmt.order_by(User.full_name)
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_all_active_users(self) -> Sequence[User]:
        """Возвращает всех активных сотрудников независимо от роли.

        Returns:
            Последовательность активных пользователей сервиса.
        """
        stmt = (
            select(User)
            .where(User.is_active.is_(True))
            .order_by(User.full_name)
        )
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_all_users(self) -> Sequence[User]:
        """Возвращает полный список всех сотрудников сервиса.

        Returns:
            Последовательность всех зарегистрированных сотрудников.
        """
        stmt = select(User).order_by(User.id.asc())
        result = await self._session.scalars(stmt)
        return result.all()

    async def create(
        self,
        telegram_id: int,
        full_name: str,
        role: UserRole = UserRole.MECHANIC,
        is_active: bool = True,
        reminders_enabled: bool = True,
    ) -> User:
        """Создает нового сотрудника в базе данных.

        Args:
            telegram_id: Идентификатор Telegram.
            full_name: Полное имя или псевдоним.
            role: Назначаемая системная роль.
            is_active: Флаг активности аккаунта.
            reminders_enabled: Флаг отправки напоминаний.

        Returns:
            Созданный и добавленный в сессию объект пользователя.
        """
        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
            role=role,
            is_active=is_active,
            reminders_enabled=reminders_enabled,
        )
        self._session.add(user)
        await self._session.flush()
        return user

    async def upsert_user(
        self,
        telegram_id: int,
        full_name: str,
        role: UserRole,
    ) -> User:
        """Создает сотрудника или обновляет существующего.

        Args:
            telegram_id: Идентификатор Telegram пользователя.
            full_name: Имя сотрудника.
            role: Назначаемая роль.

        Returns:
            Созданный или обновленный объект пользователя.
        """
        existing = await self.get_by_telegram_id(telegram_id)
        if existing is not None:
            existing.full_name = full_name
            existing.role = role
            existing.is_active = True
            await self._session.flush()
            return existing

        return await self.create(
            telegram_id=telegram_id,
            full_name=full_name,
            role=role,
            is_active=True,
            reminders_enabled=True,
        )

    async def toggle_active(self, telegram_id: int) -> User | None:
        """Инвертирует статус активности учетной записи сотрудника.

        Args:
            telegram_id: Идентификатор Telegram пользователя.

        Returns:
            Обновленный объект пользователя или None, если он не найден.
        """
        user = await self.get_by_telegram_id(telegram_id)
        if user is not None:
            user.is_active = not user.is_active
            await self._session.flush()
        return user

    async def update_role(
        self,
        user_id: int,
        role: UserRole,
    ) -> User | None:
        """Обновляет системную роль сотрудника.

        Args:
            user_id: Первичный идентификатор пользователя в базе данных.
            role: Новая системная роль сотрудника.

        Returns:
            Обновленный объект пользователя или None, если он не найден.
        """
        user = await self.get_by_id(user_id)
        if user is not None:
            user.role = role
            await self._session.flush()
        return user

    async def delete_user(self, user_id: int) -> bool:
        """Удаляет сотрудника из базы данных.

        Args:
            user_id: Первичный идентификатор пользователя в базе данных.

        Returns:
            True, если сотрудник был удален, иначе False.
        """
        user = await self.get_by_id(user_id)
        if user is None:
            return False
        stmt = delete(User).where(User.id == user_id)
        await self._session.execute(stmt)
        await self._session.flush()
        return True

    async def ensure_whitelist_users(
        self,
        admin_telegram_ids: Sequence[int],
    ) -> None:
        """Гарантирует присутствие администраторов по умолчанию в базе.

        Args:
            admin_telegram_ids: Список доверенных ID администраторов.
        """
        for telegram_id in admin_telegram_ids:
            existing_user = await self.get_by_telegram_id(telegram_id)
            if existing_user is None:
                await self.create(
                    telegram_id=telegram_id,
                    full_name=f'Администратор {telegram_id}',
                    role=UserRole.OWNER,
                    is_active=True,
                    reminders_enabled=True,
                )

    async def ensure_default_staff(self) -> None:
        """Создает базовых мастеров автосервиса по п. 1 ТЗ при их отсутствии."""
        for staff_info in _DEFAULT_STAFF:
            staff_tg_id = int(staff_info['telegram_id'])
            existing_user = await self.get_by_telegram_id(staff_tg_id)
            if existing_user is None:
                role_val = staff_info['role']
                if isinstance(role_val, UserRole):
                    await self.create(
                        telegram_id=staff_tg_id,
                        full_name=str(staff_info['full_name']),
                        role=role_val,
                        is_active=True,
                        reminders_enabled=True,
                    )

    async def update_reminders(
        self,
        telegram_id: int,
        enabled: bool,
    ) -> User | None:
        """Обновляет статус отправки напоминаний для пользователя.

        Args:
            telegram_id: Идентификатор Telegram пользователя.
            enabled: Новое значение флага отправки напоминаний.

        Returns:
            Обновленный объект пользователя или None, если он не найден.
        """
        user = await self.get_by_telegram_id(telegram_id)
        if user is not None:
            user.reminders_enabled = enabled
            await self._session.flush()
        return user
