from fastapi import HTTPException

class ErrorUniqueUsername(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail={
            'code': 1,
            'message': 'Username already exists',
            'ru_message': 'Пользователь с таким именем уже существует'
        })
class ErrorUniqueEmail(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail={
            'code': 2,
            'message': 'Email already exists',
            'ru_message': 'Пользователь с такой почтой уже существует'
        })
class ErrorUserNotFoundByEmail(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail={
            'code': 3,
            'message': 'user not found by email',
            'ru_message': 'Пользователя с такой почтой не существует'
        })
class ErrorWrongPassword(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail={
            'code': 4,
            'message': 'wrong password',
            'ru_message': 'Пароль не верный'
        })