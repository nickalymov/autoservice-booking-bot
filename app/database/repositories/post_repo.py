"""Модуль репозитория рабочих постов автосервиса.

Обеспечивает доступ к физическим и виртуальным постам, проверку доступности,
первичную инициализацию каталога постов и обновление идентификаторов календарей.
"""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import PostCode
from app.database.models.post import Post

_DEFAULT_POSTS_DATA: tuple[dict[str, str | PostCode], ...] = (
    {
        'code': PostCode.P1,
        'name': 'Обычная яма',
        'post_type': 'Яма',
        'description': 'Работы, для которых подходит яма',
    },
    {
        'code': PostCode.P2,
        'name': 'Подъемник 1',
        'post_type': 'Подъемник',
        'description': 'Работы, для которых подходит подъемник',
    },
    {
        'code': PostCode.P3,
        'name': 'Подъемник 2',
        'post_type': 'Подъемник',
        'description': 'Работы, для которых подходит подъемник',
    },
    {
        'code': PostCode.P4,
        'name': 'Яма / сход-развал',
        'post_type': 'Яма со сход-развалом',
        'description': (
            'Сход-развал, а также обычные работы, которым подходит яма'
        ),
    },
    {
        'code': PostCode.NO_POST,
        'name': 'Без поста',
        'post_type': 'Без поста',
        'description': (
            'Мелкие работы без боксов и досрочное освобождение постов'
        ),
    },
)


class PostRepository:
    """Репозиторий для выполнения операций с таблицей рабочих постов.

    Attributes:
        _session: Асинхронная сессия SQLAlchemy для выполнения запросов.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Инициализирует репозиторий с заданной сессией базы данных.

        Args:
            session: Асинхронная сессия базы данных.
        """
        self._session = session

    async def get_by_code(self, code: PostCode) -> Post | None:
        """Возвращает рабочий пост по его системному коду.

        Args:
            code: Системный код поста (P1, P2, P3, P4, NO_POST).

        Returns:
            Найденный объект поста или None, если запись отсутствует.
        """
        stmt = select(Post).where(Post.code == code)
        result = await self._session.scalars(stmt)
        return result.first()

    async def get_by_id(self, post_id: int) -> Post | None:
        """Возвращает рабочий пост по его первичному ключу.

        Args:
            post_id: Первичный ключ поста в базе данных.

        Returns:
            Найденный объект поста или None, если запись отсутствует.
        """
        stmt = select(Post).where(Post.id == post_id)
        result = await self._session.scalars(stmt)
        return result.first()

    async def get_all_active(self) -> Sequence[Post]:
        """Возвращает список всех активных постов сервиса.

        Returns:
            Последовательность активных постов, отсортированная по ID.
        """
        stmt = (
            select(Post)
            .where(Post.is_active.is_(True))
            .order_by(Post.id)
        )
        result = await self._session.scalars(stmt)
        return result.all()

    async def create(
        self,
        code: PostCode,
        name: str,
        post_type: str,
        description: str | None = None,
        is_active: bool = True,
        google_calendar_id: str | None = None,
    ) -> Post:
        """Создает новый рабочий пост в базе данных.

        Args:
            code: Уникальный код поста.
            name: Человекочитаемое наименование поста.
            post_type: Физическая категория поста.
            description: Описание и правила использования.
            is_active: Флаг доступности поста для бронирования.
            google_calendar_id: ID связанного календаря Google.

        Returns:
            Созданный и добавленный в сессию объект поста.
        """
        post = Post(
            code=code,
            name=name,
            post_type=post_type,
            description=description,
            is_active=is_active,
            google_calendar_id=google_calendar_id,
        )
        self._session.add(post)
        await self._session.flush()
        return post

    async def ensure_default_posts(self) -> None:
        """Создает базовые посты автосервиса по ТЗ, если они отсутствуют."""
        for item in _DEFAULT_POSTS_DATA:
            post_code = item['code']
            if not isinstance(post_code, PostCode):
                continue
            existing_post = await self.get_by_code(post_code)
            if existing_post is None:
                await self.create(
                    code=post_code,
                    name=str(item['name']),
                    post_type=str(item['post_type']),
                    description=str(item['description']),
                    is_active=True,
                )

    async def update_calendar_id(
        self,
        post_id: int,
        google_calendar_id: str | None,
    ) -> Post | None:
        """Обновляет привязку Google Календаря для указанного поста.

        Args:
            post_id: Первичный ключ поста.
            google_calendar_id: Новый идентификатор Google Календаря.

        Returns:
            Обновленный объект поста или None, если он не найден.
        """
        post = await self.get_by_id(post_id)
        if post is not None:
            post.google_calendar_id = google_calendar_id
            await self._session.flush()
        return post
