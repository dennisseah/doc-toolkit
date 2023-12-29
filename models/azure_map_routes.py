from datetime import datetime

from pydantic import BaseModel


class LatLongPair(BaseModel):
    latitude: float | None = None
    longitude: float | None = None


class RouteSummary(BaseModel):
    length_in_meters: int | None = None
    travel_time_in_seconds: int | None = None
    traffic_delay_in_seconds: int | None = None
    departure_time: datetime | None = None
    arrival_time: datetime | None = None


class RouteLegSummary(BaseModel):
    length_in_meters: int | None = None
    travel_time_in_seconds: int | None = None
    traffic_delay_in_seconds: int | None = None
    departure_time: datetime | None = None
    arrival_time: datetime | None = None
    no_traffic_travel_time_in_seconds: int | None = None
    historic_traffic_travel_time_in_seconds: int | None = None
    live_traffic_incidents_travel_time_in_seconds: int | None = None
    fuel_consumption_in_liters: float | None = None
    battery_consumption_in_kw_h: float | None = None


class RouteLeg(BaseModel):
    summary: RouteLegSummary | None = None
    points: list[LatLongPair] | None = None


class RouteSectionTecCause(BaseModel):
    main_cause_code: int | None = None
    sub_cause_code: int | None = None


class RouteSectionTec(BaseModel):
    effect_code: int | None = None
    causes: list[RouteSectionTecCause] | None = None


class RouteInstructionGroup(BaseModel):
    first_instruction_index: int | None = None
    last_instruction_index: int | None = None
    group_length_in_meters: int | None = None
    group_message: str | None = None


class RouteInstruction(BaseModel):
    route_offset_in_meters: int | None = None
    travel_time_in_seconds: int | None = None
    poin: LatLongPair | None = None
    point_index: int | None = None
    instruction_type: str | None = None
    road_numbers: list[str] | None = None
    exit_number: str | None = None
    street: str | None = None
    signpost_text: str | None = None
    country_code: str | None = None
    state_code: str | None = None
    junction_type: str | None = None
    turn_angle_in_degrees: int | None = None
    roundabout_exit_number: str | None = None
    possible_combine_with_next: bool | None = None
    driving_side: str | None = None
    maneuver: str | None = None
    message: str | None = None
    combined_message: str | None = None


class RouteGuidance(BaseModel):
    instructions: list[RouteInstruction] | None = None
    instruction_groups: list[RouteInstructionGroup] | None = None


class RouteSection(BaseModel):
    start_point_index: int | None = None
    end_point_index: int | None = None
    section_type: str | None = None
    travel_mode: str | None = None
    simple_category: str | None = None
    effective_speed_in_kmh: int | None = None
    delay_in_seconds: int | None = None
    delay_magnitude: str | None = None
    tec: RouteSectionTec | None = None


class Route(BaseModel):
    summary: RouteSummary | None = None
    legs: list[RouteLeg] | None = None
    sections: list[RouteSection] | None = None
    guidance: RouteGuidance | None = None


class RouteOptimizedWaypoint(BaseModel):
    provided_index: int | None = None
    optimized_index: int | None = None


class EffectiveSetting(BaseModel):
    key: str | None = None
    value: str | None = None


class RouteReport(BaseModel):
    effective_settings: list[EffectiveSetting] | None = None


class RouteDirections(BaseModel):
    format_version: str | None = None
    routes: list[Route] | None = None
    optimized_waypoints: list[RouteOptimizedWaypoint] | None = None
    report: RouteReport | None = None
