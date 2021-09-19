from celery import Celery
import celery

app = Celery('tasks', broker='')

@app.task
def RunGame():
    return 2