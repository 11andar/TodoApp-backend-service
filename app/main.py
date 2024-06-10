from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import todo

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(todo.router)

