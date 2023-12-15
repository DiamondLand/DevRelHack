from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

client = APIRouter()

templates = Jinja2Templates(directory="public/templates")

@client.get('/ping')
async def ping(r: Request):
    return templates.TemplateResponse('pong.html', {'request': r, 'ip': r.client.host})

