import datetime

from fastapi import APIRouter, Request, Depends
from user import models, depends, utils
from user.oauth import exceptions

v1 = APIRouter(prefix='/admin', tags=['user'])


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
