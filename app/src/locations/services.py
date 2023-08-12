import json
import os

from database import get_client
from config import MONGO_DB


async def sync_stations() -> None:
    client = await get_client()
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
    file_path = os.path.join(script_dir, 'stations.json')

    with open(file_path, 'r') as file:
        contents = file.read()
    return contents
