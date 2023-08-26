from typing import Any, Union
from datetime import datetime
import bson
from bson import ObjectId
from pydantic import BaseModel, validator

from locations.schemas import CitySchema


class SearchRequest(BaseModel):
    date: datetime

    city_from_id: Union[str, ObjectId] = None
    city_to_id: Union[str, ObjectId] = None
    city_from: CitySchema = None
    city_to: CitySchema = None

    station_from_id: int = None
    station_to_id: int = None
    station_from: Any = None
    station_to: Any = None

    from_long: float = None
    from_lat: float = None
    to_long: float = None
    to_lat: float = None

    routes: list = None

    supposed_stations_from: list = []
    supposed_stations_to: list = []

    @validator("city_from_id", "city_to_id", pre=True, always=True)
    def validate_id(cls, field_value):
        try:
            if field_value is None:
                return field_value
            return ObjectId(field_value)
        except bson.errors.InvalidId:
            raise ValueError(f"{field_value} must be correct ObjectId")

    class Config:
        arbitrary_types_allowed = True