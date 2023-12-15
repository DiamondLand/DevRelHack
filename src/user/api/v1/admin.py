from fastapi import APIRouter, Request, Depends
from user import models, depends, utils, exceptions
import datetime, os, uuid

v1 = APIRouter(prefix='/admin', tags=['user'])

@v1.post('/add_user')
async def create_user(request: Request, 
                        username: str,
                        first_name: str,
                        middle_name: str,
                        last_name: str,
                        email: str,
                        password: str,
                        age: datetime.datetime,
                        sex: str,
                        work: str,
                        country: str,
                        user: models.User = Depends(depends.admin_user)):
    if await utils.check_username(username):
        raise exceptions.ErrorUniqueUsername
    if await utils.check_email(email):
        raise exceptions.ErrorUniqueEmail
    
    user: models.User = models.User(
        username = username,
        first_name = first_name,
        middle_name = middle_name,
        last_name = last_name,
        email = email,
        age = age,
        sex = sex,
        work = work,
        country = country
    )
    await user.set_password(password)
    await user.set_photo()
    await user.save()
    
    return {
        'status': True,
        'user_id': user.id
    }
    
