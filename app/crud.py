from typing import Type
from sqlalchemy.orm import Session
from app.models import TodoItem
from app.schemas import TodoBase, TodoUpdate, TodoDelete


def create_todo(db: Session, todo: TodoBase) -> TodoItem:
    db_item = TodoItem(**todo.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_todo_item(db: Session, todo_id: int) -> TodoItem:
    return db.query(TodoItem).filter(TodoItem.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 10) -> list[Type[TodoItem]]:
    return db.query(TodoItem).offset(skip).limit(limit).all()


def update_todo(db: Session, todo_id: int, todo: TodoUpdate) -> TodoItem:
    db_item = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_item:
        for key, value in todo.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_todo(db: Session, todo_id: int) -> TodoDelete:
    db_item = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
