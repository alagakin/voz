from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.middleware.cors import CORSMiddleware
from config import FRONTEND_ORIGIN
from locations.cities import create_cities_search_index, sync_cities, create_cities_index
from locations.datetable import fill_date_table
from locations.stations import create_stations_search_index, sync_stations, create_stations_index
from routes.router import router as routes_router
from locations.router import router as locations_router

app = FastAPI()
origins = [
    FRONTEND_ORIGIN
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes_router)
app.include_router(locations_router)


@app.on_event("startup")
async def create_indexes():
    await sync_stations()
    await create_stations_search_index()
    fill_date_table()
    await sync_cities()
    await create_cities_search_index()
    await create_stations_index()
    await create_cities_index()


@app.on_event("startup")
async def init_cache():
    redis = aioredis.from_url("redis://redis:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
