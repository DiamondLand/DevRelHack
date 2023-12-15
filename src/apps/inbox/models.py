from tortoise.models import Model
from tortoise import fields
import datetime


class File(Model):
    """
    Модель файла.

    Атрибуты:
    - id (int): Уникальный номер файла.
    - time_created (datetime.datetime): Дата и время создания файла (автоматически заполняется).
    - file_path (str): Путь к файлу.

    Методы:
    - async def json(self): Возвращает словарь с данными файла.
    """

    id: int = fields.IntField(pk=True)
    time_created: datetime.datetime = fields.DatetimeField(auto_now=True)
    file_path = fields.CharField(max_length=200)

    async def json(self):
        return {
            'id': self.id,
            'time_created': self.time_created,
            'file_path': self.file_path
        }


class Message(Model):
    """
    Модель сообщения.

    Атрибуты:
    - id (int): Уникальный номер сообщения.
    - time_created (datetime.datetime): Дата и время создания сообщения (автоматически заполняется).
    - title (str): Заголовок сообщения.
    - content (str): Содержание сообщения.
    - files (fields.ManyToManyField): Связь многие ко многим с моделью File.
    - from_user (fields.ForeignKeyField): Связь с отправителем сообщения (внешний ключ).
    - to_user (fields.ForeignKeyField): Связь с получателем сообщения (внешний ключ).
    - viewed (bool): Флаг, указывающий, было ли сообщение просмотрено.

    Методы:
    - async def get_files(self): Получает список файлов, прикрепленных к сообщению.
    - async def json(self): Возвращает словарь с данными сообщения.
    """

    id: int = fields.IntField(pk=True)
    time_created: datetime.datetime = fields.DatetimeField(auto_now=True)
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    files = fields.ManyToManyField('models.File')
    from_user = fields.ForeignKeyField('models.User', related_name='from_user')
    to_user = fields.ForeignKeyField('models.User', related_name='to_user')
    viewed = fields.BooleanField(default=False)

    async def get_files(self):
        """
        Получает список файлов, прикрепленных к сообщению.

        Возвращает:
        - List[dict]: Список словарей с данными файлов.
        """

        data = []
        file_instances = await self.files.all()
        for file_instance in file_instances:
            data.append(await file_instance.json())
        return data

    async def json(self):
        """
        Возвращает словарь с данными сообщения.

        Возвращает:
        - dict: Словарь с данными сообщения.
        """
        
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
