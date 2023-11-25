from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class _Pagination(BaseModel):
    currentPage: int
    limit: int
    offset: int
    pageCount: int
    previousOffset: int
    totalCount: int


class _SortedBy(BaseModel):
    field: str
    order: str


class _MetaData(BaseModel):
    pagination: _Pagination
    sortedBy: list[_SortedBy]


class _Scores(BaseModel):
    acceleration: int = Field(ge=0, le=100)
    advice: int = Field(ge=0, le=100, default=0)
    braking: int = Field(ge=0, le=100)
    constantSpeed: int = Field(ge=0, le=100, default=0)
    global_: Optional[int] = Field(ge=0, le=100, alias="global", default=None)


class _Summary(BaseModel):
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


class _HDC(BaseModel):
    # Depending on
    #    car not being EV
    #    car being ev only
    #    car being hybrid but only used ev/fuel
    chargeDist: int = Field(0)
    chargeTime: int = Field(0)
    ecoDist: int = Field(0)
    ecoTime: int = Field(0)
    evDistance: int = Field(0)
    evTime: int = Field(0)
    powerDist: int = Field(0)
    powerTime: int = Field(0)


class _MonthSummary(BaseModel):
    hdc: Optional[_HDC] = Field(default=None)  # Only available on EV cars
    # histograms not imported
    month: int = Field(..., ge=1, le=12)
    scores: _Scores
    summary: _Summary
    year: int


class _TripSummary(_Summary):
    averageSpeed: float
    endLat: float
    endLon: float
    endTs: datetime
    nightTrip: bool
    startLat: float
    startLon: float
    startTs: datetime


class _Trip(BaseModel):
    # behaviours not imported
    category: int
    hdc: Optional[_HDC] = Field(default=None)  # Only available on EV cars
    id: UUID
    scores: _Scores
    summary: _TripSummary


class Trips(BaseModel):
    _metadata: _MetaData
    from_: date = Field(..., alias="from")
    summary: list[_MonthSummary] = []
    to: date
    trips: list[_Trip] = []
