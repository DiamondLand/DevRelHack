from user import models


async def check_username(username: str):
    return await models.User.filter(username=username).exists()


async def check_email(email: str):
    return await models.User.filter(email=email).exists()