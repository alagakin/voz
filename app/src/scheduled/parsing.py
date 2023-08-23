from datetime import datetime

from celery_config import app
from locations.datetable import get_next_date, set_as_fetched, fill_date_table
from locations.parser import Parser


@app.task
def parse():
    date = get_next_date()
    if date:
        date = datetime.strptime(date, '%Y-%m-%d')
        parser = Parser(date)
        parser.parse()
        return set_as_fetched(date)
    else:
        return False


@app.task
def update_date_table():
    fill_date_table(14)
