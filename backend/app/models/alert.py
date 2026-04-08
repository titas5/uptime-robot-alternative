from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base

class AlertType(str, enum.Enum):
    email = "email"
    webhook = "webhook"

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    monitor_id = Column(Integer, ForeignKey("monitors.id"))
    type = Column(Enum(AlertType))
    target = Column(String, nullable=False) # email address or webhook URL
    created_at = Column(DateTime, server_default=func.now())

    monitor = relationship("Monitor", back_populates="alerts")
