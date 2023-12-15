from fastapi import APIRouter, Request
from user.oauth.api.v1.controller import oauth

user_auth = APIRouter()
user_auth.include_router(oauth, prefix='/oauth', tags=['auth'])