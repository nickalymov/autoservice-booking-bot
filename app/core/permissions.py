"""Модуль правил разграничения прав доступа автосервиса.

Определяет матрицу полномочий ролей Владельца, Мастера и Магазина
в соответствии с требованиями раздела 4 технического задания.
"""

from app.config import UserRole
from app.database.models import Appointment
from app.database.models import User


def can_manage_appointment(
    user: User,
    appointment: Appointment,
) -> bool:
    """Проверяет право сотрудника на управление статусом и данными записи.

    Args:
        user: Объект авторизованного сотрудника.
        appointment: Проверяемая запись на ремонт.

    Returns:
        True, если действие разрешено, иначе False.
    """
    if not user.is_active:
        return False
    if user.role in (UserRole.OWNER, UserRole.SALES):
        return True
    if user.role == UserRole.MECHANIC:
        return appointment.master_id == user.id
    return False


def can_transfer_appointment(
    user: User,
    appointment: Appointment,
) -> bool:
    """Проверяет право сотрудника инициировать передачу записи коллеге.

    Args:
        user: Инициатор передачи.
        appointment: Передаваемая запись на ремонт.

    Returns:
        True, если сотрудник вправе передать запись, иначе False.
    """
    if not user.is_active:
        return False
    if user.role in (UserRole.OWNER, UserRole.SALES):
        return True
    if user.role == UserRole.MECHANIC:
        return appointment.master_id == user.id
    return False


def can_force_modify(user: User) -> bool:
    """Проверяет право на принудительное изменение чужих записей.

    Args:
        user: Проверяемый сотрудник.

    Returns:
        True для владельца и продавцов магазина, иначе False.
    """
    return user.is_active and user.role in (
        UserRole.OWNER,
        UserRole.SALES,
    )


def can_manage_users(user: User) -> bool:
    """Проверяет право на управление списком пользователей и ролями.

    Args:
        user: Проверяемый сотрудник.

    Returns:
        True только для владельца автосервиса, иначе False.
    """
    return user.is_active and user.role == UserRole.OWNER
