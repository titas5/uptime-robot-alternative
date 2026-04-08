from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base

class MonitorType(str, enum.Enum):
    http = "http"
    ping = "ping"
    keyword = "keyword"

class MonitorStatus(str, enum.Enum):
    up = "up"
    down = "down"
    paused = "paused"
    pending = "pending"

class Monitor(Base):
    __tablename__ = "monitors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    url = Column(String, nullable=False)
    type = Column(Enum(MonitorType), default=MonitorType.http)
    interval = Column(Integer, default=5) # minutes
    keyword = Column(String, nullable=True)
    status = Column(Enum(MonitorStatus), default=MonitorStatus.pending)
    last_alerted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="monitors")
    logs = relationship("MonitorLog", back_populates="monitor", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="monitor", cascade="all, delete-orphan")
