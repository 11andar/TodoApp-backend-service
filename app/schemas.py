from pydantic import BaseModel, Field, SkipValidation
from datetime import datetime
from typing import Optional
from models import set_end_of_current_day


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 0
    done: bool = False
    due_date: Optional[datetime] = Field(defaul=None, validator=SkipValidation)

    def __init__(self, **data):
        if 'due_date' not in data or data['due_date'] is None:
            data['due_date'] = set_end_of_current_day()
        super().__init__(**data)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class TodoCreate(TodoBase):
    pass


class TodoRead(TodoBase):
    id: int

    class Config:
        orm_mode = True


class TodoUpdate(TodoBase):
    title: Optional[str]
    description: Optional[str] = None
    priority: Optional[int] = 0
    done: Optional[bool] = False
    due_date: Optional[datetime.date] = None


class TodoDelete(TodoBase):
    id: int
    message: str


class TodoResponse(BaseModel):
    data: TodoRead
    success: bool
