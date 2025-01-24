from celery import Celery
import os

# Настройки Celery
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def create_task(title, description):
    print(f"Task created: Title: {title}, Description: {description}")
