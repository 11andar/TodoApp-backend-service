from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean
from database import Base


class TodoItem(Base):
    __tablename__ = 'todo_items'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, default=None)
    priority = Column(Integer, default=0, nullable=False)
    done = Column(Boolean, default=False)

    @staticmethod
    def set_end_of_day():
        current_date = datetime.now()
        return current_date.replace(hour=23, minute=59, second=59).date()

    due_date = Column(Date, default=set_end_of_day)

    def __repr__(self):
        return f"""Title: {self.title}, Due date: {self.due_date}"""
