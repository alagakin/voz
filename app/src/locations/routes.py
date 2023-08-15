from fastapi import APIRouter, Depends
from search.services import get_client, get_index

router = APIRouter(
    prefix="/api/v1/station",
)


@router.get("/search/")
async def search_station(query: str, client=Depends(get_client)):
    index = get_index('stations', client)
    return index.search(query, {
        'limit': 5,
        'attributesToSearchOn': ['name', 'display_name', 'name1', 'names']
    })
