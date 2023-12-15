from user import models

async def check_username(username: str) -> bool:
    """
    Проверяет, существует ли пользователь с указанным именем пользователя.

    :param username: Имя пользователя для проверки.

    :return: True, если пользователь существует, иначе False.
    """
    return await models.User.filter(username=username).exists()


async def check_email(email: str) -> bool:
    """
    Проверяет, существует ли пользователь с указанным адресом электронной почты.

    :param email: Адрес электронной почты для проверки.

    :return: True, если пользователь существует, иначе False.
    """
    return await models.User.filter(email=email).exists()
