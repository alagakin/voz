from database import get_sync_client
from datetime import datetime, timedelta
from config import MONGO_DB


def fill_date_table(days: int = 14):
    client = get_sync_client()
    dates = generate_dates(days)
    db = client[MONGO_DB]
    for date in dates:
        existing_item = db.datetable.find_one({'date': date})
        if not existing_item:
            db.datetable.insert_one({
                'date': date,
                'fetched': False
            })


def get_next_date():
    client = get_sync_client()
    db = client[MONGO_DB]
    query = {'fetched': False}
    count = db.datetable.count_documents(query)
    if count == 0:
        fill_date_table()
    result = db.datetable.find(query).sort('date', 1)

    return result[0]['date']


def set_as_fetched(date: datetime | str) -> bool:
    if isinstance(date, datetime):
        date = date.date().isoformat()

    client = get_sync_client()
    db = client[MONGO_DB]
    result = db.datetable.update_one({'date': date}, {'$set': {
        'date': date,
        'fetched': True
    }})
    return result.modified_count


def generate_dates(days: int):
    start = datetime.today()
    dates = [start.date() + timedelta(days=i) for i in range(days)]
    return [date.isoformat() for date in dates]
