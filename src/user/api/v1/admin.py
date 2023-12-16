import datetime

from user.oauth import utils as oauth_utils, exceptions as oauth_exceptions
from fastapi import APIRouter, Request, Depends
from user import models, depends, utils
from user.oauth import exceptions

v1 = APIRouter(prefix='/admin', tags=['admin'])


@v1.post('/add_user')
async def create_user(request: Request, username: str,
                      first_name: str, middle_name: str, last_name: str,
                      email: str, password: str,
                      age: datetime.datetime, sex: str,
                      work: str, country: str,
                      user: models.User = Depends(depends.admin_user)):
    """
    Создает нового пользователя с правами администратора.

    :param request: Запрос FastAPI.
    :param username: Имя пользователя.
    :param first_name: Имя пользователя.
    :param middle_name: Отчество пользователя.
    :param last_name: Фамилия пользователя.
    :param email: Электронная почта пользователя.
    :param password: Пароль пользователя.
    :param age: Возраст пользователя (datetime).
    :param sex: Пол пользователя.
    :param work: Род деятельности пользователя.
    :param country: Страна проживания пользователя.
    :param user: Пользователь с правами администратора (зависимость).

    :return: Словарь с информацией о созданном пользователе.
    """

    # Проверка уникальности имени пользователя и электронной почты
    if await utils.check_username(username):
        raise exceptions.ErrorUniqueUsername
    if await utils.check_email(email):
        raise exceptions.ErrorUniqueEmail

    # Создание нового пользователя
    user: models.User = models.User(
        username=username,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        email=email,
        age=age,
        sex=sex,
        work=work,
        country=country
    )

    # Установка пароля и фотографии пользователя
    await user.set_password(password)
    await user.set_photo()
    await user.save()

    return {
        'status': True,
        'user_id': user.id
    }


@v1.post('/update/username')
async def update_username(request: Request, username: str, user_id: int,
                          user: models.User = Depends(depends.admin_user)):
    """
    Обновляет имя пользователя.

    :param request: Объект запроса.
    :param username: Новое имя пользователя.
    :param user_id: Идентификатор пользователя, чье имя будет обновлено.
    :param user: Пользователь, выполняющий обновление (администратор).

    :return: Словарь с ключом 'status', указывающим на успешное обновление имени пользователя.
    """
    
    user = await models.User.get(id=user_id)
    if await oauth_utils.check_username(username):
        raise oauth_exceptions.ErrorUniqueUsername

    user.username = username
    await user.save()
    return {'status': True}


@v1.post('/update/email')
async def update_email(request: Request, email: str, user_id: int,
                       user: models.User = Depends(depends.admin_user)):
    """
    Обновляет электронную почту пользователя.

    :param request: Объект запроса.
    :param email: Новый адрес электронной почты.
    :param user_id: Идентификатор пользователя, чья почта будет обновлена.
    :param user: Пользователь, выполняющий обновление (администратор).

    :return: Словарь с ключом 'status', указывающим на успешное обновление адреса электронной почты.
    """
    
    user = await models.User.get(id=user_id)
    if await oauth_utils.check_email(email):
        raise oauth_exceptions.ErrorUniqueEmail

    user.email = email
    await user.save()
    return {'status': True}


@v1.post('/update/first_name')
async def update_first_name(request: Request, first_name: str, user_id: int,
                            user: models.User = Depends(depends.admin_user)):
    """
    Обновляет имя пользователя.

    :param request: Объект запроса.
    :param first_name: Новое имя пользователя.
    :param user_id: Идентификатор пользователя, чье имя будет обновлено.
    :param user: Пользователь, выполняющий обновление (администратор).

    :return: Словарь с ключом 'status', указывающим на успешное обновление имени пользователя.
    """

    user = await models.User.get(id=user_id)
    user.first_name = first_name
    await user.save()
    return {'status': True}


@v1.post('/update/last_name')
async def update_last_name(request: Request, last_name: str, user_id: int,
                           user: models.User = Depends(depends.admin_user)):
    """
    Обновляет фамилию пользователя.

    :param request: Объект запроса.
    :param last_name: Новая фамилия пользователя.
    :param user_id: Идентификатор пользователя, чья фамилия будет обновлена.
    :param user: Пользователь, выполняющий обновление (администратор).

    :return: Словарь с ключом 'status', указывающим на успешное обновление фамилии пользователя.
    """

    user = await models.User.get(id=user_id)
    user.last_name = last_name
    await user.save()
    return {'status': True}


@v1.post('/update/middle_name')
async def update_middle_name(request: Request, middle_name: str, user_id: int,
                             user: models.User = Depends(depends.admin_user)):
    """
    Обновляет отчество пользователя.

    :param request: Объект запроса.
    :param middle_name: Новое отчество пользователя.
    :param user_id: Идентификатор пользователя, чье отчество будет обновлено.
    :param user: Пользователь, выполняющий обновление (администратор).

    :return: Словарь с ключом 'status', указывающим на успешное обновление отчества пользователя.
    """

    user = await models.User.get(id=user_id)
    user.middle_name = middle_name
    await user.save()
    return {'status': True}


@v1.post('/update/age')
async def update_age(request: Request, age: datetime.datetime, user_id: int,
                     user: models.User = Depends(depends.admin_user)):
    """
    Обновляет возраст пользователя.

    :param request: Объект запроса.
    :param age: Новый возраст пользователя.
    :param user_id: Идентификатор пользователя, чей возраст будет обновлен.
    :param user: Пользователь, выполняющий обновление (администратор).

    :return: Словарь с ключом 'status', указывающим на успешное обновление возраста пользователя.
    """

    user = await models.User.get(id=user_id)
    user.age = age
    await user.save()
    return {'status': True}


@v1.post('/update/sex')
async def update_sex(request: Request, sex: str, user_id: int,
                     user: models.User = Depends(depends.admin_user)):
    """
    Обновляет пол пользователя.

    :param request: Объект запроса.
    :param sex: Новый пол пользователя.
    :param user_id: Идентификатор пользователя, чей пол будет обновлен.
    :param user: Пользователь, выполняющий обновление (администратор).

    :return: Словарь с ключом 'status', указывающим на успешное обновление пола пользователя.
    """

    user = await models.User.get(id=user_id)
    user.sex = sex
    await user.save()
    return {'status': True}


@v1.post('/update/county')
async def update_county(request: Request, county: str, user_id: int,
                        user: models.User = Depends(depends.admin_user)):
    """
    Обновляет страну пользователя.

    :param request: Объект запроса.
    :param county: Новая страна пользователя.
    :param user_id: Идентификатор пользователя, чья страна будет обновлена.
    :param user: Пользователь, выполняющий обновление (администратор).

    :return: Словарь с ключом 'status', указывающим на успешное обновление страны пользователя.
    """

    user = await models.User.get(id=user_id)
    user.country = county
    await user.save()
    return {'status': True}

