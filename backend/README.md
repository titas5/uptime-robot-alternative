# Uptime Monitoring Backend - Native Services Setup (No Docker)

If you prefer to run the backend natively without Docker (similar to a LAMP stack approach), you must manually run PostgreSQL, Redis, and the Python services natively on your system or server.

## Prerequisites
1. **Python 3.11+**
2. **PostgreSQL 15+**
3. **Redis 7+**

---

## 1. Environment Setup

Copy your environment configurations. You can create a `.env` file in the `backend` folder.

```env
# Example .env configuration
DATABASE_URL=postgresql://your_db_user:your_db_password@localhost:5432/uptime_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=YOUR_SUPER_SECRET_KEY
```

## 2. Infrastructure Setup (Database & Redis)

### PostgreSQL Setup
If you have PostgreSQL installed, you need to create the database and a user. Open your `psql` console:

```sql
CREATE DATABASE uptime_db;
CREATE USER your_db_user WITH ENCRYPTED PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE uptime_db TO your_db_user;
```

### Redis Setup
Ensure your local Redis server is running and accessible on the default port `6379`. On most Linux systems, you can ensure it's running via:
```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
```
*(On Windows, you can use WSL, Memurai, or install a Redis port for Windows)*.

---

## 3. Python Environment & Dependencies Setup

You need to establish a virtual environment for Python to keep dependencies isolated:

```bash
# Move to the backend folder
cd backend

# Create a Python virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate

# Install the application dependencies
pip install -r requirements.txt
```

---

## 4. Running the Application

Once your database, redis, and virtual environment are set up, you need to run three separate processes for the entire backend application to function fully. It is recommended to use something like `tmux`, `screen`, or `systemd` (Supervisor/PM2) to keep these running in the background on a production server.

### Process 1: The API Server (FastAPI)
Run the core API service handling web requests:
```bash
# If using development mode:
uvicorn app.main:app --host 0.0.0.0 --port 5555 --reload

# For production, it's recommended to run without --reload and to use Gunicorn:
# gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5555
```

### Process 2: Celery Background Worker
The worker is responsible for actually pinging/checking the user's monitors. It polls Redis for tasks.
```bash
# From the backend folder (in a new terminal / session, ensure virtual environment is activated):
celery -A app.workers.celery_app worker --loglevel=info
```
*(Note for Windows users: Celery can occasionally have trouble on native Windows. Using `celery -A app.workers.celery_app worker --pool=solo --loglevel=info` might be necessary).*

### Process 3: Celery Scheduler (Beat)
The scheduler dispatches background tasks (like queuing multiple URLs up for checking every 1 minute).
```bash
# From the backend folder (in a new terminal / session, ensure virtual environment is activated):
celery -A app.workers.celery_app beat --loglevel=info
```

## Production Considerations (Summary)
To run this in a real "LAMP-like" server environment without docker seamlessly:
1. Put the Fast API Server behind a reverse proxy like **Nginx** or **Apache**.
2. Run your Uvicorn/Gunicorn API server, Celery worker, and Celery beat using process managers like **systemd** or **PM2** so that they run in the background and automatically restart upon failure or reboot.
