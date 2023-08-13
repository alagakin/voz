import time

from celery import Celery

from parser.services import set_routes

app = Celery(
    'tasks',  # Name of the app
    broker='redis://redis:6379/0',  # URL to the Redis broker
    backend='rpc://',  # Use RPC backend for results
)
