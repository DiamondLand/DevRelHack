async def filter_user_min_age(users, min_age: str):
    """
    Фильтрует пользователей по минимальному возрасту.

    :param users: Список пользователей для фильтрации.
    :param min_age: Минимальный возраст для фильтрации.

    :return: Список пользователей, удовлетворяющих условию минимального возраста.
    """

    data = []
    for user in users:
        if await user.get_old() > min_age:
            data.append(user)
    return data


async def filter_user_max_age(users, max_age: str):
    """
    Фильтрует пользователей по максимальному возрасту.

    :param users: Список пользователей для фильтрации.
    :param max_age: Максимальный возраст для фильтрации.

    :return: Список пользователей, удовлетворяющих условию максимального возраста.
    """

    data = []
    for user in users:
        if await user.get_old() < max_age:
            data.append(user)
    return data


async def filter_user_sex(users, sex: str):
    """
    Фильтрует пользователей по полу.

    :param users: Список пользователей для фильтрации.
    :param sex: Пол для фильтрации.

    :return: Список пользователей, удовлетворяющих условию пола.
    """

    data = []
    for user in users:
        if user.sex == sex:
            data.append(user)
    return data


async def filter_user_county(users, county: str):
    """
    Фильтрует пользователей по стране проживания.

    :param users: Список пользователей для фильтрации.
    :param county: Страна для фильтрации.

    :return: Список пользователей, удовлетворяющих условию страны проживания.
    """

    data = []
    for user in users:
        if user.county == county:
            data.append(user)
    return data


async def filter_user_work(users, work: str):
    """
    Фильтрует пользователей по роду деятельности.

    :param users: Список пользователей для фильтрации.
    :param work: Род деятельности для фильтрации.

    :return: Список пользователей, удовлетворяющих условию рода деятельности.
    """

    data = []
    for user in users:
        if user.work == work:
            data.append(user)
    return data


async def filter_user_events(users, events_min: int, events_max: int):
    """
    Фильтрует пользователей по количеству участия в событиях.

    :param users: Список пользователей для фильтрации.
    :param events_min: Минимальное количество событий для фильтрации.
    :param events_max: Максимальное количество событий для фильтрации.

    :return: Список пользователей, удовлетворяющих условиям количества событий.
    """
    
    data = []
    for user in users:
        if await user.get_events_count() >= events_min and await user.get_events_count() <= events_max:
            data.append(user)
    return data


async def filter_user_feedbacks(users, feedbacks_min: int, feedbacks_max: int):
    """
    Фильтрует пользователей по количеству оставленных отзывов.

    :param users: Список пользователей для фильтрации.
    :param feedbacks_min: Минимальное количество отзывов для фильтрации.
    :param feedbacks_max: Максимальное количество отзывов для фильтрации.

    :return: Список пользователей, удовлетворяющих условиям количества отзывов.
    """
    
    data = []
    for user in users:
        if await user.get_feedbacks_count() >= feedbacks_min and await user.get_feedbacks_count() <= feedbacks_max:
            data.append(user)
    return data


async def filter_user_feedback_star(users, star_min: int, star_max: int):
    """
    Фильтрует пользователей по средней оценке отзывов.

    :param users: Список пользователей для фильтрации.
    :param star_min: Минимальная средняя оценка для фильтрации.
    :param star_max: Максимальная средняя оценка для фильтрации.

    :return: Список пользователей, удовлетворяющих условиям средней оценки отзывов.
    """
    
    data = []
    for user in users:
        if await user.get_feedback_mean_star() >= star_min and await user.get_feedback_mean_star() <= star_max:
            data.append(user)
    return data
