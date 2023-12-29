from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.maps.route.aio import MapsRouteClient
from azure.maps.route.models import LatLon

from common.settings import AzureMapsSettings
from models.azure_map_routes import RouteDirections


def to_dict(obj: Any) -> Any:
    if isinstance(obj, list):
        return [to_dict(item) for item in obj]

    if isinstance(obj, LatLon):
        return {"lat": obj.lat, "lon": obj.lon}

    if hasattr(obj, "__dict__"):
        res = {}
        for k, v in obj.__dict__.items():
            if not k.startswith("_"):
                res[k] = to_dict(v) if isinstance(v, object) else v
        return res

    return obj


def get_client(settings: AzureMapsSettings) -> MapsRouteClient:
    """Get Azure Maps client.

    :param settings: Azure Maps settings.
    """
    return MapsRouteClient(
        credential=AzureKeyCredential(settings.azure_map_key),
    )


async def get_route_directions(
    settings: AzureMapsSettings, route_points: list[LatLon]
) -> RouteDirections:
    """Get route directions.

    :param settings: Azure Maps settings.
    :param route_points: Route points.
    """
    client = get_client(settings=settings)
    result = await client.get_route_directions(route_points=route_points)
    return RouteDirections(**to_dict(result))


# async def main():
#     settings = AzureMapsSettings.model_validate({})
#     result = await get_route_directions(
#         settings=settings,
#         route_points=[LatLon(47.60323, -122.33028), LatLon(53.2, -106)],
#     )

#     print(RouteDirections(**to_dict(result)))


# if __name__ == "__main__":
#     import asyncio

#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
