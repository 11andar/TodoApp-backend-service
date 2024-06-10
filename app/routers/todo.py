from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.TodoRead)
async def create_todo_item(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)
