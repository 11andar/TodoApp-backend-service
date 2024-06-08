from datetime import date
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TodoItem(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    priority = Column(Integer, default=0, nullable=False)
    done = Column(Boolean, default=False)
    due_date = Column(Date, default=date.today)

    def __repr__(self):
        return f"""Title: {self.title}, Due date: {self.due_date}"""
