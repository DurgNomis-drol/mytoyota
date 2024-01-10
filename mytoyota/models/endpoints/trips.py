"""Toyota Connected Services API - Trips Models."""
from __future__ import annotations

from datetime import date, datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel
from mytoyota.utils.helpers import add_with_none


class _SummaryBaseModel(BaseModel):
    length: int
    duration: int
    duration_idle: int = Field(alias="durationIdle")
    countries: List[str]
    max_speed: float = Field(alias="maxSpeed")
    average_speed: float = Field(alias="averageSpeed")
    length_overspeed: int = Field(alias="lengthOverspeed")
    duration_overspeed: int = Field(alias="durationOverspeed")
    length_highway: int = Field(alias="lengthHighway")
    duration_highway: int = Field(alias="durationHighway")
    fuel_consumption: Optional[float] = Field(
        alias="fuelConsumption", default=None
    )  # Electric cars might not use fuel. Milliliters.

    def __add__(self, other: _SummaryBaseModel):
        """Add together two SummaryBaseModel's.

        Handles Min/Max/Average fields correctly.

        Args:
        ----
        other: _SummaryBaseModel: to be added
        """
        if other is not None:
            self.length += other.length
            self.duration += other.duration
            self.duration_idle += other.duration_idle
            self.countries.extend(x for x in other.countries if x not in self.countries)
            self.max_speed = max(self.max_speed, other.max_speed)
            self.average_speed = (self.average_speed + other.average_speed) / 2.0
            self.length_overspeed += other.length_overspeed
            self.duration_overspeed += other.duration_overspeed
            self.length_highway += other.length_highway
            self.duration_highway += other.duration_highway
            self.fuel_consumption = add_with_none(self.fuel_consumption, other.fuel_consumption)

        return self


class _SummaryModel(_SummaryBaseModel):
    start_lat: float = Field(alias="startLat")
    start_lon: float = Field(alias="startLon")
    start_ts: datetime = Field(alias="startTs")
    end_lat: float = Field(alias="endLat")
    end_lon: float = Field(alias="endLon")
    end_ts: datetime = Field(alias="endTs")
    night_trip: bool = Field(alias="nightTrip")


class _CoachingMsgParamModel(BaseModel):
    name: str
    unit: str
    value: int


class _BehaviourModel(BaseModel):
    ts: datetime
    type: Optional[str] = None
    coaching_msg_params: Optional[List[_CoachingMsgParamModel]] = Field(
        alias="coachingMsgParams", default=None
    )


class _ScoresModel(BaseModel):
    global_: int = Field(..., alias="global")
    acceleration: Optional[int] = None
    braking: Optional[int] = None
    advice: Optional[int] = None
    constant_speed: Optional[int] = Field(alias="constantSpeed", default=None)


class _HDCModel(BaseModel):
    ev_time: Optional[int] = Field(alias="evTime", default=None)
    ev_distance: Optional[int] = Field(alias="evDistance", default=None)
    charge_time: Optional[int] = Field(alias="chargeTime", default=None)
    charge_dist: Optional[int] = Field(alias="chargeDist", default=None)
    eco_time: Optional[int] = Field(alias="ecoTime", default=None)
    eco_dist: Optional[int] = Field(alias="ecoDist", default=None)
    power_time: Optional[int] = Field(alias="powerTime", default=None)
    power_dist: Optional[int] = Field(alias="powerDist", default=None)

    def __add__(self, other: _HDCModel):
        """Add together two HDCModel's.

        Handles Min/Max/Average fields correctly.

        Args:
        ----
        other: _SummaryBaseModel: to be added
        """
        if other is not None:
            self.ev_time = add_with_none(self.ev_time, other.ev_time)
            self.ev_distance = add_with_none(self.ev_distance, other.ev_distance)
            self.charge_time = add_with_none(self.charge_time, other.charge_time)
            self.charge_dist = add_with_none(self.charge_dist, other.charge_dist)
            self.eco_time = add_with_none(self.eco_time, other.eco_time)
            self.eco_dist = add_with_none(self.eco_dist, other.eco_dist)
            self.power_time = add_with_none(self.power_time, other.power_time)
            self.power_dist = add_with_none(self.power_dist, other.power_dist)

        return self


class _RouteModel(BaseModel):
    lat: float = Field(repr=False)
    lon: float
    overspeed: bool
    highway: bool
    index_in_points: int = Field(alias="indexInPoints")
    mode: Optional[int] = None
    is_ev: bool = Field(alias="isEv")


class _TripModel(BaseModel):
    id: UUID
    category: int
    summary: _SummaryModel
    scores: _ScoresModel
    behaviours: Optional[List[_BehaviourModel]] = None
    hdc: Optional[_HDCModel] = None
    route: Optional[List[_RouteModel]] = None


class _HistogramModel(BaseModel):
    year: int
    month: int
    day: int
    summary: _SummaryBaseModel
    scores: Optional[_ScoresModel] = None
    hdc: Optional[_HDCModel] = None


class _SummaryItemModel(BaseModel):
    year: int
    month: int
    summary: _SummaryBaseModel
    scores: _ScoresModel
    hdc: Optional[_HDCModel] = None
    histograms: List[_HistogramModel]


class _PaginationModel(BaseModel):
    limit: int
    offset: int
    previous_offset: Optional[Any] = Field(alias="previousOffset", default=None)
    next_offset: Optional[int] = Field(alias="nextOffset", default=None)
    current_page: int = Field(alias="currentPage")
    total_count: int = Field(alias="totalCount")
    page_count: int = Field(alias="pageCount")


class _SortedByItemModel(BaseModel):
    field: str
    order: str


class _MetadataModel(BaseModel):
    pagination: _PaginationModel
    sorted_by: List[_SortedByItemModel] = Field(alias="sortedBy")


class TripsModel(BaseModel):
    r"""Model representing trips data.

    Attributes
    ----------
        from_date (date): The start date of the trips.
        to_date (date): The end date of the trips.
        trips (List[_TripModel]): The list of trips.
        summary (Optional[List[_SummaryItemModel]], optional): The summary of the trips. \n
            Defaults to None.
        metadata (_MetadataModel): The metadata of the trips.
        route (Optional[_RouteModel], optional): The route of the trips. \n
            Defaults to None.

    """

    from_date: date = Field(..., alias="from")
    to_date: date = Field(..., alias="to")
    trips: List[_TripModel]
    summary: Optional[List[_SummaryItemModel]] = None
    metadata: _MetadataModel = Field(..., alias="_metadata")
    route: Optional[_RouteModel] = None


class TripsResponseModel(StatusModel):
    r"""Model representing a trips response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[TripsModel], optional): The trips payload. \n
            Defaults to None.

    """

    payload: Optional[TripsModel] = None
