from datetime import datetime
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


def setup() -> None:
    Base.metadata.create_all(bind=engine)


def teardown() -> None:
    Base.metadata.drop_all(bind=engine)


def test_create_todo_item():
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


def test_get_todo_item():
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

