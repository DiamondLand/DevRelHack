from tortoise.contrib.fastapi import register_tortoise

def init_db(app):
    """
    Инициализирует базу данных с использованием Tortoise ORM.

    :param app: FastAPI приложение, в котором будет зарегистрирована база данных.
    """
    
    register_tortoise(
        app,
        db_url='sqlite://database.db',
        modules={'models': ['user.models', 'apps.activity.models', 'apps.inbox.models']},
        generate_schemas=True,
        add_exception_handlers=True
    )