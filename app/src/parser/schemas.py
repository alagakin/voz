from typing import List

from pydantic import BaseModel, validator, Field
from datetime import datetime, date


# Define Pydantic Schema
class TrainSchema(BaseModel):
    id: int = 1
    number: int
    arrive: datetime
    departure: datetime
    rang: str
    date: datetime = Field(default_factory=datetime.now)
    station_from: int
    station_to: int

    @validator("arrive", "departure", pre=True)
    def parse_datetime(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            # todo: what if days are different?
            parsed_time = datetime.strptime(value, "%H:%M")
            current_date = date.today()
            return datetime.combine(current_date, parsed_time.time())
        except ValueError:
            raise ValueError("Invalid datetime format. Expected 'HH:MM'.")


class RouteStationSchema(BaseModel):
    id: int
    number: int
    name: str
    name1: str
    time: int
    arrive: datetime
    departure: datetime
    date: datetime = Field(default_factory=datetime.now)

    @validator("arrive", "departure", pre=True)
    def parse_datetime(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            # todo: what if days are different?
            parsed_time = datetime.strptime(value, "%H:%M")
            current_date = date.today()
            return datetime.combine(current_date, parsed_time.time())
        except ValueError:
            raise ValueError("Invalid datetime format. Expected 'HH:MM'.")


class RouteSchema(BaseModel):
    train_id: int
    train_number: int
    stations: List[RouteStationSchema]

