from pydantic import BaseModel
import datetime

class CreateEvent(BaseModel):
    """
    Модель для создания нового события.

    Атрибуты:
    - title (str): Название события.
    - description (str): Описание события.
    - start_date (datetime.datetime): Дата и время начала события.
    - end_date (datetime.datetime): Дата и время окончания события.
    """

    title: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime


class CreateFeedback(BaseModel):
    """
    Модель для создания обратной связи к событию.

    Атрибуты:
    - comment (str): Текстовый комментарий отзыва.
    - starts (int): Количество звезд в отзыве.
    - event_id (int): Уникальный идентификатор события, к которому относится отзыв.
    """

    comment: str
    stars: int
    event_id: int
