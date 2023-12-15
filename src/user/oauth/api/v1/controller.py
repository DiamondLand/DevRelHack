from fastapi import APIRouter, Request
from user.oauth import schemas
from user.oauth.api.v1 import service

oauth = APIRouter()

@oauth.post('/sign-up')
async def sign_up(request: Request, data: schemas.SignUpModel) -> schemas.SignUpReturn:
    return await service.sign_up(data)

@oauth.post('/sign-in')
async def sign_in(request: Request, data: schemas.SignInModel) -> schemas.SignInReturn:
    return await service.sign_in(data)

