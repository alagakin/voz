from celery_config import app
from parser.services import parse as pr


@app.task
def parse():
    pr()