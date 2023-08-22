from celery_config import app
from locations.parser import parse as pr


@app.task
def parse():
    pr()