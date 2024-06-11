import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.models import TodoItem
from app.schemas import TodoBase
from app.crud import (
    create_todo,
    get_todo_item,
    get_todos,
    update_todo,
    delete_todo
)


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)
