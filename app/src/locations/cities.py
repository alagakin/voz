import csv
import os
from typing import List

from config import MONGO_DB
from database import get_async_client
from locations.schemas import CitySchema
from meili import fill_index
from utils import latin_to_cyrillic, simplify_latin_serbian

files = [
    "files/ba.csv",
    "files/hr.csv",
    "files/me.csv",
    "files/rs.csv"
]


async def load_cities_to_db():
    client = await get_async_client()
    db = client[MONGO_DB]
    collection = db["cities"]

    for file in files:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, file)
        cities = read_cities(file_path)

        for city in cities:
            query = {"name": city.name, "country": city.country}
            existing_document = await collection.find_one(query)
            if existing_document:
                await collection.update_one(query, {"$set": city.dict()})
            else:
                await collection.insert_one(city.dict())


def read_cities(file) -> List[CitySchema]:
    with open(file, "r") as csv_file:
        csv_reader = csv.reader(csv_file)

        cities = []
        for key, row in enumerate(csv_reader):
            if key == 0:
                continue
            cities.append({
                "name": row[0],
                "alias": row[5],
                "coordinates": {
                    "type": "Point",
                    "coordinates": [float(row[1]), float(row[2])]
                },
                "country": row[3]
            })

        res = []
        for city in cities:
            res.append(CitySchema(**city))

        return res


async def create_cities_search_index():
    client = await get_async_client()
    db = client[MONGO_DB]
    stations = db["cities"]
    documents = []
    async for station in stations.find():
        documents.append(make_document_for_index(station))

    return fill_index(index_name="cities", documents=documents)


def make_document_for_index(city):
    return {
        "id": str(city["_id"]),
        "name": city["name"],
        "name1": latin_to_cyrillic(city["name"]),
        "names": simplify_latin_serbian(city["name"]),
        "country": city["country"]
    }
