from celery import Celery
from config import MONGO_HOST, MONGO_PASS, MONGO_PORT, MONGO_USER
from celery.schedules import crontab

app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
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
        'schedule': crontab(minute='*/30'),
    },
    'date_table': {
        'task': 'scheduled.parsing.update_date_table',
        'schedule': crontab(minute=0, hour=1)
    },
    # todo: mongo stations index
}
