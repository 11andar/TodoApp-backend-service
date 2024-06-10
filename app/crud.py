from sqlalchemy.orm import Session
from models import TodoItem
from schemas import TodoCreate, TodoUpdate


def create_todo(db: Session, todo: TodoCreate) -> TodoItem:
    db_item = TodoItem(**todo.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
