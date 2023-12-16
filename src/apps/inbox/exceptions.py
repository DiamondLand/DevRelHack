from fastapi import HTTPException

class ErrorMessageNotFound(HTTPException):
    """
    Исключение, вызываемое при отсутствии сообщения.

    Атрибуты:
    - status_code (int): Код состояния HTTP (404 Not Found).
    - detail (dict): Детали ошибки, включая код и сообщение на английском и русском.
    """

    def __init__(self):
        super().__init__(status_code=404, detail={
            'code': 9,
            'message': 'Message not found',
            'ru_message': 'Сообщение не найдено'
        })
