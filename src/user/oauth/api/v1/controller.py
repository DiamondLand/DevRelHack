from fastapi import APIRouter, Request
from user.oauth import schemas
from user.oauth.api.v1 import service

oauth = APIRouter()


@oauth.post('/sign-up')
async def sign_up(request: Request, data: schemas.SignUpModel) -> schemas.SignUpReturn:
    """
    Регистрирует нового пользователя.

    :param request: Запрос FastAPI.
    :param data: Данные для регистрации нового пользователя.

    :return: Информация о зарегистрированном пользователе.
    """
    return await service.sign_up(data)


@oauth.post('/sign-in')
async def sign_in(request: Request, data: schemas.SignInModel) -> schemas.SignInReturn:
    """
    Авторизует пользователя.

    :param request: Запрос FastAPI.
    :param data: Данные для авторизации пользователя.

    :return: Информация о вошедшем пользователе и токен доступа.
    """
    return await service.sign_in(data)
