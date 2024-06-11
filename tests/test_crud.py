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


def test_create_todo(mock_db):
    todo_data = TodoBase(title="Test Todo")
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    created_todo = create_todo(mock_db, todo_data)

    assert isinstance(created_todo, TodoItem)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(created_todo)
