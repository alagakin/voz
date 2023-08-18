import hashlib
from typing import List
from pydantic import BaseModel, validator, Field, root_validator
from datetime import datetime, date
import pytz

timezone = pytz.timezone('Europe/Belgrade')


class TrainSchema(BaseModel):
    id: int = 1
    number: int
    # todo: how to get know of day of the date?
    arrival: datetime
    departure: datetime
    rang: str
    date: datetime = Field(default_factory=datetime.now)
    station_from: int
    station_to: int

    @validator("arrival", "departure", pre=True)
    def parse_datetime(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            parsed_time = datetime.strptime(value, "%H:%M")
            current_date = date.today()
            return timezone.localize(datetime.combine(current_date, parsed_time.time()))
        except ValueError:
            raise ValueError("Invalid datetime format. Expected 'HH:MM'.")


class RouteStationSchema(BaseModel):
    id: int
    number: int
    name: str
    name1: str
    time: int
    arrival: datetime
    departure: datetime
    date: datetime = Field(default_factory=datetime.now().date)

    @root_validator
    def strip_strings(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = value.strip()
        return values

    @validator("arrival", "departure", pre=True)
    def parse_datetime(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            parsed_time = datetime.strptime(value, "%H:%M")
            current_date = date.today()
            return timezone.localize(datetime.combine(current_date, parsed_time.time()))
        except ValueError:
            raise ValueError("Invalid datetime format. Expected 'HH:MM'.")


class RouteSchema(BaseModel):
    id: str = ""
    train_id: int
    train_number: int
    first_station: str = ''
    last_station: str = ''
    date: datetime = Field(default_factory=datetime.now)
    stations: List[RouteStationSchema]

    @root_validator
    def set_first_and_last(cls, values):
        stations = values.get('stations')
        if len(stations) < 2:
            return values

        values["first_station"] = stations[0].name
        values["last_station"] = stations[len(stations) - 1].name
        values["date"] = timezone.localize(
            datetime(stations[0].arrival.year, stations[0].arrival.month, stations[0].arrival.day))
        return values

    @root_validator
    def calc_hash(cls, values):
        fields = {field: values.get(field) for field in values if field != "id"}
        json = str(fields)
        hash_object = hashlib.sha256(json.encode())
        hash_value = hash_object.hexdigest()
        values['id'] = hash_value
        return values
