from datetime import datetime

import pytz
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from starlette.status import HTTP_400_BAD_REQUEST

from database import get_async_client
from meili import get_client as get_search_client

from meili import get_index
from routes.handler import ParamsCheckHandler, AmbiguousParamsException
from routes.routes_searcher import RoutesHandler
from routes.stations import StationsHandler
from routes.cities import CitiesHandler
from routes.request import SearchRequest

router = APIRouter(
    prefix="/api/v1",
)

timezone = pytz.timezone('Europe/Belgrade')

@router.get("/city/search/")
async def search_station(query: str, client=Depends(get_search_client)):
    index = get_index("cities", client)
    return index.search(query, {
        'limit': 5,
        'attributesToSearchOn': ['name', 'name1', 'names']
    })


@router.get("/routes/")
async def routes(
        city_from_id: str = None,
        city_to_id: str = None,
        station_from_id: str = None,
        station_to_id: str = None,
        from_long: float = None,
        from_lat: float = None,
        to_long: float = None,
        to_lat: float = None,
        date: str = None,
        client=Depends(get_async_client)):
    try:
        if date is None:
            date = datetime.now(tz=timezone).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            date = datetime.fromisoformat(date)
            date = timezone.localize(date)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)

    try:
        search_request = SearchRequest(
            city_from_id=city_from_id,
            city_to_id=city_to_id,
            station_from_id=station_from_id,
            station_to_id=station_to_id,
            from_long=from_long,
            from_lat=from_lat,
            to_lat=to_lat,
            to_long=to_long,
            date=date
        )
        search_request = await ParamsCheckHandler(request=search_request).handle()
        search_request = await CitiesHandler(request=search_request, client=client).handle()
        search_request = await StationsHandler(request=search_request, client=client).handle()
        search_request = await RoutesHandler(request=search_request, client=client).handle()

        return search_request.routes
    except ValidationError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=e.errors())
    except AmbiguousParamsException:
        raise HTTPException(HTTP_400_BAD_REQUEST, 'Ambiguous params')