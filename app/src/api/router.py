import pytz
from fastapi import APIRouter, Depends
from config import MONGO_DB
from database import get_async_client
from meili import get_client as get_search_client, get_index

timezone = pytz.timezone('Europe/Belgrade')

router = APIRouter(
    prefix="/api/v1",
)


@router.get("/station/search/")
async def search_station(query: str, client=Depends(get_search_client)):
    index = get_index('stations', client)
    return index.search(query, {
        'limit': 5,
        'attributesToSearchOn': ['name', 'display_name', 'name1', 'names']
    })


@router.get("/available-days/")
async def get_available_day(client=Depends(get_async_client)):
    db = client[MONGO_DB]
    collection = db['datetable']
    dates = []
    async for item in collection.find({'fetched': True}):
        dates.append(item['date'])
    return dates
