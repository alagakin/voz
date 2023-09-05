import hashlib
from typing import List
from pydantic import BaseModel, root_validator
from datetime import datetime, timedelta
import pytz

timezone = pytz.timezone('Europe/Belgrade')


class TrainSchema(BaseModel):
    id: int = 1
    number: int
    arrival: datetime
    departure: datetime
    rang: str
    station_from: int
    station_to: int


class RouteStationSchema(BaseModel):
    id: int
    number: int
    name: str
    name1: str
    time: int
    arrival: datetime
    departure: datetime

    @root_validator
    def strip_strings(cls, values):
        for field, value in values.items():
            if isinstance(value, str):
                values[field] = value.strip()
        return values


class RouteSchema(BaseModel):
    id: str = ""
    train_id: int
    train_number: int
    first_station: str = ''
    last_station: str = ''
    date: str = ''
    stations: List[RouteStationSchema]

    @root_validator
    def set_first_and_last(cls, values):
        stations = values.get('stations')
        if len(stations) < 2:
            return values

        values["first_station"] = stations[0].name
        values["last_station"] = stations[len(stations) - 1].name
        return values

    @root_validator
    def calc_hash(cls, values):
        fields = {field: values.get(field) for field in values if field != "id"}
        json = str(fields)
        hash_object = hashlib.sha256(json.encode())
        hash_value = hash_object.hexdigest()
        values['id'] = hash_value
        return values

    @root_validator
    def change_dates_if_different_dates(cls, values):
        stations = values.get('stations')
        prev_arrival = stations[0].arrival
        prev_departure = stations[0].departure
        days_add_arrival = 0
        days_add_departure = 0
        for i in range(1, len(stations)):
            arrival = stations[i].arrival
            departure = stations[i].departure
            if arrival.hour < prev_arrival.hour:
                days_add_arrival += 1
            if departure.hour < prev_departure.hour:
                days_add_departure += 1

            arrival += timedelta(days=days_add_arrival)
            departure += timedelta(days=days_add_departure)

            values['stations'][i].arrival = arrival
            values['stations'][i].departure = departure

            prev_arrival = arrival
            prev_departure = departure

        return values


class Coordinates(BaseModel):
    type: str = "Point"
    coordinates: list[float]


class CitySchema(BaseModel):
    name: str
    country: str
    coordinates: Coordinates


class LocationDisplaySchema(BaseModel):
    id: int
    display_name: str
    type: str


class CityDisplaySchema(LocationDisplaySchema):
    @classmethod
    def from_motor_dict(cls, dictionary):
        display_name = f"{dictionary['name']}, {dictionary['country']}"
        return cls(display_name=display_name, id=dictionary["id"], type="city")

    @classmethod
    def from_meili_document(cls, document):
        display_name = f"{document['name']}, {document['country']}"
        return cls(display_name=display_name, id=document["id"], type="city")


class StationDisplaySchema(LocationDisplaySchema):
    @classmethod
    def from_motor_dict(cls, dictionary):
        display_name = dictionary['name'].title()
        return cls(display_name=display_name, id=dictionary["id"], type="station")

    @classmethod
    def from_meili_document(cls, document):
        display_name = document['display_name']
        return cls(display_name=display_name, id=document["id"], type="station")
