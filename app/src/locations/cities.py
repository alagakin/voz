import asyncio
import json
import os
from typing import Union

from config import MONGO_DB
from database import get_async_client
from locations.schemas import CityDisplaySchema
from meili import fill_index
from utils import latin_to_cyrillic, simplify_latin_serbian


async def sync_cities() -> None:
    client = await get_async_client()
    db = client[MONGO_DB]
    collection = db["cities"]

    cities_json = await read_cities()
    cities = json.loads(cities_json)

    if len(cities):
        await collection.drop()

    for city in cities:
        if "logo" not in city:
            city["logo"] = None
        await collection.insert_one(city)

    client.close()


async def read_cities():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'files/cities.json')

    with open(file_path, 'r') as file:
        contents = file.read()
    return contents


async def create_cities_search_index():
    client = await get_async_client()
    db = client[MONGO_DB]
    cities = db["cities"]
    documents = []
    async for city in cities.find():
        documents.append(make_document_for_index(city))
    if len(documents):
        return fill_index(index_name="cities", documents=documents)
    return False


def make_document_for_index(city):
    return {
        "id": city["id"],
        "name": city["name"],
        "name1": latin_to_cyrillic(city["name"]),
        "names": simplify_latin_serbian(city["name"]),
        "country": city["country"]
    }


async def get_city_by_id(city_id) -> Union[CityDisplaySchema, False]:
    client = await get_async_client()
    db = client[MONGO_DB]
    cities = db["cities"]

    city = await cities.find_one({'id': city_id})
    if city:
        return CityDisplaySchema.from_motor_dict(city)
    return False


async def get_top_cities():
    client = await get_async_client()
    db = client[MONGO_DB]
    res = []
    async for city in db.cities.find({"logo": {"$ne": None}}):
        res.append(CityDisplaySchema.from_motor_dict(city))
    return res


async def create_cities_index():
    client = await get_async_client()
    db = client[MONGO_DB]
    await db.cities.create_index([("coordinates", "2dsphere")])
