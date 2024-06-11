from datetime import datetime
from app.models import set_end_of_current_day
from app.schemas import TodoBase


def test_todo_base_due_date_none():
    data = {"due_date": None}
    test_base = TodoBase(**data)
    assert test_base.due_date == set_end_of_current_day()


def test_todo_base_due_date_absent():
    data = {}
    test_base = TodoBase(**data)
    assert test_base.due_date == set_end_of_current_day()


def test_todo_base_due_date_exists():
    date = datetime.utcnow()
    data = {"due_date": date}
    test_base = TodoBase(**data)
    assert test_base.due_date == date


def test_todo_base_priority_lt_zero():
    data = {"priority": -1}
    test_base = TodoBase(**data)
    assert test_base.priority == 0


def test_todo_base_priority_gt_four():
    data = {"priority": 5}
    test_base = TodoBase(**data)
    assert test_base.priority == 4
