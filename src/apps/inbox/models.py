from tortoise.models import Model
from tortoise import fields
import datetime

class File(Model):
    id: int = fields.IntField(pk=True)                                      # Уникальный Номер пользователя
    time_created: datetime.datetime = fields.DatetimeField(auto_now=True)
    file_path = fields.CharField(max_length=200)
    
    async def json(self):
        return {
            'id': self.id,
            'time_created': self.time_created,
            'file_path': self.file_path
        }

class Message(Model):
    id: int = fields.IntField(pk=True)                                      # Уникальный Номер пользователя
    time_created: datetime.datetime = fields.DatetimeField(auto_now=True)
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    files = fields.ManyToManyField('models.File')
    from_user = fields.ForeignKeyField('models.User',related_name='from_user')
    to_user = fields.ForeignKeyField('models.User', related_name='to_user')
    
    viewed = fields.BooleanField(default=False)
    
    async def get_files(self):
        data = []
        file_instances = await self.files.all()
        for file_instance in file_instances:
            data.append(await file_instance.json())
        return data
    
    async def json(self):
        files = await self.get_files()
        return {
            'id': self.id,
            'time_created': self.time_created,
            'title': self.title,
            'content': self.content,
            'files': files,
            'from_user': await (await self.from_user.get()).json(),
            'to_user': await (await self.to_user.get()).json(),
            'viewed': self.viewed
        }