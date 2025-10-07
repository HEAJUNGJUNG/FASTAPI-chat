from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.todo import models, schemas
from app.auth.models import User

router = APIRouter(prefix="/todo", tags=["Todo"])

@router.post("/", response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_todo = models.Todo(**todo.dict(), user_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/", response_model=List[schemas.TodoResponse])
def get_todos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todos = db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()
    return todos

@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, todo_update: schemas.TodoUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    for key, value in todo_update.dict(exclude_unset=True).items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"detail": "Todo deleted"}
