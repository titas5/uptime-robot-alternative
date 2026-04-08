import smtplib
import requests
import logging
from email.message import EmailMessage
from datetime import datetime, timedelta
from app.core.config import settings
from app.models.monitor import Monitor, MonitorStatus
from app.models.alert import Alert, AlertType
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

def send_email_alert(to_email: str, subject: str, body: str):
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        logger.warning("SMTP not configured. Skipping email alert.")
        return
        
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = settings.EMAILS_FROM_EMAIL or settings.SMTP_USER
    msg["To"] = to_email

    try:
        if settings.SMTP_TLS:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT or 587)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT or 465)
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")

def send_webhook_alert(url: str, payload: dict):
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        logger.error(f"Failed to send webhook to {url}: {e}")

def trigger_alerts(db: Session, monitor: Monitor, new_status: MonitorStatus):
    COOLDOWN_MINUTES = 60 # Cooldown for sending repeated DOWN alerts
    now = datetime.utcnow()
    
    should_alert = False
    is_transition = monitor.status != new_status and monitor.status != MonitorStatus.pending
    
    if is_transition:
        should_alert = True
    elif new_status == MonitorStatus.down:
        if monitor.last_alerted_at is None or (now - monitor.last_alerted_at) > timedelta(minutes=COOLDOWN_MINUTES):
            should_alert = True
            
    if not should_alert:
        return
        
    alerts = db.query(Alert).filter(Alert.monitor_id == monitor.id).all()
    if not alerts:
        return
        
    status_str = "DOWN" if new_status == MonitorStatus.down else "UP"
    subject = f"Monitor Alert: {monitor.url} is {status_str}"
    body = f"Your monitor for {monitor.url} changed status to {status_str} at {now.isoformat()}."
    
    for alert in alerts:
        if alert.type == AlertType.email:
            send_email_alert(alert.target, subject, body)
        elif alert.type == AlertType.webhook:
            payload = {
                "monitor_id": monitor.id,
                "url": monitor.url,
                "status": status_str,
                "timestamp": now.isoformat()
            }
            send_webhook_alert(alert.target, payload)
            
    monitor.last_alerted_at = now
