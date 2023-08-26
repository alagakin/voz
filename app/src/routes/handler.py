from abc import ABC, abstractmethod

from routes.request import SearchRequest


class AmbiguousParamsException(Exception):
    pass


class HandlerInterface(ABC):
    request: SearchRequest

    @abstractmethod
    async def handle(self) -> SearchRequest:
        pass


class ParamsCheckHandler(HandlerInterface):
    request: SearchRequest

    def __init__(self, request: SearchRequest):
        self.request = request

    async def handle(self) -> SearchRequest:
        from_list = [self.from_city_set(), self.from_station_set(), self.from_coords_set()]
        to_list = [self.to_city_set(), self.to_station_set(), self.to_coords_set()]

        if sum(from_list) != 1 or sum(to_list) != 1:
            raise AmbiguousParamsException()

        return self.request

    def from_city_set(self):
        return self.request.city_from_id is not None

    def to_city_set(self):
        return self.request.city_to_id is not None

    def from_station_set(self):
        return self.request.station_from_id is not None

    def to_station_set(self):
        return self.request.station_to_id is not None

    def from_coords_set(self):
        return self.request.from_long is not None and self.request.from_lat is not None

    def to_coords_set(self):
        return self.request.to_long is not None and self.request.to_lat is not None
