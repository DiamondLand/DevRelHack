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


class ErrorAlreadyFeedback(HTTPException):
    """
    Исключение, указывающее на то, что пользователь уже оставил отзыв.

    Атрибуты:
    - status_code (int): Код состояния HTTP (409 - конфликт).
    - detail (dict): Словарь с информацией об ошибке.
        - 'code' (int): Код ошибки.
        - 'message' (str): Англоязычное сообщение об ошибке.
        - 'ru_message' (str): Русскоязычное сообщение об ошибке.
    """

    def __init__(self):
        super().__init__(status_code=409, detail={
            'code': 6,
            'message': 'You have already left a review',
            'ru_message': 'Вы уже оставляли отзыв'
        })