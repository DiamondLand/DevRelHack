from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from core.db import init_db
from client.controller import client
from user.controller import user
from apps.activity.api.v1.controller import v1 as activity
from apps.inbox.api.v1.controller import v1 as inbox

app = FastAPI()

init_db(app)

app.mount("/static", StaticFiles(directory="public/static"), name="static")

app.include_router(client, tags=['Клиентская часть'])
app.include_router(user, tags=['api', 'user'])
app.include_router(activity, tags=['api', 'activity'], prefix='/activity')
app.include_router(inbox, tags=['api', 'inbox'], prefix='/inbox')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
