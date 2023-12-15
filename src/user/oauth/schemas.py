import datetime
from pydantic import BaseModel


class SignUpModel(BaseModel):
    """
    Модель данных для регистрации нового пользователя.
    """
    username: str
    first_name: str
    middle_name: str
    last_name: str
    email: str
    password: str
    age: datetime.datetime
    sex: str
    work: str
    country: str


class SignInModel(BaseModel):
    """
    Модель данных для авторизации пользователя.
    """
    email: str
    password: str


class SignUpReturn(BaseModel):
    """
    Модель данных, возвращаемых после успешной регистрации пользователя.
    """
    status: bool
    user_id: int


class SignInReturn(BaseModel):
    """
    Модель данных, возвращаемых после успешной авторизации пользователя.
    """
    token: str
