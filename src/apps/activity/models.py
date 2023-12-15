from tortoise.models import Model
from tortoise import fields
import datetime

class FeedBack(Model):
    id: int = fields.IntField(pk=True)                                      # Уникальный Номер пользователя
    time_created: datetime.datetime = fields.DatetimeField(auto_now=True)
    
    from_user = fields.ForeignKeyField('models.User')
    comment = fields.TextField()
    stars = fields.IntField()

    async def json(self):
        return {
            'id': self.id,
            'time_created': self.time_created,
            'from_user': await(await self.from_user.get()).json(),
            'comment': self.comment,
            'stars': self.stars
        }
    
class Event(Model):
    id: int = fields.IntField(pk=True)                                      # Уникальный Номер пользователя
    time_created: datetime.datetime = fields.DatetimeField(auto_now=True)
    
    title = fields.CharField(max_length=100)
    description = fields.TextField()
    photo_path = fields.CharField(max_length=200)
    
    strat_date = fields.DatetimeField()
    end_date = fields.DatetimeField()
    
    feedbacks = fields.ManyToManyField('models.FeedBack')
    
    async def get_feedbacks(self):
        data = []
        feeds = await self.feedbacks.all()
        for feed in feeds:
            data.append(await feed.json())
            
        return data
    
    async def json(self):
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
    
    