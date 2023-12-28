from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.maps.search import MapsSearchClient
from azure.maps.search.models import LatLon

from common.settings import AzureMapsSettings
from models.azure_map import SearchAddressResult


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


def get_client(settings: AzureMapsSettings) -> MapsSearchClient:
    """Get Azure Maps client.

    :param settings: Azure Maps settings.
    """
    return MapsSearchClient(
        credential=AzureKeyCredential(settings.azure_map_key),
    )


def search_address(settings: AzureMapsSettings, query: str) -> SearchAddressResult:
    """Search address.

    :param settings: Azure Maps settings.
    :param query: Address query.
    """
    client = get_client(settings)
    result = client.search_address(query=query)
    return SearchAddressResult(**to_dict(result))


def search_nearby_point_of_interest(
    settings: AzureMapsSettings, latlon: LatLon
) -> SearchAddressResult:
    """Search nearby point of interest.

    :param settings: Azure Maps settings.
    :param latlon: Latitude and longitude.
    """
    client = get_client(settings)
    result = client.search_nearby_point_of_interest(coordinates=latlon)
    return SearchAddressResult(**to_dict(result))


# if __name__ == "__main__":
#     settings = AzureMapsSettings.model_validate({})

#     result = search_address(
#         settings=settings, query="1045 La Avenida St, Mountain View, CA"
#     )

#     if result and result.results:
#         print(
#             {
#                 r.address.freeform_address: r.additional_properties.get(
#                     "matchConfidence"
#                 )
#                 for r in result.results
#                 if r.address and r.additional_properties
#             }
#         )
