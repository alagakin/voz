from fastapi import APIRouter, Depends
from meili import get_client as get_search_client, get_index

router = APIRouter(
    prefix="/api/v1",
)


@router.get("/locations/")
async def locations(query: str, client=Depends(get_search_client)):
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
            res.append({
                'id': city['id'],
                'display_name': f"{city['name']}, {city['country']}",
                'type': 'city'
            })
        if len(stations):
            station = stations.pop()
            res.append({
                'id': station["id"],
                'display_name': station["display_name"],
                'type': "station"
            })

    return res
