from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

client = APIRouter()

templates = Jinja2Templates(directory="public/templates")