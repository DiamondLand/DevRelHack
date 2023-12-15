import datetime
from fastapi import APIRouter, Request, Depends
from user import models, depends, utils
from user.oauth import utils as oauth_utils, exceptions as oauth_exceptions

v1 = APIRouter(prefix='/user', tags=['user'])


@v1.post('/me')
async def me(request: Request, user: models.User = Depends(depends.get_user)):
    """
    Получает информацию о текущем пользователе.

    :param request: Запрос FastAPI.
    :param user: Пользователь (зависимость).

    :return: Информация о текущем пользователе в формате JSON.
    """
    
    return await user.json()


@v1.get('/users')
async def get_users(request: Request, user: models.User = Depends(depends.get_user)):
    """
    Получает список пользователей (кроме текущего пользователя).

    :param request: Запрос FastAPI.
    :param user: Пользователь (зависимость).

    :return: Список пользователей в формате JSON.
    """

    users = []
    users_db = await models.User.all()
    for user_db in users_db:
        if user_db.username != user.username:
            users.append(await user_db.json())
    return users


@v1.post('/user_filter')
async def user_filter(request: Request, user: models.User = Depends(depends.get_user),
                      age_min: int = 0, age_max: int = 100, sex: str = 'all',
                      county: str = 'all', work='all', events_min: int = 0, events_max: int = 99999,
                      feedbacks_min: int = 0, feedbacks_max: int = 9999, star_min: int = 0, star_max: int = 9999):
    """
    Фильтрует пользователей по различным критериям.

    :param request: Запрос FastAPI.
    :param user: Пользователь (зависимость).
    :param age_min: Минимальный возраст пользователя.
    :param age_max: Максимальный возраст пользователя.
    :param sex: Пол пользователя ('all', 'male', 'female').
    :param county: Страна проживания пользователя ('all' для всех стран).
    :param work: Род деятельности пользователя ('all' для всех родов деятельности).
    :param events_min: Минимальное количество событий пользователя.
    :param events_max: Максимальное количество событий пользователя.
    :param feedbacks_min: Минимальное количество отзывов пользователя.
    :param feedbacks_max: Максимальное количество отзывов пользователя.
    :param star_min: Минимальное количество звезд пользователя.
    :param star_max: Максимальное количество звезд пользователя.

    :return: Список пользователей, отфильтрованных по заданным критериям, в формате JSON.
    """

    all_users = await models.User.all()

    users = await utils.filter_user_min_age(all_users, age_min)
    users = await utils.filter_user_max_age(users, age_max)

    if sex != 'all':
        users = await utils.filter_user_sex(users, sex)

    if county != 'all':
        users = await utils.filter_user_county(users, county)

    if work != 'all':
        users = await utils.filter_user_work(users, work)

    users = await utils.filter_user_events(users, events_min, events_max)
    users = await utils.filter_user_feedbacks(users, feedbacks_min, feedbacks_max)
    users = await utils.filter_user_feedback_star(users, star_min, star_max)

    data = []
    for user in users:
        data.append(await user.json())
    return data


@v1.post('/update/username')
async def update_username(request: Request, username: str,
                          user: models.User = Depends(depends.get_user)):
    """
    Обновляет имя пользователя.

    :param request: Объект запроса.
    :param username: Новое имя пользователя.
    :param user: Пользователь, выполняющий обновление.

    :return: Словарь с ключом 'status', указывающим на успешное обновление имени пользователя.
    """

    if await oauth_utils.check_username(username):
        raise oauth_exceptions.ErrorUniqueUsername

    user.username = username
    await user.save()
    return {'status': True}


@v1.post('/update/email')
async def update_email(request: Request, email: str,
                       user: models.User = Depends(depends.get_user)):
    """
    Обновляет электронную почту пользователя.

    :param request: Объект запроса.
    :param email: Новый адрес электронной почты.
    :param user: Пользователь, выполняющий обновление.

    :return: Словарь с ключом 'status', указывающим на успешное обновление адреса электронной почты.
    """

    if await oauth_utils.check_email(email):
        raise oauth_exceptions.ErrorUniqueEmail

    user.email = email
    await user.save()
    return {'status': True}


