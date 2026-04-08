# UptimeMonitor Platform

A production-ready, highly scalable Uptime Monitoring SaaS platform designed as a lightweight, performant alternative to UptimeRobot. Built with modern, separated architecture utilizing FastAPI, Next.js, Celery, PostgreSQL, and Redis.

## 🧱 Architecture Overview

* **Frontend**: Next.js Pages Router + React + Recharts (hosted on Vercel or VPS)
* **Backend**: Python FastAPI (Handles REST API and business logic)
* **Worker Queue**: Celery + Redis (Handles periodic background HTTP/Ping/Keyword checks)
* **Database**: PostgreSQL (Stores users, monitors, historical check logs, and alerts config)

## ✨ Core Features

* **Advanced Monitoring**: Supports standard HTTP/HTTPS parsing, ICMP OS-level Pings, and custom Keyword payload searches.
* **Smart Alerts**: Emits Emails (using secure SMTP configurations) and Webhook JSON payloads instantly upon status-change differentials (UP/DOWN thresholds). Built in with Cooldown suppression mechanisms.
* **Modern Dashboard UI**: Gorgeous dark-mode UI with smooth micro-interactions, showcasing interactive Recharts line graphs mapping Response over Time alongside 24h, 7d, 30d uptime percentages.
* **Robust Security**: Fully isolated with JSON Web Token (JWT) architecture, robust Password Hashing via `bcrypt`, strict Pydantic input validation structures, and `slowapi` Rate Limiting built into the core API.

## 🚀 Getting Started Locally

### 1. Unified Docker Deployment (Recommended)
You can spawn the entire backend stack (PostgreSQL, Redis, FastAPI, Celery Workers, and the Celery Beat Scheduler) instantaneously using Docker from the root directory:

```bash
docker-compose up -d --build
```
*The API will be mapped to `http://localhost:8000`*.

### 2. Running Frontend
Navigate to the Next.js directory to spool up the web application:

```bash
cd frontend
npm install
npm run dev
```
*The application UI will render at `http://localhost:3000`*.

## ⚙️ Configuration & Environment

To route SMTP limits or customize PostgreSQL binds, apply `.env` variables onto your Docker execution bounds or pass them into the containers natively. Key variables supported inside `backend/app/core/config.py`:
- `DATABASE_URL`
- `REDIS_URL`
- `SECRET_KEY`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`

## 🤝 Project Structure

```text
/
├── backend/                  # FastAPI Application core
│   ├── app/
│   │   ├── api/              # Route Controllers
│   │   ├── core/             # Security / Configs / Rate limits
│   │   ├── db/               # SQLAlchemy connectors
│   │   ├── models/           # DB schema representations
│   │   ├── schemas/          # Pydantic typing
│   │   ├── services/         # Webhook & Email emission tools
│   │   └── workers/          # Celery background checkers
│   └── dockerfile            # Lean python runtime build wrapper
├── frontend/                 # Next.js Application Core
│   ├── components/           # Reusable functional React UI elements 
│   ├── context/              # Context providers (AuthContext)
│   ├── hooks/                # Async React Query abstractions
│   ├── pages/                # Application router
│   └── styles/               # Bespoke Global design architecture
└── docker-compose.yml        # Multi-node orchestration logic
```
