import json
import os
from database import get_async_client
from config import MONGO_DB
from utils import latin_to_cyrillic, simplify_latin_serbian
from meili import fill_index


async def sync_stations() -> None:
    client = await get_async_client()
    db = client[MONGO_DB]
    collection = db["stations"]

    stations_json = await read_stations()
    stations = json.loads(stations_json)

    for station in stations:
        query = {"name": station["name"]}
        existing_document = await collection.find_one(query)

        if existing_document:
            await collection.update_one(query, {"$set": station})
        else:
            await collection.insert_one(station)

    client.close()


async def read_stations():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'files/stations.json')

    with open(file_path, 'r') as file:
        contents = file.read()
    return contents


async def create_stations_search_index():
    client = await get_async_client()
    db = client[MONGO_DB]
    stations = db["stations"]
    documents = []
    async for station in stations.find():
        documents.append(make_document_for_index(station))

    return fill_index(index_name="stations", documents=documents)


def make_document_for_index(station):
    return {
        'id': station["id"],
        'display_name': station['name'].title(),
        'name': station["name"],
        'name1': latin_to_cyrillic(station["name"]),
        'names': simplify_latin_serbian(station["name"])
    }


async def create_stations_index():
    client = await get_async_client()
    db = client[MONGO_DB]
    await db.stations.create_index([("coordinates", "2dsphere")])