@v1.post('/update/password')
async def update_password(request: Request, password: str,
                          user: models.User = Depends(depends.get_user)):
    """
    Обновляет пароль пользователя.

    :param request: Объект запроса.
    :param password: Новый пароль пользователя.
    :param user: Пользователь, выполняющий обновление.

    :return: Словарь с ключом 'status', указывающим на успешное обновление пароля пользователя.
    """

    if user.check_password(password):
        user.set_password(password)

        return {
            'status': True,
        }
    return {
        'message': 'Неверный пароль'
    }


@v1.post('/update/first_name')
async def update_first_name(request: Request, first_name: str,
                            user: models.User = Depends(depends.get_user)):
    """
    Обновляет имя пользователя.

    :param request: Объект запроса.
    :param first_name: Новое имя пользователя.
    :param user: Пользователь, выполняющий обновление.

    :return: Словарь с ключом 'status', указывающим на успешное обновление имени пользователя.
    """

    user.first_name = first_name
    await user.save()
    return {'status': True}


@v1.post('/update/last_name')
async def update_last_name(request: Request, last_name: str,
                           user: models.User = Depends(depends.get_user)):
    """
    Обновляет фамилию пользователя.

    :param request: Объект запроса.
    :param last_name: Новая фамилия пользователя.
    :param user: Пользователь, выполняющий обновление.

    :return: Словарь с ключом 'status', указывающим на успешное обновление фамилии пользователя.
    """

    user.last_name = last_name
    await user.save()
    return {'status': True}


@v1.post('/update/middle_name')
async def update_middle_name(request: Request, middle_name: str,
                             user: models.User = Depends(depends.get_user)):
    """
    Обновляет отчество пользователя.

    :param request: Объект запроса.
    :param middle_name: Новое отчество пользователя.
    :param user: Пользователь, выполняющий обновление.

    :return: Словарь с ключом 'status', указывающим на успешное обновление отчества пользователя.
    """

    user.middle_name = middle_name
    await user.save()
    return {'status': True}


@v1.post('/update/age')
async def update_age(request: Request, age: datetime.datetime,
                     user: models.User = Depends(depends.get_user)):
    """
    Обновляет возраст пользователя.

    :param request: Объект запроса.
    :param age: Новый возраст пользователя.
    :param user: Пользователь, выполняющий обновление.

    :return: Словарь с ключом 'status', указывающим на успешное обновление возраста пользователя.
    """

    user.age = age
    await user.save()
    return {'status': True}


@v1.post('/update/sex')
async def update_sex(request: Request, sex: str,
                     user: models.User = Depends(depends.get_user)):
    """
    Обновляет пол пользователя.

    :param request: Объект запроса.
    :param sex: Новый пол пользователя.
    :param user: Пользователь, выполняющий обновление.

    :return: Словарь с ключом 'status', указывающим на успешное обновление пола пользователя.
    """

    user.sex = sex
    await user.save()
    return {'status': True}


@v1.post('/update/county')
async def update_county(request: Request, county: str,
                        user: models.User = Depends(depends.get_user)):
    """
    Обновляет страну пользователя.

    :param request: Объект запроса.
    :param county: Новая страна пользователя.
    :param user: Пользователь, выполняющий обновление.

    :return: Словарь с ключом 'status', указывающим на успешное обновление страны пользователя.
    """

    user.country = county
    await user.save()
    return {'status': True}


@v1.post('/user_profile')
async def get_user_profile(request: Request, user_id: int,
                           user: models.User = Depends(depends.get_user)):
    """
    Получает профиль пользователя.

    :param request: Объект запроса.
    :param user_id: Идентификатор пользователя, чей профиль нужно получить.
    :param user: Пользователь, выполняющий запрос.

    :return: JSON-представление профиля пользователя.
    """
    db_user = await models.User.get(id=user_id)
    return await db_user.json()

