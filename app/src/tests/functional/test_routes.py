import pytest

from httpx import AsyncClient

from tests.conftest import ROUTE_PREFIX


@pytest.mark.parametrize("route", ["/locations/top_cities/", "/routes/available-days/"])
async def test_not_parametrized_routes_routes_availability(route, ac: AsyncClient):
    response = await ac.get(ROUTE_PREFIX + route)
    assert response.status_code == 200
