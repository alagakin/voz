import json
from datetime import datetime
from typing import List
import requests
import pytz
from bs4 import BeautifulSoup
from pydantic import ValidationError

from config import MONGO_DB, MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT
from log import trains_parsing_logger, routes_parsing_logger
from locations.schemas import TrainSchema, RouteStationSchema, RouteSchema
import pymongo
from requests.exceptions import ConnectionError, HTTPError

timezone = pytz.timezone('Europe/Belgrade')


def get_client():
    client = pymongo.MongoClient(
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"
    )
    return client


def parse():
    trains = get_trains()
    client = get_client()
    for train in trains:
        route = get_routes_of_train(train)
        if route:
            save_route(route, client)


def get_trains():
    stations = get_stations()
    trains = []
    for station in stations:
        trains.extend(get_trains_for_station(station))

    return trains


def save_route(route, client):
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


def get_trains_for_station(station) -> List[TrainSchema]:
    res = []
    url = f"https://w3.srbvoz.rs/redvoznje//stanicni/" \
          f"{station['name']}/{station['id']}/" \
          f"{datetime.now().strftime('%d.%m.%Y')}/0000/polazak/999/sr"
    try:
        html = fetch_url(url)
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


def get_routes_of_train(train: TrainSchema):
    url = f"https://w3.srbvoz.rs/redvoznje//api/vozdetalji1" \
          f"?idvoza={train.id}&brojvoza={train.number}" \
          f"&datum={train.date.strftime('%d-%m-%Y')}" \
          f"&stanicaod={train.station_from}" \
          f"&stanicado={train.station_to}"

    try:
        json_data = fetch_url(url)
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

    train_id = data["IDVOZA"]
    train_number = data["BROJVOZA"]
    res = RouteSchema(stations=stations, train_id=train_id, train_number=train_number)

    return res


def get_stations():
    client = get_client()
    db = client[MONGO_DB]
    collection = db["stations"]
    stations = []
    for document in collection.find():
        stations.append(document)

    return stations


def fetch_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text
