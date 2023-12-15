from user.models import User
from core import providers
from user import exceptions
from fastapi import Depends


async def get_user(token: str) -> User:
    """
    Получает пользователя по токену.

    :param token: JWT токен.

    :return: Объект пользователя.
    """
    return await User.get(
        id=(
            await providers.JWTProvider.decode(
                token=token
            )
        ).get('user_id')
    )


async def get_user_by_username(username: str) -> User:
    """
    Получает пользователя по имени пользователя.

    :param username: Имя пользователя.

    :return: Объект пользователя.
    """
    user = await User.filter(username=username).first()
    if not user:
        raise exceptions.ErrorUsernameNotFound
    return user


async def admin_user(user: User = Depends(get_user)) -> User:
    """
    Проверяет, является ли пользователь администратором.

    :param user: Объект пользователя (зависимость).

    :return: Объект пользователя, если он администратор.

    :raise: Ошибка, если пользователь не администратор.
    """
    if user.is_admin:
        return user
    raise exceptions.ErrorUserNotAdmin
