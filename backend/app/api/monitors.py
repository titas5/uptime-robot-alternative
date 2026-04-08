from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.monitor import Monitor
from app.models.monitor_log import MonitorLog
from app.schemas.monitor import MonitorCreate, MonitorUpdate, MonitorResponse, MonitorLogResponse

router = APIRouter()

@router.get("/", response_model=List[MonitorResponse])
def get_monitors(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Monitor).filter(Monitor.user_id == current_user.id).all()

@router.post("/", response_model=MonitorResponse)
def create_monitor(monitor_in: MonitorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    monitor = Monitor(
        **monitor_in.model_dump(),
        user_id=current_user.id
    )
    db.add(monitor)
    db.commit()
    db.refresh(monitor)
    return monitor

@router.put("/{id}", response_model=MonitorResponse)
def update_monitor(id: int, monitor_in: MonitorUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    monitor = db.query(Monitor).filter(Monitor.id == id, Monitor.user_id == current_user.id).first()
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    
    update_data = monitor_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(monitor, field, value)
    
    db.add(monitor)
    db.commit()
    db.refresh(monitor)
    return monitor

@router.delete("/{id}")
def delete_monitor(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    monitor = db.query(Monitor).filter(Monitor.id == id, Monitor.user_id == current_user.id).first()
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    
    db.delete(monitor)
    db.commit()
    return {"message": "Monitor deleted successfully"}

@router.get("/{id}/logs", response_model=List[MonitorLogResponse])
def get_monitor_logs(id: int, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    monitor = db.query(Monitor).filter(Monitor.id == id, Monitor.user_id == current_user.id).first()
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    
    logs = db.query(MonitorLog).filter(MonitorLog.monitor_id == id).order_by(MonitorLog.checked_at.desc()).limit(limit).all()
    return logs

from datetime import datetime, timedelta
from app.schemas.monitor import MonitorStatsResponse

@router.get("/{id}/stats", response_model=MonitorStatsResponse)
def get_monitor_stats(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    monitor = db.query(Monitor).filter(Monitor.id == id, Monitor.user_id == current_user.id).first()
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    
    def calc_uptime(days: int) -> float:
        cutoff = datetime.utcnow() - timedelta(days=days)
        logs = db.query(MonitorLog.status).filter(
            MonitorLog.monitor_id == id,
            MonitorLog.checked_at >= cutoff
        ).all()
        if not logs:
            return 100.0
        up_count = sum(1 for log in logs if log[0] == "up")
        return round((up_count / len(logs)) * 100, 2)
    
    return {
        "uptime_24h": calc_uptime(1),
        "uptime_7d": calc_uptime(7),
        "uptime_30d": calc_uptime(30),
    }
