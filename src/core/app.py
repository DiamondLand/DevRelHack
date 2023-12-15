from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from core.lines import count as CL
from core.db import init_db
from client.controller import client
from user.controller import user
from apps.activity.api.v1.controller import v1 as activity
from apps.inbox.api.v1.controller import v1 as inbox
from apps.inbox.api.v1.admin import v1 as inbox_admin

app = FastAPI()

# Инициализация базы данных
init_db(app)

# Монтирование статических файлов
app.mount("/static", StaticFiles(directory="public/static"), name="static")

# Включение роутеров
app.include_router(client, tags=['Клиентская часть'])
app.include_router(user, tags=['api', 'user'])
app.include_router(activity, tags=['api', 'activity'], prefix='/activity')
app.include_router(inbox, tags=['api', 'inbox'], prefix='/inbox')
app.include_router(inbox_admin)

# Добавление middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(len(app.routes))
app.title = 'Dev.Rel.Hack.2.0'
app.description = f'''Backend developer tg/vk @allelleo\n
Count of routes: {len(app.routes)}\n
Count of lines: {CL()}\n'''