from user.models import User
from core import providers
from user import exceptions
from fastapi import Depends
async def get_user(token: str) -> User:

    return await User.get(
        id=(
            await providers.JWTProvider.decode(
                token=token
            )
        ).get('user_id')
    )
    
async def get_user_by_username(username: str) -> User:
    user = await User.filter(username=username).first()
    if not user:
        raise exceptions.ErrorUsernameNotFound
    return user

async def admin_user(user:User = Depends(get_user)) -> User:
    if user.is_admin:
        return user
    raise