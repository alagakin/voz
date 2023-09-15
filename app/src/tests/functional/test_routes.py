import pytest
from fastapi.testclient import TestClient
from main import app, init_cache

client = TestClient(app)
ROUTE_PREFIX = "/api/v1"


@pytest.fixture(autouse=True)
async def setup_and_teardown():
    await init_cache()
    yield


@pytest.mark.parametrize("route", ["/locations/top_cities/", "/routes/available-days/"])
def test_not_parametrized_routes_routes_availability(route):
    response = client.get(ROUTE_PREFIX + route)
    assert response.status_code == 200
