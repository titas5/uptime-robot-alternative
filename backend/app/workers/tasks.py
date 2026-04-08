import requests
from requests.exceptions import RequestException
import time
import subprocess
import platform
from sqlalchemy.orm import Session
from app.workers.celery_app import celery_app
from app.db.database import SessionLocal
from app.models.monitor import Monitor, MonitorStatus
from app.models.monitor_log import MonitorLog

def perform_http_check(url: str, retries: int = 3) -> tuple[bool, float]:
    for attempt in range(retries):
        start_time = time.time()
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            elapsed = (time.time() - start_time) * 1000
            return True, elapsed
        except RequestException:
            if attempt == retries - 1:
                return False, 0.0
            time.sleep(1)
    return False, 0.0

def perform_ping_check(url: str, retries: int = 3) -> tuple[bool, float]:
    host = url.replace("http://", "").replace("https://", "").split("/")[0]
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    for attempt in range(retries):
        start_time = time.time()
        try:
            command = ['ping', param, '1', host]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
            if result.returncode == 0:
                elapsed = (time.time() - start_time) * 1000
                return True, elapsed
        except Exception:
            pass
        if attempt < retries - 1:
            time.sleep(1)
    return False, 0.0

def perform_keyword_check(url: str, keyword: str, retries: int = 3) -> tuple[bool, float]:
    for attempt in range(retries):
        start_time = time.time()
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            elapsed = (time.time() - start_time) * 1000
            if keyword and keyword.lower() in response.text.lower():
                return True, elapsed
            return False, elapsed
        except RequestException:
            if attempt == retries - 1:
                return False, 0.0
            time.sleep(1)
    return False, 0.0

@celery_app.task
def check_monitor(monitor_id: int):
    # This will check individual monitor
    db: Session = SessionLocal()
    try:
        monitor = db.query(Monitor).filter(Monitor.id == monitor_id).first()
        if not monitor or monitor.status == MonitorStatus.paused:
            return

        is_up = False
        response_time = 0.0

        if monitor.type == "http":
            is_up, response_time = perform_http_check(monitor.url)
        elif monitor.type == "ping":
            is_up, response_time = perform_ping_check(monitor.url)
        elif monitor.type == "keyword":
            is_up, response_time = perform_keyword_check(monitor.url, monitor.keyword or "")
        
        new_status = MonitorStatus.up if is_up else MonitorStatus.down

        # Trigger alert logic here
        from app.services.alerts import trigger_alerts
        trigger_alerts(db, monitor, new_status)

        monitor.status = new_status
        db.add(monitor)

        # Record check in log
        log = MonitorLog(
            monitor_id=monitor.id,
            status=new_status,
            response_time=response_time
        )
        db.add(log)
        db.commit()

    finally:
        db.close()

@celery_app.task
def schedule_monitor_checks():
    db: Session = SessionLocal()
    try:
        # In a real app we'd filter by 'checked_at' + 'interval'
        # For simplicity in this demo, pulling active monitors to schedule
        monitors = db.query(Monitor).filter(Monitor.status != MonitorStatus.paused).all()
        for monitor in monitors:
            check_monitor.delay(monitor.id)
    finally:
        db.close()
