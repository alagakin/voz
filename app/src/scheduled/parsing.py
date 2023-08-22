from datetime import datetime

from celery_config import app
from locations.datetable import get_next_date, set_as_fetched
from locations.parser import Parser


@app.task
def parse():
    date = get_next_date()
    date = datetime.strptime(date, '%Y-%m-%dT')

    parser = Parser(date)
    parser.parse()
    set_as_fetched(date)
