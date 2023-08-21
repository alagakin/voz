from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from locations.services import index_stations
from api.routes import router as api_router
from locations.routes import router as search_router

app = FastAPI()
origins = [
    "http://localhost:50000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(search_router)
app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    await index_stations()


@app.get("/")
def index():
    from parser.services import parse as ps
    ps()