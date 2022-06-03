from sqlalchemy import Column, String, Integer, DateTime

from models.db import Base
from datetime import datetime
from enum import Enum


class Event_Actions(Enum):
    PAGE_VIEW = 'page_view'
    SESSION_GEN = 'session_gen'
    CLICK = 'click'

class TrackEvent(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(String(64), index=True, nullable=False)
    session_id = Column(String(64), index=True, nullable=False)
    action = Column(String(64), index=False, nullable=False)
    index = Column(Integer, index=False, nullable=True)
    category = Column(String(64), index=False, nullable=True)
    element_label = Column(String(64), index=False, nullable=True)
    element_value = Column(String(64), index=False, nullable=True)
    remote_addr = Column(String(256), index=False, nullable=True)
    creation_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<TrackEvent id:{self.id} datasetid:{self.dataset_id} action:{self.action}>'
