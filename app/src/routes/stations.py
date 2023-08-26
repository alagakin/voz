from config import MONGO_DB
from routes.handler import HandlerInterface
from routes.request import SearchRequest


class StationsHandler(HandlerInterface):
    request: SearchRequest

    def __init__(self, request: SearchRequest, client):
        self.request = request
        self.client = client
        self.db = self.client[MONGO_DB]

    async def handle(self) -> SearchRequest:
        if self.request.city_from is not None or self.request.city_to is not None:
            await self.handle_cities()

        if self.request.station_from_id is not None or self.request.station_to_id is not None:
            await self.handle_stations()

        if self.request.from_long and self.request.from_lat:
            self.request.supposed_stations_from = await self.find_stations_by_coordinates(self.request.from_long,
                                                                                          self.request.from_lat, 10000)

        if self.request.to_long and self.request.to_lat:
            self.request.supposed_stations_to = await self.find_stations_by_coordinates(self.request.to_long,
                                                                                        self.request.to_lat, 10000)

        return self.request

    async def handle_cities(self):

        if self.request.city_from is not None:
            city_from_longitude = self.request.city_from.coordinates.coordinates[0]
            city_from_latitude = self.request.city_from.coordinates.coordinates[1]
            self.request.supposed_stations_from = await self.find_stations_by_coordinates(city_from_longitude,
                                                                                          city_from_latitude)
        if self.request.city_to is not None:
            city_to_longitude = self.request.city_to.coordinates.coordinates[0]
            city_to_latitude = self.request.city_to.coordinates.coordinates[1]
            self.request.supposed_stations_to = await self.find_stations_by_coordinates(city_to_longitude,
                                                                                        city_to_latitude)

    async def handle_stations(self):
        if self.request.station_from_id is not None:
            station_from = await self.fetch_station(self.request.station_from_id)
            if station_from:
                self.request.supposed_stations_from = [station_from]
        if self.request.station_to_id is not None:
            station_to = await self.fetch_station(self.request.station_to_id)
            if station_to:
                self.request.supposed_stations_to = [station_to]

    async def fetch_station(self, station_id):
        query = {'id': station_id}
        return await self.db.stations.find_one(query)

    async def find_stations_by_coordinates(self, longitude: float, latitude: float, distance: int = 5000):
        cursor = self.db.stations.find({
            "coordinates": {
                "$nearSphere": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [longitude, latitude]
                    },
                    "$maxDistance": distance
                }
            }
        }, {"_id": 0})

        results = []
        async for document in cursor:
            results.append(document)

        return results
