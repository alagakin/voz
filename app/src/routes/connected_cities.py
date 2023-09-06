from datetime import datetime
from typing import List

import pytz

from config import MONGO_DB
from locations.cities import get_city_by_id
from locations.schemas import CityDisplaySchema

timezone = pytz.timezone('Europe/Belgrade')


class ConnectedCities:
    def __init__(self, city_id: int, client):
        self.__city_id = city_id
        self.__client = client
        self.__db = self.__client[MONGO_DB]

    async def get(self):
        city = await get_city_by_id(self.__city_id)
        if not city:
            return False
        stations = await self.get_stations(city)
        stations_ids = [station['id'] for station in stations]
        if not stations:
            return False

        reachable_coordinates = await self.get_reachable_stations_coordinates(stations_ids)
        if not reachable_coordinates:
            return False

        connected_cities = await self.get_connected_cities(reachable_coordinates)
        if not connected_cities:
            return False

        return connected_cities

    async def get_connected_cities(self, coordinates) -> List[CityDisplaySchema]:
        cities = dict()
        for lat, long in coordinates:
            cursor = self.__db.cities.find({
                "coordinates": {
                    "$nearSphere": {
                        "$geometry": {
                            "type": "Point",
                            "coordinates": [lat, long]
                        },
                        "$maxDistance": 5000
                    }
                },
                "logo": {
                    "$ne": None
                }
            }, {"_id": 0})
            res = await cursor.to_list(length=None)
            for city in res:
                cities[city['id']] = city

        return [CityDisplaySchema.from_motor_dict(city) for city in cities.values()]

    async def get_reachable_stations_coordinates(self, stations_ids):
        now = datetime.now(tz=timezone).replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_day = timezone.localize(datetime.combine(now, datetime.min.time()))
        end_of_day = timezone.localize(datetime.combine(now, datetime.max.time()))
        query = {
            "date": {
                "$gte": start_of_day.isoformat(),
                "$lt": end_of_day.isoformat()
            }
        }
        reachable_stations_ids = set()
        async for route in self.__db.routes.find(query, {"_id": 0}):
            for station in route['stations']:
                if station['id'] in stations_ids:
                    to_add = [stat['id'] for stat in route['stations']]
                    reachable_stations_ids.update(to_add)
                    break
        if not reachable_stations_ids:
            return False
        cursor = self.__db.stations.find({"id": {"$in": list(reachable_stations_ids)}}, {'coordinates': 1, '_id': 0})
        res = await cursor.to_list(length=None)
        return [item['coordinates'] for item in res]

    async def get_stations(self, city):
        longitude = city.coordinates[0]
        latitude = city.coordinates[1]
        cursor = self.__db.stations.find({
            "coordinates": {
                "$nearSphere": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [longitude, latitude]
                    },
                    "$maxDistance": 5000
                }
            }
        }, {"_id": 0})

        return await cursor.to_list(length=None)
