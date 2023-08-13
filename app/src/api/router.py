from fastapi import APIRouter

from config import MONGO_DB
from database import get_client

router = APIRouter(
    prefix="/api/v1",
)


@router.get('/find-routes/')
async def index(station_from, station_to):
    client = await get_client()
    db = client[MONGO_DB]
    collection = db["routes"]
    stations = db["stations"]
    routes = []
    async for route in collection.find({}):
        if route_matches(route, station_from, station_to):
            route["_id"] = str(route["_id"])
            route = await set_coordinates(route, stations)
            routes.append(route)
    return routes


def route_matches(route, station_from, station_to) -> bool:
    station_from_key = -1
    station_to_key = -1
    for key, station in enumerate(route['stations']):
        if station['name'] == station_from:
            station_from_key = key
        if station['name'] == station_to:
            station_to_key = key

    if station_from_key == -1 or station_to_key == -1:
        return False

    if station_from_key >= station_to_key:
        return False

    return True


async def set_coordinates(route, stations):
    for station in route['stations']:
        db_station = await stations.find_one({"id": station['id']})
        if db_station:
            coords = db_station["coordinates"]
            station["coordinates"] = coords

    return route
