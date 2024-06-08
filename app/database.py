import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL)
LocalSession = sessionmaker(bind=engine)


def get_session():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
