from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class Event_Actions(Enum):
    PAGE_VIEW = 'page_view'
    SESSION_GEN = 'session_gen'
    CLICK = 'click'


class Event_Category(Enum):
    BUTTON = 'button'


class TrackEventBase(BaseModel):
    dataset_id: str
    session_id: str


class TrackEventSessionCreate(TrackEventBase):
    action: Optional[str] = None
    remote_addr: Optional[str] = None


class TrackEventViewCreate(TrackEventSessionCreate):
    index: int


class TrackEventCreate(TrackEventViewCreate):
    category: str
    element_label: str


class TrackEvent(TrackEventBase):
    id: int
    action: str
    remote_addr: str = None
    index: Optional[str] = None
    category: Optional[str] = None
    element_label: Optional[str] = None
    element_value: Optional[str] = None
    creation_time: datetime = datetime.utcnow

    class Config:
        orm_mode = True


class StatisticTestsBase(BaseModel):
    page_view: int
    conversion_rates: Dict


class StatisticTests(StatisticTestsBase):
    index: int
    element_label: str
    page_view: int
    conversion_rates: Dict


class StatisticDatasetOut(BaseModel):
    dataset_id: str
    tests: List
    all: StatisticTestsBase


class CandidateImpressions(BaseModel):
    click: int = 0
    page_view: int = 0

    class Config:
        orm_mode = True


class BaselineIndices(BaseModel):
    indices: list

    class Config:
        orm_mode = True


class Dump(BaseModel):
    dump: list

    class Config:
        orm_mode = True
