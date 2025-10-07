from fastapi import FastAPI, Request
from app.core.database import Base, engine
from app.auth import models as auth_models
from app.todo import models as todo_models
from app.auth import routes as auth_routes
from app.todo import routes as todo_routes
from app.url import routes as url_routes
from app.chat import routes as chat_routes

import os

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
# DB 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FASTAPI CHAT")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR,"static")), name="static")
templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates"))

# Auth 라우터 등록
app.include_router(auth_routes.router)
app.include_router(todo_routes.router)
app.include_router(url_routes.router) 
app.include_router(chat_routes.router)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/login")

@app.get("/login", include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/chat", include_in_schema=False)
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})