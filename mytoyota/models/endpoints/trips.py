""" Toyota Connected Services API - V1 Trips Models """
from datetime import date, datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel

# pylint: disable=missing-class-docstring


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
    )  # Electric cars might not use fuel


class _SummaryModel(_SummaryBaseModel):
    start_lat: float = Field(alias="startLat")
    start_lon: float = Field(alias="startLon")
    start_ts: datetime = Field(alias="startTs")
    end_lat: float = Field(alias="endLat")
    end_lon: float = Field(alias="endLon")
    end_ts: datetime = Field(alias="endTs")
    night_trip: bool = Field(alias="nightTrip")


class _ContextModel(BaseModel):
    slope: float


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
    acceleration: int
    braking: int
    advice: Optional[int] = None
    constantSpeed: Optional[int] = None


class _HDCModel(BaseModel):
    ev_time: Optional[int] = Field(alias="evTime", default=None)
    ev_distance: Optional[int] = Field(alias="evDistance", default=None)
    charge_time: Optional[int] = Field(alias="chargeTime", default=None)
    charge_dist: Optional[int] = Field(alias="chargeDist", default=None)
    eco_time: Optional[int] = Field(alias="ecoTime", default=None)
    eco_dist: Optional[int] = Field(alias="ecoDist", default=None)
    power_time: Optional[int] = Field(alias="powerTime", default=None)
    power_dist: Optional[int] = Field(alias="powerDist", default=None)


class _RouteModel(BaseModel):
    lat: float
    lon: float
    overspeed: bool
    highway: bool
    index_in_points: int = Field(alias="indexInPoints")
    mode: int
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
    scores: _ScoresModel
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
    from_date: date = Field(..., alias="from")
    to_date: date = Field(..., alias="to")
    trips: List[_TripModel]
    summary: List[_SummaryItemModel]
    metadata: _MetadataModel = Field(..., alias="_metadata")
    route: Optional[_RouteModel] = None


class TripsResponseModel(StatusModel):
    payload: Optional[TripsModel] = None
