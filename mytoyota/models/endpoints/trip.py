from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


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
    sortedBy: list[_SortedByModel]


class _ScoresModel(BaseModel):
    acceleration: int = Field(ge=0, le=100)
    advice: int = Field(ge=0, le=100, default=0)
    braking: int = Field(ge=0, le=100)
    constantSpeed: int = Field(ge=0, le=100, default=0)
    global_: Optional[int] = Field(ge=0, le=100, alias="global", default=None)


class _SummaryModel(BaseModel):
    countries: list[str]
    duration: int
    durationHighway: int
    durationIdle: int
    durationOverspeed: int
    fuelConsumption: float
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


class _MonthSummaryModel(BaseModel):
    hdc: Optional[_HDCModel] = None  # Only available on EV cars
    # histograms not imported
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


class _TripModel(BaseModel):
    # behaviours not imported
    category: int
    hdc: Optional[_HDCModel] = None  # Only available on EV cars
    id: UUID
    scores: _ScoresModel
    summary: _TripSummaryModel


class TripsModel(BaseModel):
    _metadata: _MetaDataModel
    from_date: date = Field(..., alias="from")
    to_date: date = Field(..., alias="to")
    summary: list[_MonthSummaryModel] = []
    trips: list[_TripModel] = []
