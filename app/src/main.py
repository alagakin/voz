from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from config import FRONTEND_ORIGIN
from locations.cities import create_cities_search_index, sync_cities
from locations.datetable import fill_date_table
from locations.stations import create_stations_search_index, sync_stations, create_stations_index
from api.router import router as api_router
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
app.include_router(api_router)
app.include_router(routes_router)
app.include_router(locations_router)


@app.on_event("startup")
async def startup_event():
    await sync_stations()
    await create_stations_search_index()
    fill_date_table()
    await sync_cities()
    await create_cities_search_index()
    await create_stations_index()
