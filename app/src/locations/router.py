from fastapi_cache.decorator import cache
from starlette.status import HTTP_404_NOT_FOUND
from fastapi import APIRouter, Depends, HTTPException

from locations.schemas import CityDisplaySchema, StationDisplaySchema
from locations.stations import get_station_by_id
from meili import get_client as get_search_client
from locations.cities import get_city_by_id, get_top_cities

router = APIRouter(
    prefix="/api/v1/locations",
)


@router.get("/")
async def search(query: str, client=Depends(get_search_client)):
    query_result = client.multi_search(
        [
            {'indexUid': 'cities', 'q': query, 'limit': 3},
            {'indexUid': 'stations', 'q': query, 'limit': 3},
        ]
    )
    cities = query_result["results"][0]["hits"]
    stations = query_result["results"][1]["hits"]
    cities = sorted(cities, key=lambda x: -len(x['name']))
    stations = sorted(stations, key=lambda x: -len(x['display_name']))
    res = []
    while len(cities) or len(stations):
        if len(cities):
            city = cities.pop()
            res.append(CityDisplaySchema.from_meili_document(city))
        if len(stations):
            station = stations.pop()
            res.append(StationDisplaySchema.from_meili_document(station))

    return res


@router.get("/city/")
@cache(expire=3600)
async def city_by_id(id: int):
    res = await get_city_by_id(id)
    if not res:
        raise HTTPException(HTTP_404_NOT_FOUND)
    return res


@router.get("/station/")
@cache(expire=3600)
async def station_by_id(id: int):
    res = await get_station_by_id(id)
    if not res:
        raise HTTPException(HTTP_404_NOT_FOUND)
    return res


@router.get("/top_cities/")
@cache(expire=3600)
async def get_top_cities_route():
    return await get_top_cities()
