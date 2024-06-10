import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

database_dir = Path(__file__).resolve().parent.parent / 'database'
database_dir.mkdir(parents=True, exist_ok=True)

db_file = database_dir / 'todo_items.db'
db_file.touch()

engine = create_engine(DATABASE_URL)
LocalSession = sessionmaker(bind=engine)
Base = declarative_base()


def get_session():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
