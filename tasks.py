from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, Task as TaskResponse  # Импортируем обе схемы
from database import SessionLocal, engine, Base
from celery_worker import create_task
import redis

Base.metadata.create_all(bind=engine)

app = FastAPI()
cache = redis.Redis(host='localhost', port=6379, db=0)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model=TaskResponse)  # Изменили здесь
def post_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    create_task.delay(task.title, task.description)
    return db_task

@app.get("/tasks/{task_id}", response_model=TaskResponse)  # Изменили здесь
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = cache.get(task_id)
    if task is None:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task:
            cache.set(task_id, db_task.json())
            return db_task
        return None
    return task
