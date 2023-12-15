from fastapi import HTTPException

class ErrorFeedBackForMe(HTTPException):
    """
    Исключение, вызываемое при попытке оставить отзыв самому себе.

    Атрибуты:
    - status_code (int): Код состояния HTTP (409 Conflict).
    - detail (dict): Детали ошибки, включая код и сообщение на английском и русском.
    """

    def __init__(self):
        super().__init__(status_code=409, detail={
            'code': 5,
            'message': 'You cannot leave a review for yourself',
            'ru_message': 'Bы не можете оставить отзыв себе'
        })