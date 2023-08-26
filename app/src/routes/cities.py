from config import MONGO_DB
from locations.schemas import CitySchema
from routes.handler import HandlerInterface
from routes.request import SearchRequest


class CitiesHandler(HandlerInterface):
    request: SearchRequest

    def __init__(self, request: SearchRequest, client):
        self.request = request
        self.client = client

    async def handle(self) -> SearchRequest:
        if not self.request.city_from_id and not self.request.city_to_id:
            return self.request

        db = self.client[MONGO_DB]
        collection = db['cities']

        if self.request.city_from_id:
            city_from = await collection.find_one({"_id": self.request.city_from_id})
            if not city_from:
                return self.request
            self.request.city_from = CitySchema(**city_from)

        if self.request.city_to_id:
            city_to = await collection.find_one({"_id": self.request.city_to_id})
            if not city_to:
                return self.request
            self.request.city_to = CitySchema(**city_to)

        return self.request
