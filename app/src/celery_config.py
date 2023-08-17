from celery import Celery

app = Celery(
    'tasks',  # Name of the app
    broker='redis://redis:6379/0',  # URL to the Redis broker
    include=["parser.services"]
)
