from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.monitor import MonitorStatus

class MonitorLog(Base):
    __tablename__ = "monitor_logs"

    id = Column(Integer, primary_key=True, index=True)
    monitor_id = Column(Integer, ForeignKey("monitors.id"))
    status = Column(Enum(MonitorStatus))
    response_time = Column(Float) # in milliseconds
    checked_at = Column(DateTime, server_default=func.now())

    monitor = relationship("Monitor", back_populates="logs")
