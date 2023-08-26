from typing import Dict
import pytz
from fastapi import APIRouter, Depends
from starlette.status import HTTP_400_BAD_REQUEST

from config import MONGO_DB
from database import get_async_client
from datetime import datetime
from meili import get_client as get_search_client, get_index
from fastapi.exceptions import HTTPException

timezone = pytz.timezone('Europe/Belgrade')

router = APIRouter(
    prefix="/api/v1",
)
iso_datetime_regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?$"


@router.get('/find-routes/')
async def index(station_from: int, station_to: int, date: str = None):
    try:
        if date is None:
            date = datetime.now(tz=timezone)
        else:
            date = datetime.fromisoformat(date)
            date = timezone.localize(date)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)

    client = await get_async_client()
    db = client[MONGO_DB]
    collection = db["routes"]
    stations = db["stations"]
    routes = []

    start_of_day = timezone.localize(datetime.combine(date, datetime.min.time()))
    end_of_day = timezone.localize(datetime.combine(date, datetime.max.time()))
    query = {
        "date": {
            "$gte": start_of_day.isoformat(),
            "$lt": end_of_day.isoformat()
        }
    }

    async for route in collection.find(query):
        route = get_route(route, station_from, station_to)
        if route:
            route["_id"] = str(route["_id"])
            route = await set_coordinates(route, stations)
            routes.append(route)
    return routes


def get_route(route, station_from: int, station_to: int) -> Dict or bool:
    station_from_key = -1
    station_to_key = -1
    for key, station in enumerate(route['stations']):
        if station['id'] == station_from:
            station_from_key = key
        if station['id'] == station_to:
            station_to_key = key

    if station_from_key == -1 or station_to_key == -1:
        return False

    if station_from_key >= station_to_key:
        return False
    route['stations'] = route['stations'][station_from_key:station_to_key + 1]

    return route


async def set_coordinates(route, stations):
    for station in route['stations']:
        db_station = await stations.find_one({"id": station['id']})
        if db_station:
            coords = db_station["coordinates"]
            station["coordinates"] = coords

    return route


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


@router.get("/city/search/")
async def search_station(query: str, client=Depends(get_search_client)):
    index = get_index("cities", client)
    return index.search(query, {
        'limit': 5,
        'attributesToSearchOn': ['name', 'name1', 'names']
    })
