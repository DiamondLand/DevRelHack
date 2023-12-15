from fastapi import APIRouter, Request, Depends
from user import models, depends, utils

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
