"""Модуль модели записи на ремонт автосервиса.

Определяет сущность заявки на ремонт, фиксацию временных интервалов,
привязку к мастерам и постам, канал создания и хранение базы знаний.
"""

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.models.base import Base
from app.database.models.base import TimestampMixin
from app.schemas.appointment import AppointmentSource
from app.schemas.appointment import AppointmentStatus

if TYPE_CHECKING:
    from app.database.models.history_log import HistoryLog
    from app.database.models.user import User


class Appointment(Base, TimestampMixin):
    """Модель записи автомобиля на ремонт и обслуживание.

    Attributes:
        id: Первичный ключ записи в базе данных.
        public_id: Уникальный публичный номер записи (например B209093036).
        status: Текущий статус жизненного цикла записи.
        source: Канал создания записи (голос, текст, календарь).
        start_datetime: Плановые дата и время начала обслуживания.
        end_datetime: Плановые дата и время окончания обслуживания.
        planned_duration_minutes: Плановая длительность работ в минутах.
        actual_start_datetime: Время фактического взятия автомобиля в работу.
        actual_end_datetime: Фактическое время завершения обслуживания.
        actual_duration_minutes: Фактическая длительность работ в минутах.
        post_id: Внешний ключ назначенного рабочего поста.
        master_id: Внешний ключ ответственного мастера.
        created_by_user_id: Внешний ключ сотрудника, создавшего запись.
        target_master_id: Внешний ключ мастера-получателя при передаче.
        car_model: Марка и модель транспортного средства.
        client_phone: Контактный номер телефона клиента.
        client_name: Имя клиента.
        license_plate: Государственный регистрационный номер автомобиля.
        vin: Идентификационный номер (VIN) транспортного средства.
        work_description: Заявленная неисправность или перечень работ.
        work_items: Структурированный список операций для базы знаний.
        master_comment: Итоговый комментарий мастера по факту работ.
        raw_transcription: Исходный текст голосового сообщения.
        google_calendar_event_id: Идентификатор события в Google Calendar.
        post: Связанный объект рабочего поста.
        master: Связанный объект ответственного мастера.
        created_by: Связанный объект сотрудника, оформившего бронь.
        target_master: Связанный объект мастера, принимающего передачу.
        history_logs: Связанный список записей аудита изменений.
    """

    __tablename__ = 'appointments'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    public_id: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True,
        nullable=False,
    )
    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus, native_enum=False, length=32),
        default=AppointmentStatus.DRAFT,
        index=True,
        nullable=False,
    )
    source: Mapped[AppointmentSource] = mapped_column(
        Enum(AppointmentSource, native_enum=False, length=32),
        default=AppointmentSource.VOICE,
        nullable=False,
    )

    start_datetime: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
        nullable=False,
    )
    end_datetime: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
        nullable=False,
    )
    planned_duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    actual_start_datetime: Mapped[datetime.datetime | None] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=True,
        )
    )
    actual_end_datetime: Mapped[datetime.datetime | None] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=True,
        )
    )
    actual_duration_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    post_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey('posts.id', ondelete='SET NULL'),
        index=True,
        nullable=True,
    )
    master_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id', ondelete='RESTRICT'),
        index=True,
        nullable=False,
    )
    created_by_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False,
    )
    target_master_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
    )

    car_model: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    client_phone: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )
    client_name: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )
    license_plate: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )
    vin: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )

    work_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    work_items: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    master_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    raw_transcription: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    google_calendar_event_id: Mapped[str | None] = mapped_column(
        String(255),
        index=True,
        nullable=True,
    )

    post: Mapped['Post | None'] = relationship(
        back_populates='appointments',
    )
    master: Mapped['User'] = relationship(
        foreign_keys=[master_id],
        back_populates='appointments',
    )
    created_by: Mapped['User'] = relationship(
        foreign_keys=[created_by_user_id],
    )
    target_master: Mapped['User | None'] = relationship(
        foreign_keys=[target_master_id],
    )
    history_logs: Mapped[list['HistoryLog']] = relationship(
        back_populates='appointment',
        cascade='all, delete-orphan',
    )
