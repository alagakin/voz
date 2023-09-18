import asyncio
import pytest

from httpx import AsyncClient
from typing import AsyncGenerator

from main import init_cache
from main import app

ROUTE_PREFIX = "/api/v1"


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def setup_and_teardown():
    await init_cache()
    yield


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
