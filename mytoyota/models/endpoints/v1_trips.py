""" Toyota Connected Services API - V1 Trips Models """
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field

from .common import _StatusModel

# pylint: disable=missing-class-docstring


class _PaginationModel(BaseModel):
    currentPage: int
    limit: int
    offset: int
    pageCount: int
    previousOffset: int
    totalCount: int


class _SortedByModel(BaseModel):
    field: str
    order: str


class _MetaDataModel(BaseModel):
    pagination: _PaginationModel
    sortedBy: List[_SortedByModel]


class _ScoresModel(BaseModel):
    acceleration: int = Field(ge=0, le=100)
    advice: int = Field(ge=0, le=100, default=0)
    braking: int = Field(ge=0, le=100)
    constantSpeed: int = Field(ge=0, le=100, default=0)
    global_: Optional[int] = Field(ge=0, le=100, alias="global", default=None)


class _SummaryModel(BaseModel):
    average_speed: float = Field(alias="averageSpeed")
    countries: List[str]
    duration: int
    durationHighway: int
    durationIdle: int
    durationOverspeed: int
    fuelConsumption: Optional[float] = None
    length: int
    lengthHighway: int
    lengthOverspeed: int
    maxSpeed: float


class _HDCModel(BaseModel):
    # Depending on
    #    car not being EV
    #    car being ev only
    #    car being hybrid but only used ev/fuel
    chargeDist: int = 0
    chargeTime: int = 0
    ecoDist: int = 0
    ecoTime: int = 0
    evDistance: int = 0
    evTime: int = 0
    powerDist: int = 0
    powerTime: int = 0


class _HistogramsModel(BaseModel):
    day: int
    hdc: Optional[_HDCModel]
    month: int
    scores: _ScoresModel
    summary: _SummaryModel
    year: int


class _AllSummaryModel(BaseModel):
    hdc: Optional[_HDCModel] = None  # Only available on EV cars
    histograms: List[_HistogramsModel]
    month: int = Field(..., ge=1, le=12)
    scores: _ScoresModel
    summary: _SummaryModel
    year: int


class _TripSummaryModel(_SummaryModel):
    averageSpeed: float
    endLat: float
    endLon: float
    endTs: datetime
    nightTrip: bool
    startLat: float
    startLon: float
    startTs: datetime


class _ContextModel(BaseModel):
    slope: float


class _BehavioursModel(BaseModel):
    coaching_msg: int = Field(alias="coachingMsg")
    context: _ContextModel
    diagnostic_msg: int = Field(alias="diagnosticMsg")
    good: bool
    lat: float
    lon: float
    priority: bool
    severity: float
    ts: datetime


class _RouteModel(BaseModel):
    highway: bool
    index_in_points: int = Field(alias="indexInPoints")
    is_ev: bool = Field(alias="isEv")
    lat: float
    lon: float
    mode: int
    overspeed: bool


class _TripModel(BaseModel):
    behaviours: List[_BehavioursModel]
    category: int
    hdc: Optional[_HDCModel] = None  # Only available on EV cars
    id: UUID
    route: List[_RouteModel]
    scores: _ScoresModel
    summary: _TripSummaryModel


class _TripsModel(BaseModel):
    _metadata: _MetaDataModel
    from_date: date = Field(..., alias="from")
    summary: List[_AllSummaryModel] = []
    to_date: date = Field(..., alias="to")
    trips: List[_TripModel] = []


class V1TripsModel(BaseModel):
    payload: _TripsModel
    status: _StatusModel
