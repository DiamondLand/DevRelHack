from fastapi import HTTPException

class ErrorMessageNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail={
            'code': 7,
            'message': 'Message not found',
            'ru_message': 'Сообщение не найдено'
        })