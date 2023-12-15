from fastapi import HTTPException

class ErrorUsernameNotFound(HTTPException):
    """
    Исключение, сигнализирующее о том, что пользователь с указанным именем пользователя не найден.
    """
    def __init__(self):
        super().__init__(status_code=404, detail={
            'code': 6,
            'message': 'User not found',
            'ru_message': 'Пользователь не найден'
        })
