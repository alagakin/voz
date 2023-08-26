from datetime import datetime

import pytz

from config import MONGO_DB
from routes.handler import HandlerInterface
from routes.request import SearchRequest

timezone = pytz.timezone('Europe/Belgrade')


class RoutesHandler(HandlerInterface):
    request: SearchRequest
    _stations_coordinates: None or dict = None
    supposed_stations_from_ids: list = []
    supposed_stations_to_ids: list = []
    date: datetime

    def __init__(self, request: SearchRequest, client):
        self.request = request
        self.client = client
        self.stations = self.client[MONGO_DB]["stations"]
        self.routes = self.client[MONGO_DB]["routes"]
        self.request.routes = []
        self.date = self.request.date
        supposed_stations_from_ids = []
        supposed_stations_to_ids = []

        for st in self.request.supposed_stations_from:
            supposed_stations_from_ids.append(st['id'])

        for st in self.request.supposed_stations_to:
            supposed_stations_to_ids.append(st['id'])

        self.supposed_stations_from_ids = supposed_stations_from_ids
        self.supposed_stations_to_ids = supposed_stations_to_ids

    async def handle(self) -> SearchRequest:
        if not len(self.supposed_stations_from_ids) and not len(self.supposed_stations_to_ids):
            return self.request

        start_of_day = timezone.localize(datetime.combine(self.date, datetime.min.time()))
        end_of_day = timezone.localize(datetime.combine(self.date, datetime.max.time()))
        query = {
            "date": {
                "$gte": start_of_day.isoformat(),
                "$lt": end_of_day.isoformat()
            }
        }

        routes = []
        async for route in self.routes.find(query, {"_id": 0}):
            if self.check_route_fits(route['stations']):
                routes.append(await self.modify_route(route))

        self.request.routes = routes

        return self.request

    async def modify_route(self, route):
        stations_from = []
        stations_to = []
        stations_coordinates = await self.stations_coordinates
        for station in route['stations']:
            if station['id'] in stations_coordinates:
                station['coordinates'] = stations_coordinates[station['id']]
            if station['id'] in self.supposed_stations_from_ids:
                stations_from.append(station)
            if station['id'] in self.supposed_stations_to_ids:
                stations_to.append(station)

        route['stations_from'] = stations_from
        route['stations_to'] = stations_to

        return route

    def check_route_fits(self, stations: list):
        station_from_key = -1
        station_to_key = -1
        for key, station in enumerate(stations):
            if station['id'] in self.supposed_stations_from_ids:
                station_from_key = key
            if station['id'] in self.supposed_stations_to_ids:
                station_to_key = key

        if station_from_key == -1 or station_to_key == -1:
            return False

        if station_from_key >= station_to_key:
            return False

        return True

    @property
    async def stations_coordinates(self):
        if self._stations_coordinates is None:
            await self._get_stations_coordinates()
        return self._stations_coordinates

    async def _get_stations_coordinates(self):
        stations_coordinates = dict()
        async for st in self.stations.find({}):
            stations_coordinates[st['id']] = st['coordinates']
        self._stations_coordinates = stations_coordinates
