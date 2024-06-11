import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.database import Base
from app.models import TodoItem, set_end_of_current_day

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, echo=True)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = LocalSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_set_end_of_current_day(db_session):
    current_day = datetime.utcnow()
    end_of_current_day = current_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    date_returned = set_end_of_current_day()
    assert date_returned == end_of_current_day


def test_todo_item_default(db_session):
    todo_item = TodoItem()
    db_session.add(todo_item)
    db_session.commit()
    assert todo_item.title == "Todo Item"
    assert todo_item.description is None
    assert todo_item.priority == 0
    assert todo_item.done == False
    assert todo_item.due_date.hour == 23
    assert todo_item.due_date.minute == 59
    assert todo_item.due_date.second == 59
    assert todo_item.due_date.microsecond == 999999


def test_todo_item_custom(db_session):
    custom_title = "Custom Title"
    custom_description = "Custom Description"
    custom_priority = 1
    custom_done = True
    custom_due_date = datetime.utcnow().replace(hour=21, minute=37, second=00, microsecond=000000)
    test_item = TodoItem(title=custom_title, description=custom_description,
                         priority=custom_priority, done=custom_done, due_date=custom_due_date)
    db_session.add(test_item)
    db_session.commit()

    assert test_item.title == custom_title
    assert test_item.description == custom_description
    assert test_item.priority == custom_priority
    assert test_item.done == custom_done
    assert test_item.due_date == custom_due_date


def test_repr_method(db_session):
    todo_item = TodoItem(title="Repr Task")
    db_session.add(todo_item)
    db_session.commit()

    expected_repr = f"Title: Repr Task, Due date: {todo_item.due_date}"
    assert repr(todo_item) == expected_repr
