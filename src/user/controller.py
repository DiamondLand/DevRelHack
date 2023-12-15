from fastapi import APIRouter, Request
from user.oauth.controller import user_auth
from user.api.v1.controller import v1
from user.api.v1.admin import v1 as v1_admin

user = APIRouter()
user.include_router(user_auth)
user.include_router(v1)
user.include_router(v1_admin)