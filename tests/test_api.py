import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base


client = TestClient(app)

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL,
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_todo_item(db_session):
    response = client.post(
        "/todos/", json={
                         "title": "Test Title",
                         "description": "Test Description",
                         "priority": 1,
                         "done": False,
                         }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Title"
    assert data["description"] == "Test Description"
    assert data["priority"] == 1
    assert data["done"] == False
    assert "id" in data


def test_get_todo_item(db_session):
    response = client.post(
        "/todos/", json={
                        "title": "Test Title",
                        "description": "Test Description"
                        }
    )
    assert response.status_code == 200
    data = response.json()
    todo_id = data["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Title"
    assert data["description"] == "Test Description"
    assert data["id"] == todo_id


def test_get_todos(db_session):
    todos = [
        {"title": "Test Title 1", "description": "Test Description 1"},
        {"title": "Test Title 2", "description": "Test Description 2"},
        {"title": "Test Title 3", "description": "Test Description 3"},
    ]

    created_todos = []
    for todo in todos:
        response = client.post("/todos/", json=todo)
        assert response.status_code == 200
        created_todos.append(response.json())

    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == len(created_todos)

    for created_todo in created_todos:
        assert any(todo["id"] == created_todo["id"] for todo in data)
        assert any(todo["title"] == created_todo["title"] for todo in data)
        assert any(todo["description"] == created_todo["description"] for todo in data)
