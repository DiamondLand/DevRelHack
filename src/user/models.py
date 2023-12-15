import bcrypt
import datetime
import random

from tortoise.models import Model
from tortoise import fields


class User(Model):
    """
    Модель пользователя.

    Attributes:
    - id: Уникальный идентификатор пользователя.
    - is_admin: Флаг, указывающий, является ли пользователь администратором.
    - time_created: Время создания пользователя.
    - username: Имя пользователя.
    - first_name: Имя пользователя.
    - middle_name: Отчество пользователя.
    - last_name: Фамилия пользователя.
    - email: Адрес электронной почты пользователя.
    - password: Хэшированный пароль пользователя.
    - photo: Путь к фотографии пользователя.
    - age: Дата рождения пользователя.
    - sex: Пол пользователя.
    - work: Род деятельности пользователя.
    - country: Страна проживания пользователя.
    - events: Связь с событиями, в которых участвует пользователь.

    Methods:
    - set_photo: Устанавливает случайное фото пользователя.
    - set_password: Устанавливает хэшированный пароль пользователя.
    - check_password: Проверяет, совпадает ли переданный пароль с хэшированным паролем пользователя.
    - get_events: Получает события, в которых участвует пользователь.
    - get_events_count: Получает количество событий, в которых участвует пользователь.
    - get_feedbacks_count: Получает количество отзывов, оставленных пользователем.
    - get_feedback_mean_star: Получает среднюю оценку по отзывам, оставленным пользователем.
    - get_old: Получает возраст пользователя.
    - json: Возвращает объект пользователя в формате JSON.
    """

    id: int = fields.IntField(pk=True) 
    is_admin: bool = fields.BooleanField(default=False)
    time_created: datetime.datetime = fields.DatetimeField(auto_now=True)   
    username: str = fields.CharField(max_length=60, unique=True)            
    first_name: str = fields.CharField(max_length=60)                     
    middle_name: str = fields.CharField(max_length=60)
    last_name: str = fields.CharField(max_length=60)                       
    email: str = fields.CharField(max_length=60, unique=True)               
    password: str = fields.CharField(max_length=100)                       
    photo = fields.CharField(max_length=200)
    age = fields.DatetimeField()
    sex: str = fields.CharField(max_length=10)
    work: str = fields.CharField(max_length=50)
    country: str = fields.CharField(max_length=100)
    events = fields.ManyToManyField('models.Event')

    async def set_photo(self):
        """Устанавливает случайное фото пользователя."""
        index: int = random.randint(1, 10)
        self.photo = f'/static/images/avatars/{index}.png'

    async def set_password(self, password: str) -> None:
        """Устанавливает хэшированный пароль пользователя."""
        self.password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

    async def check_password(self, password: str) -> bool:
        """Проверяет, совпадает ли переданный пароль с хэшированным паролем пользователя."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    async def get_events(self):
        """Получает события, в которых участвует пользователь."""
        data = []
        events = await self.events.all()
        for event in events:
            data.append(await event.json())

        return data

    async def get_events_count(self):
        """Получает количество событий, в которых участвует пользователь."""
        return len(await self.get_events())

    async def get_feedbacks_count(self):
        """Получает количество отзывов, оставленных пользователем."""
        count = 0
        for event in await self.events.all():
            count += len(await event.feedbacks.all())
        return count

    async def get_feedback_mean_star(self):
        """Получает среднюю оценку по отзывам, оставленным пользователем."""
        count = 0
        feeds = await self.get_feedbacks_count()
        if feeds == 0:
            return 0
        for event in await self.events.all():
            for feed in await event.feedbacks.all():
                count += feed.stars
        return count / feeds

    async def get_old(self):
        """Получает возраст пользователя."""
        now = datetime.datetime.now(datetime.timezone.utc)
        return int((now - self.age).days / 365)

    async def json(self) -> dict:
        """Возвращает объект пользователя в формате JSON."""
        return {
            'id': self.id,
            'is_admin': self.is_admin,
            'time_created': self.time_created,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'photo': self.photo,
            'age': self.age,
        }