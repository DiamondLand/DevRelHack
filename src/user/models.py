from tortoise.models import Model
from tortoise import fields
import bcrypt, datetime, random



class User(Model):
    id: int = fields.IntField(pk=True)                                      # Уникальный Номер пользователя
    is_admin: bool = fields.BooleanField(default=False)                     # Является ли пользователь администратором сайта
    time_created: datetime.datetime = fields.DatetimeField(auto_now=True)   # Время и дата создания аккаунта
    
    username: str = fields.CharField(max_length=60, unique=True)            # Псевдоним пользователя
    first_name: str = fields.CharField(max_length=60)                       # Имя
    middle_name: str = fields.CharField(max_length=60)                     
    last_name: str = fields.CharField(max_length=60)                        # Фамилия
    email: str = fields.CharField(max_length=60, unique=True)               # Электронная почта
    password: str = fields.CharField(max_length=100)                       # Пароль
    
    photo = fields.CharField(max_length=200)
    
    age = fields.DatetimeField()
    sex: str = fields.CharField(max_length=10)
    work: str = fields.CharField(max_length=50)
    country: str = fields.CharField(max_length=100)
    
    events = fields.ManyToManyField('models.Event')
    
    async def set_photo(self):
        index: int = random.randint(1, 10)
        self.photo = f'/static/images/avatars/{index}.png'
    
    async def set_password(self, password: str) -> None:
        """
        Sets the password of the user.

        Args:
            password (str): The password to set.
        """
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    async def check_password(self, password: str) -> bool:
        """
        Checks the password of the user.

        Args:
            password (str): The password to check.

        Returns:
            bool: A boolean indicating whether the password is correct.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    async def get_events(self):
        data = []
        events = await self.events.all()
        for event in events:
            data.append(await event.json())
            
        return data
    
    async def get_events_count(self):
        return len(await self.get_events())
    
    async def get_feedbacks_count(self):
        count = 0
        for event in await self.events.all():
            count += len(await event.feedbacks.all())
        return count
    
    async def get_feedback_mean_star(self):
        count = 0
        feeds = await self.get_feedbacks_count()
        if feeds == 0:
            return 0
        for event in await self.events.all():
            for feed in await event.feedbacks.all():
                count += feed.stars
        return count / feeds
    
    async def get_old(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        print(int((now - self.age).days / 365))
        return int((now - self.age).days / 365)
    async def json(self) -> dict:
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
            'sex': self.sex,
            'work': self.work,
            'country': self.country
        }
        