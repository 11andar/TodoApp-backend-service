import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.models import TodoItem
from app.schemas import TodoBase, TodoUpdate
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
    assert created_todo.title == "Test Todo"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(created_todo)


def test_get_todo_item(mock_db):
    todo_item = TodoItem(title="Test Todo", id=1)
    mock_db.query.return_value.filter.return_value.first.return_value = todo_item
    result = get_todo_item(mock_db, 1)
    assert result == todo_item


def test_get_todo_item_not_found(mock_db):
    todo_item = None
    mock_db.query.return_value.filter.return_value.first.return_value = todo_item
    result = get_todo_item(mock_db, 1)
    assert result == todo_item


def test_get_todos(mock_db):
    todos = [TodoItem(title="Test Todo", id=i) for i in range(10)]
    mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = todos
    result = get_todos(mock_db)
    assert result == todos


def test_get_todos_offset_limit(mock_db):
    todos = [TodoItem(title="Test Todo", id=i) for i in range(10)]
    offset = 2
    limit = 3
    expected_result = todos[offset:offset + limit]
    mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = expected_result
    result = get_todos(mock_db, offset, limit)
    assert [todo for todo in result] == [todo for todo in expected_result]


def test_get_todos_offset_exceeds(mock_db):
    offset = 16
    expected_result = []
    mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = expected_result
    result = get_todos(mock_db, offset)
    assert result == expected_result


def test_update_todo(mock_db):
    todo_item = TodoItem(id=1, title="Test Title", description="Test Description")
    mock_db.query.return_value.filter.return_value.first.return_value = todo_item
    todo_update = TodoUpdate(title="Update Title", description="Update Description")
    updated_todo = update_todo(mock_db, 1, todo_update)
    assert updated_todo.title == "Update Title"
    assert updated_todo.description == "Update Description"


def test_update_todo_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    todo_update = TodoUpdate(title="Update Title", description="Update Description")
    updated_todo = update_todo(mock_db, 1, todo_update)
    assert updated_todo is None
