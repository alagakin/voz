import json
from datetime import datetime
from typing import List
import requests
import pytz
from bs4 import BeautifulSoup
from pydantic import ValidationError

from config import MONGO_DB
from log import trains_parsing_logger, routes_parsing_logger
from locations.schemas import TrainSchema, RouteStationSchema, RouteSchema
from requests.exceptions import ConnectionError, HTTPError
from database import get_sync_client

timezone = pytz.timezone('Europe/Belgrade')


class Parser:
    date: datetime

    def __init__(self, date: datetime):
        self.date = date

    def parse(self):
        trains = self.get_trains()
        client = get_sync_client()
        for train in trains:
            route = self.get_routes_of_train(train)
            if route:
                self.save_route(route, client)

    def get_trains(self):
        stations = self.get_stations()
        trains = []
        for station in stations:
            trains.extend(self.get_trains_for_station(station))

        return trains

    def save_route(self, route, client):
        db = client[MONGO_DB]
        collection = db["routes"]
        route = route.dict()
        for station in route["stations"]:
            station["arrival"] = station["arrival"].isoformat()
            station["departure"] = station["departure"].isoformat()
            station["date"] = station["date"].isoformat()

        query = {"id": route["id"]}
        existing_document = collection.find_one(query)

        if not existing_document:
            collection.insert_one(route)

    def get_trains_for_station(self, station) -> List[TrainSchema]:
        res = []
        url = f"https://w3.srbvoz.rs/redvoznje//stanicni/" \
              f"{station['name']}/{station['id']}/" \
              f"{self.date.strftime('%d.%m.%Y')}/0000/polazak/999/sr"
        try:
            html = self.fetch_url(url)
        except HTTPError or ConnectionError:
            return res
        try:
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find(id="rezultati")
            table = table.find('table')
            rows = table.find_all(class_='tsmall')
        except AttributeError:
            return []

        for i in range(1, len(rows)):
            try:
                row = rows[i]
                item = {}
                cells = row.find_all('td')
                item["number"] = int(cells[0].text.strip())
                item["arrival"] = cells[1].text.strip()
                item["departure"] = cells[3].text.strip()
                item["rang"] = cells[4].find('img').get('title')
                item["id"] = cells[8].find('button').get('data-idvoza')
                item["station_from"] = cells[8].find('button').get('data-stod')
                item["station_to"] = cells[8].find('button').get('data-stdo')
                schema = TrainSchema(**item)
                res.append(schema)
            except ValidationError as validationError:
                trains_parsing_logger.error(validationError)
            except Exception as e:
                trains_parsing_logger.error(f"{e} {e.__class__}")

        return res

    def get_routes_of_train(self, train: TrainSchema):
        url = f"https://w3.srbvoz.rs/redvoznje//api/vozdetalji1" \
              f"?idvoza={train.id}&brojvoza={train.number}" \
              f"&datum={self.date.strftime('%d-%m-%Y')}" \
              f"&stanicaod={train.station_from}" \
              f"&stanicado={train.station_to}"

        try:
            json_data = self.fetch_url(url)
        except HTTPError or ConnectionError:
            return False

        try:
            data = json.loads(json_data)[0]
        except KeyError:
            return False

        stations = []
        for station in data['stanicavoza']:
            item = {}
            try:
                item['arrival'] = station["DOLAZAK"]
                item["departure"] = station["POLAZAK"]
                item["number"] = station["RBSTANICE"]
                item["name"] = station["NAZIV"]
                item["name1"] = station["NAZIV1"]
                item["time"] = station["vremevoznje"]
                item["id"] = station["Sifra"]
                stations.append(RouteStationSchema(**item))
            except KeyError as e:
                message = f"Key {e} is not present in object {station}"
                routes_parsing_logger.error(message)

        if len(stations) == 0:
            return False

        try:
            train_id = data["IDVOZA"]
            train_number = data["BROJVOZA"]
            res = RouteSchema(stations=stations, train_id=train_id, train_number=train_number,
                              date=timezone.localize(self.date).isoformat())
        except ValidationError as e:
            routes_parsing_logger.error(e)
            return False

        return res

    def get_stations(self):
        client = get_sync_client()
        db = client[MONGO_DB]
        collection = db["stations"]
        stations = []
        for document in collection.find():
            stations.append(document)

        return stations

    def fetch_url(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text
