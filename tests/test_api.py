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
