from celery import Celery
from config import MONGO_HOST, MONGO_PASS, MONGO_PORT, MONGO_USER
from celery.schedules import crontab

app = Celery(
    'tasks',  # Name of the app
    broker='redis://redis:6379/0',  # URL to the Redis broker
    include=["scheduled.parsing"],
    backend='celery.backends.mongodb.MongoBackend'
)

app.conf.update(
    result_backend=f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/celery_result",
    result_backend_transport_options={'retry_options': {'max_retries': 3}}
)

app.conf.beat_schedule = {
    'parsing': {
        'task': 'scheduled.parsing.parse',
        'schedule': crontab(hour=2),
    },
}