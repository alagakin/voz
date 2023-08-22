from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from config import FRONTEND_ORIGIN
from locations.stations import index_stations, sync_stations
from api.routes import router as api_router

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


@app.on_event("startup")
async def startup_event():
    await sync_stations()
    await index_stations()
