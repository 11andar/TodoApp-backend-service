from pydantic import BaseModel, Field, SkipValidation
from datetime import datetime
from typing import Optional
from app.models import set_end_of_current_day


class TodoBase(BaseModel):
    title: str = "Todo Item"
    description: Optional[str] = None
    priority: Optional[int] = 0
    done: bool = False
    due_date: Optional[datetime] = Field(default=None, validator=SkipValidation)

    def __init__(self, **data):
        if 'due_date' not in data or data['due_date'] is None:
            data['due_date'] = set_end_of_current_day()
        if 'priority' in data:
            if data['priority'] < 0:
                data['priority'] = 0
            elif data['priority'] > 4:
                data['priority'] = 4
        super().__init__(**data)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class TodoRead(TodoBase):
    id: int


class TodoUpdate(TodoBase):
    title: Optional[str]
    description: Optional[str] = None
    priority: Optional[int] = 0
    done: Optional[bool] = False
    due_date: Optional[datetime.date] = None
