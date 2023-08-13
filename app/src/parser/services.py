import json
from datetime import datetime
from typing import List
import aiohttp
from bs4 import BeautifulSoup
from pydantic import ValidationError

from config import MONGO_DB
from database import get_client
from log import logger, trains_parsing_logger, routes_parsing_logger
from parser.schemas import TrainSchema, RouteStationSchema, RouteSchema


async def parse():
    trains = await get_trains()
    client = await get_client()
    for train in trains:
        route = await get_routes_of_train(train)
        if route:
            await save_route(route, client)


async def get_trains():
    stations = await get_stations()
    trains = []
    for station in stations:
        trains.extend(await get_trains_for_station(station))

    return trains


async def save_route(route, client):
    db = client[MONGO_DB]
    collection = db["routes"]
    route = route.dict()
    for station in route["stations"]:
        station["arrival"] = station["arrival"].isoformat()
        station["departure"] = station["departure"].isoformat()
        station["date"] = station["date"].isoformat()

    query = {"id": route["id"]}
    existing_document = await collection.find_one(query)

    if not existing_document:
        await collection.insert_one(route)


async def get_trains_for_station(station) -> List[TrainSchema]:
    res = []
    url = f"https://w3.srbvoz.rs/redvoznje//stanicni/" \
          f"{station['name']}/{station['id']}/" \
          f"{datetime.now().strftime('%d.%m.%Y')}/0000/polazak/999/sr"
    html = await fetch_url(url)
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


async def get_routes_of_train(train: TrainSchema):
    url = f"https://w3.srbvoz.rs/redvoznje//api/vozdetalji1" \
          f"?idvoza={train.id}&brojvoza={train.number}" \
          f"&datum={train.date.strftime('%d-%m-%Y')}" \
          f"&stanicaod={train.station_from}" \
          f"&stanicado={train.station_to}"

    json_data = await fetch_url(url)

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

    train_id = data["IDVOZA"]
    train_number = data["BROJVOZA"]
    res = RouteSchema(stations=stations, train_id=train_id, train_number=train_number)

    return res


async def get_stations():
    client = await get_client()
    db = client[MONGO_DB]
    collection = db["stations"]
    stations = []
    async for document in collection.find():
        stations.append(document)

    client.close()

    return stations


async def fetch_url(url) -> str:
    # todo use single schema
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
