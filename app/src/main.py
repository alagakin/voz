from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.router import router

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",  # If you're running a Vue app on this port
    "http://localhost:8000",
]

# Use the CORSMiddleware to enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
