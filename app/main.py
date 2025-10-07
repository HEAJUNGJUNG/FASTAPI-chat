from fastapi import FastAPI
from app.core.database import Base, engine
from app.auth import models as auth_models
from app.todo import models as todo_models
from app.auth import routes as auth_routes
from app.todo import routes as todo_routes
from app.url import routes as url_routes
from app.chat import routes as chat_routes
from fastapi.staticfiles import StaticFiles
# DB 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Productivity Hub")

# Auth 라우터 등록
app.include_router(auth_routes.router)
app.include_router(todo_routes.router)
app.include_router(url_routes.router)
app.include_router(chat_routes.router)

@app.get("/")
def root():
    return {"msg": "Welcome to Productivity Hub!"}

app.mount("/static", StaticFiles(directory="app/static"), name="static")