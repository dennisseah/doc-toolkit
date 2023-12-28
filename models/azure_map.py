from typing import Any

from pydantic import BaseModel


class LatLon(BaseModel):
    additional_properties: dict[str, Any] | None = None
    lat: float = 0
    lon: float = 0


class PointOfInterestCategorySet(BaseModel):
    id: int | None = None


class GeometryIdentifier(BaseModel):
    id: str | None = None


class DataSource(BaseModel):
    geometry: GeometryIdentifier | None = None


class BrandName(BaseModel):
    names: str | None = None


class ClassificationName(BaseModel):
    name_locale: str | None = None
    names: str | None = None


class Classification(BaseModel):
    code: str | None = None
    names: list[ClassificationName] | None = None


class OperatingHoursTime(BaseModel):
    date: str | None = None
    hour: int | None = None
    minute: int | None = None


class OperatingHoursTimeRange(BaseModel):
    start_time: OperatingHoursTime | None = None
    end_time: OperatingHoursTime | None = None


class OperatingHours(BaseModel):
    mode: str | None = None
    opening_time: OperatingHoursTimeRange | None = None
    closing_time: OperatingHoursTimeRange | None = None


class EntryPoint(BaseModel):
    additional_properties: dict[str, Any] | None = None
    type: str | None = None
    position: LatLon | None = None


class PointOfInterest(BaseModel):
    name: str | None = None
    phone: str | None = None
    url: str | None = None
    category_set: list[PointOfInterestCategorySet] | None = None
    classifications: list[Classification] | None = None
    brands: list[BrandName] | None = None
    operating_hours: list[OperatingHours] | None = None


class BoundingBox(BaseModel):
    west: float = 0.0
    south: float = 0.0
    east: float = 0.0
    north: float = 0.0


class ViewPort(BaseModel):
    additional_properties: dict[str, Any] | None = None
    top_left: LatLon | None = None
    bottom_right: LatLon | None = None


class Address(BaseModel):
    additional_properties: dict[str, Any] | None = None
    building_number: str | None = None
    street: str | None = None
    cross_street: str | None = None
    street_number: str | None = None
    route_numbers: list[int] | None = None
    street_name: str | None = None
    street_name_and_number: str | None = None
    municipality: str | None = None
    municipality_subdivision: str | None = None
    country_tertiary_subdivision: str | None = None
    country_secondary_subdivision: str | None = None
    country_subdivision: str | None = None
    postal_code: str | None = None
    extended_postal_code: str | None = None
    country_code: str | None = None
    country: str | None = None
    country_code_iso3: str | None = None
    freeform_address: str | None = None
    country_subdivision_name: str | None = None
    local_name: str | None = None
    bounding_box: BoundingBox | None = None


class AddressRanges(BaseModel):
    range_left: str | None = None
    range_right: str | None = None
    from_property: LatLon | None = None
    to: LatLon | None = None


class SearchAddressResultItem(BaseModel):
    additional_properties: dict[str, Any] | None = None
    type: str | None = None
    id: str | None = None
    score: float | None = None
    distance_in_meters: float | None = None
    info: str | None = None
    entity_type: str | None = None
    point_of_interest: PointOfInterest | None = None
    address: Address | None = None
    position: LatLon | None = None
    viewport: ViewPort | None = None
    entry_points: list[EntryPoint] | None = None
    address_ranges: LatLon | None = None
    data_sources: DataSource | None = None
    match_type: str | None = None
    detour_time: int | None = None


class SearchAddressResult(BaseModel):
    query: str | None = None
    query_type: str | None = None
    query_time: int | None = None
    top: int | None = None
    skip: int | None = None
    total_results: int | None = None
    fuzzy_level: int | None = None
    num_results: int | None = None
    geo_bias: LatLon | None = None
    results: list[SearchAddressResultItem] | None = None
