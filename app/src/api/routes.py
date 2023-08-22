from typing import Dict
import pytz
from fastapi import APIRouter, Depends
from config import MONGO_DB
from database import get_async_client
from datetime import datetime
from meili import get_client as get_search_client, get_index

timezone = pytz.timezone('Europe/Belgrade')

router = APIRouter(
    prefix="/api/v1",
)


@router.get('/find-routes/')
async def index(station_from: int, station_to: int):
    client = await get_async_client()
    db = client[MONGO_DB]
    collection = db["routes"]
    stations = db["stations"]
    routes = []

    current_date = datetime.now(timezone).date()
    start_of_day = timezone.localize(datetime.combine(current_date, datetime.min.time()))
    end_of_day = timezone.localize(datetime.combine(current_date, datetime.max.time()))

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

    now = datetime.now(timezone)
    arrival = datetime.fromisoformat(route['stations'][0]['arrival'])
    if now > arrival:
        return False

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
