async def filter_user_min_age(users, min_age: str):
    data = []
    for user in users:
        if await user.get_old() > min_age:
            data.append(user)
    return data


async def filter_user_max_age(users, max_age: str):
    data = []
    for user in users:
        if await user.get_old() < max_age:
            data.append(user)
    return data

async def filter_user_sex(users, sex: str):
    data = []
    for user in users:
        if user.sex == sex:
            data.append(user)
    return data

async def filter_user_county(users, county: str):
    data = []
    for user in users:
        if user.county == county:
            data.append(user)
    return data

async def filter_user_work(users, work: str):
    data = []
    for user in users:
        if user.work == work:
            data.append(user)
    return data

async def filter_user_events(users, events_min: int, events_max: int):
    data = []
    for user in users:
        if await user.get_events_count() >= events_min and await user.get_events_count() <= events_max:
            data.append(user)
    return data

async def filter_user_feedbacks(users, feedbacks_min: int, feedbacks_max: int):
    data = []
    for user in users:
        if await user.get_feedbacks_count() >= feedbacks_min and await user.get_feedbacks_count() <= feedbacks_max:
            data.append(user)
    return data

async def filter_user_feedback_star(users, star_min: int, star_max: int):
    data = []
    for user in users:
        if await user.get_feedback_mean_star() >= star_min and await user.get_feedback_mean_star() <= star_max:
            data.append(user)
    return data