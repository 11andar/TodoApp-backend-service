from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from typing import List

router = APIRouter()


@router.post("/todos/", response_model=schemas.TodoRead)
async def create_todo_item(todo: schemas.TodoBase, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)


@router.get("/todos/{todo_id}", response_model=schemas.TodoRead)
async def get_todo_item(todo_id: int, db: Session = Depends(get_db)):
    return crud.get_todo_item(db=db, todo_id=todo_id)


@router.get("/todos/", response_model=List[schemas.TodoRead])
async def get_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_todos(db=db, skip=skip, limit=limit)


@router.put("/todos/{todo_id}", response_model=schemas.TodoRead)
async def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_todo(db=db, todo_id=todo_id, todo=todo)
    if db_item:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_item


@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_todo(db=db, todo_id=todo_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted"}
