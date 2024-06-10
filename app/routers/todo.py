from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from typing import List

router = APIRouter()


@router.post("/todos/", response_model=schemas.TodoRead)
async def create_todo_item(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)


@router.get("/todos/{todo_id}", response_model=schemas.TodoRead)
async def get_todo_item(todo_id: int, db: Session = Depends(get_db)):
    return crud.get_todo(db=db, todo_id=todo_id)


@router.get("/todos/", response_model=List[schemas.TodoRead])
async def get_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_todos(db=db, skip=skip, limit=limit)
