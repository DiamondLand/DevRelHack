from pydantic import BaseModel
import datetime

class SignUpModel(BaseModel):
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
    email: str
    password: str
    
class SignUpReturn(BaseModel):
    status: bool
    user_id: int
    
class SignInReturn(BaseModel):
    token: str