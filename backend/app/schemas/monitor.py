from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.monitor import MonitorType, MonitorStatus

class MonitorCreate(BaseModel):
    url: str
    type: MonitorType = MonitorType.http
    keyword: Optional[str] = None
    interval: int = 5 # minutes

class MonitorUpdate(BaseModel):
    url: Optional[str] = None
    type: Optional[MonitorType] = None
    keyword: Optional[str] = None
    interval: Optional[int] = None
    status: Optional[MonitorStatus] = None

class MonitorResponse(BaseModel):
    id: int
    user_id: int
    url: str
    type: MonitorType
    keyword: Optional[str] = None
    interval: int
    status: MonitorStatus
    created_at: datetime

    class Config:
        from_attributes = True

class MonitorLogResponse(BaseModel):
    id: int
    monitor_id: int
    status: MonitorStatus
    response_time: Optional[float] = None
    checked_at: datetime

    class Config:
        from_attributes = True

class MonitorStatsResponse(BaseModel):
    uptime_24h: float
    uptime_7d: float
    uptime_30d: float
