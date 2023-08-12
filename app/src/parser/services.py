import json
from typing import List
import aiohttp
from bs4 import BeautifulSoup
from config import MONGO_DB
from database import get_client
from log import logger
from parser.schemas import TrainSchema, RouteStationSchema, RouteSchema


async def fetch_url(url) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_list_of_trains(url) -> List[TrainSchema]:
    html = await fetch_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id="rezultati")
    table = table.find('table')
    rows = table.find_all(class_='tsmall')

    res = []
    # todo errors
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
        except Exception:
            logger.error(str(row))

        res.append(TrainSchema(**item))

    return res


async def get_routes(train: TrainSchema) -> RouteSchema:
    url = f"https://w3.srbvoz.rs/redvoznje//api/vozdetalji1" \
          f"?idvoza={train.id}&brojvoza={train.number}" \
          f"&datum={train.date.strftime('%d-%m-%Y')}" \
          f"&stanicaod={train.station_from}" \
          f"&stanicado={train.station_to}"
    json_data = await fetch_url(url)

    data = json.loads(json_data)[0]
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
        except Exception:
            logger.error(json.loads(station))

    train_id = data["IDVOZA"]
    train_number = data["BROJVOZA"]
    res = RouteSchema(stations=stations, train_id=train_id, train_number=train_number)

    return res


async def set_routes():
    stations = await get_stations()
    stations = stations[:1]
    for station in stations:
        trains = await get_list_of_trains(
            f"https://w3.srbvoz.rs/redvoznje//stanicni/{station['name']}/{station['id']}/11.08.2023/0000/polazak/999/sr")

        routes = []

        for train in trains:
            routes.append(await get_routes(train))

        client = await get_client()
        db = client[MONGO_DB]
        collection = db["routes"]

        for route in routes:
            route = route.dict()
            for station in route["stations"]:
                station["arrival"] = station["arrival"].isoformat()
                station["departure"] = station["departure"].isoformat()
                station["date"] = station["date"].isoformat()

            query = {"id": route["id"]}
            existing_document = await collection.find_one(query)

            if not existing_document:
                await collection.insert_one(route)


async def get_stations():
    client = await get_client()
    db = client[MONGO_DB]
    collection = db["stations"]
    stations = []
    async for document in collection.find():
        stations.append(document)

    client.close()

    return stations