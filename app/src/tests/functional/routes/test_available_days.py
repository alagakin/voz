from httpx import AsyncClient

from tests.conftest import ROUTE_PREFIX


async def test_available_days(ac: AsyncClient):
    response = await ac.get(ROUTE_PREFIX + "/routes/available-days/")
    assert len(response.json()) > 0
