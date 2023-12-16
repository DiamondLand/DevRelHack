from fastapi import HTTPException

class ErrorUsernameNotFound(HTTPException):
    """
    Исключение, сигнализирующее о том, что пользователь с указанным именем пользователя не найден.
    """
    def __init__(self):
        super().__init__(status_code=404, detail={
            'code': 7,
            'message': 'User not found',
            'ru_message': 'Пользователь не найден'
        })

class ErrorUserNotAdmin(HTTPException):
    """
    Исключение, сигнализирующее о том, что пользователь не явялется администратором.
    """
    def __init__(self):
        super().__init__(status_code=404, detail={
            'code': 8,
            'message': 'You are not administrator',
            'ru_message': 'Вы не являетесь администратором'
        })

