import datetime

from tortoise.models import Model
from tortoise import fields


class FeedBack(Model):
    """
    Модель обратной связи.

    Атрибуты:
    - id (int): Уникальный номер пользователя.
    - time_created (datetime.datetime): Дата и время создания записи (автоматически заполняется).
    - from_user (models.User): Ссылка на пользователя, оставившего отзыв (внешний ключ).
    - comment (str): Текстовый комментарий отзыва.
    - stars (int): Количество звезд в отзыве.

    Методы:
    - async def json(self): Возвращает словарь с данными обратной связи.
    """

    id: int = fields.IntField(pk=True)
    time_created: datetime.datetime = fields.DatetimeField(auto_now=True)
    from_user = fields.ForeignKeyField('models.User')
    comment = fields.TextField()
    stars = fields.IntField()

    async def json(self):
        return {
            'id': self.id,
            'time_created': self.time_created,
            'from_user': await (await self.from_user.get()).json(),
            'comment': self.comment,
            'stars': self.stars
        }


class Event(Model):
    """
    Модель события.

    Атрибуты:
    - id (int): Уникальный номер пользователя.
    - time_created (datetime.datetime): Дата и время создания записи (автоматически заполняется).
    - title (str): Заголовок события.
    - description (str): Описание события.
    - photo_path (str): Путь к фотографии события.
    - strat_date (datetime.datetime): Дата и время начала события.
    - end_date (datetime.datetime): Дата и время окончания события.
    - feedbacks (fields.ManyToManyField): Связь многие ко многим с моделью FeedBack.

    Методы:
    - async def get_feedbacks(self): Получает список отзывов для события.
    - async def json(self): Возвращает словарь с данными события.
    """

    id: int = fields.IntField(pk=True)
    time_created: datetime.datetime = fields.DatetimeField(auto_now=True)
    title = fields.CharField(max_length=100)
    description = fields.TextField()
    photo_path = fields.CharField(max_length=200)
    strat_date = fields.DatetimeField()
    end_date = fields.DatetimeField()
    feedbacks = fields.ManyToManyField('models.FeedBack')

    async def get_feedbacks(self):
        """
        Получает список отзывов для события.

        Возвращает:
        - List[dict]: Список словарей с данными обратной связи.
        """
        
        data = []
        feeds = await self.feedbacks.all()
        for feed in feeds:
            data.append(await feed.json())

        return data

    async def json(self):
        """
        Возвращает словарь с данными события.

        Возвращает:
        - dict: Словарь с данными события.
        """

        feeds = await self.get_feedbacks()
        return {
            'id': self.id,
            'time_created': self.time_created,
            'title': self.title,
            'description': self.description,
            'photo_path': self.photo_path,
            'strat_date': self.strat_date,
            'end_date': self.end_date,
            'feedbacks': feeds,
            "feedbacks_count": len(feeds)
        }
