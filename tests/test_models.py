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
