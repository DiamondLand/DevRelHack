from fastapi import HTTPException

class ErrorFeedBackForMe(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail={
            'code': 5,
            'message': 'You cannot leave a review for yourself',
            'ru_message': 'Bы не можете оставить отзыв себе'
        })