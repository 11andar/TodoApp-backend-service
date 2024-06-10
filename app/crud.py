from sqlalchemy.orm import Session
from models import TodoItem
from schemas import TodoCreate, TodoUpdate


def create_todo(db: Session, todo: TodoCreate) -> TodoItem:
    db_item = TodoItem(**todo.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_todo_item(db: Session, id: int) -> TodoItem:
    return db.query(TodoItem).filter(TodoItem.id == id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 10) -> list[TodoItem]:
    return db.query(TodoItem).offset(skip).limit(limit).all()
