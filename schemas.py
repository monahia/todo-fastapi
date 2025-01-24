from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
