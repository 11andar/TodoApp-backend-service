from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database import Base


def set_end_of_current_day() -> datetime:
    current_day = datetime.utcnow()
    return current_day.replace(hour=23, minute=59, second=59)


class TodoItem(Base):
    __tablename__ = 'todo_items'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, default=None)
    priority = Column(Integer, default=0, nullable=False)
    done = Column(Boolean, default=False)
    due_date = Column(DateTime, default=set_end_of_current_day)

    def __repr__(self):
        return f"""Title: {self.title}, Due date: {self.due_date}"""
