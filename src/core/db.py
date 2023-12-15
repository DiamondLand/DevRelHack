from tortoise.contrib.fastapi import register_tortoise

def init_db(app):
    register_tortoise(
        app,
        db_url='sqlite://database.db',
        modules={'models': ['user.models', 'apps.activity.models', 'apps.inbox.models']},
        generate_schemas=True,
        add_exception_handlers=True
    )