from user import models
from user.oauth import schemas, utils, exceptions
from core import providers
from tortoise.exceptions import DoesNotExist

async def sign_up(data: schemas.SignUpModel) -> schemas.SignUpReturn:
    """
    Регистрирует нового пользователя.

    :param data: Данные для регистрации нового пользователя (см. schemas.SignUpModel).

    :return: Информация о зарегистрированном пользователе.
    """
    if await utils.check_username(data.username):
        raise exceptions.ErrorUniqueUsername
    if await utils.check_email(data.email):
        raise exceptions.ErrorUniqueEmail

    user: models.User = models.User(
        username=data.username,
        first_name=data.first_name,
        middle_name=data.middle_name,
        last_name=data.last_name,
        email=data.email,
        age=data.age,
        sex=data.sex,
        work=data.work,
        country=data.country
    )
    await user.set_password(data.password)
    await user.set_photo()
    await user.save()

    return {
        'status': True,
        'user_id': user.id
    }


async def sign_in(data: schemas.SignInModel) -> schemas.SignInReturn:
    """
    Авторизует пользователя.

    :param data: Данные для авторизации пользователя (см. schemas.SignInModel).

    :return: Информация о вошедшем пользователе и токен доступа.
    """
    try:
        user: models.User = await models.User.get(email=data.email)
    except DoesNotExist:
        raise exceptions.ErrorUserNotFoundByEmail

    if await user.check_password(data.password):
        return {
            'token': await providers.JWTProvider.encode(payload={
                'user_id': user.id
            })
        }
    raise exceptions.ErrorWrongPassword
