# Split Server Deployment Guide

This guide explains how to decouple the platform across two independent servers:
- **Server 1**: Backend API, Celery Workers, Redis, and PostgreSQL Database
- **Server 2**: Next.js React Frontend

---

## 🖥 Server 1: Backend & Database

This server handles all the background monitoring logic and data storage. You'll run the existing Docker Compose stack here.

### 1. Configure the Server
SSH into your first VPS (e.g., Ubuntu) and clone the repository. Ensure you have Docker and Docker Compose installed.

### 2. Docker Execution
By default, the `docker-compose.yml` file in the root directory manages everything perfectly for this use case. No changes are needed to the docker topology itself since the frontend was purposely never grouped in the docker-compose schema to begin with.

Simply boot up the stack:
```bash
docker-compose up -d --build
```

### 3. Exposing the API
Your API now natively runs on `http://<SERVER_1_IP>:8000/api/v1`. 
*Note: For production, it's highly recommended you put an Nginx Reverse Proxy over port 8000 to assign an SSL Certificate mapping it to a real domain like `https://api.yourdomain.com/api/v1`.*

---

## 🌐 Server 2: Frontend (Next.js)

This environment will exclusively serve your UI Dashboard.

### Option A: Vercel (Recommended API Edge-Network)
Vercel is the creator of Next.js and is optimized to run frontend frameworks securely scale-free.
1. Push your `frontend` code folder to a new standalone GitHub Repository.
2. Log into Vercel and import the repository.
3. In the Vercel **Environment Variables** deployment section, add:
   - `NEXT_PUBLIC_API_URL` = `http://<SERVER_1_IP>:8000/api/v1` *(or use your backend's SSL configured domain)*
4. Click **Deploy**.

### Option B: Dedicated Linux VPS (e.g., Ubuntu)
If you wish to host the frontend stack yourself manually on a second generic Linux Server:

1. Install Node.js (`v18+`)
2. SSH into Server 2 and navigate to the newly cloned `frontend/` directory.
3. Create a `.env` file mapping the traffic strictly towards Server 1's connection:
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://<SERVER_1_IP>:8000/api/v1" > .env
   ```
4. Install Modules and Bundle the Production Build:
   ```bash
   npm install
   npm run build
   ```
5. Keep it alive persistently across reboots utilizing PM2:
   ```bash
   npm install -g pm2
   pm2 start npm --name "uptime-frontend" -- start
   ```

## 🔗 Architecture Communication Target
The communication cross-talk relies entirely on `frontend/services/api.ts`. The Axios default URL has been explicitly coded to adapt via `process.env.NEXT_PUBLIC_API_URL`. As long as you inject that environment variable onto your Frontend mapping accurately to the IP layer of your Backend container block, the UI interfaces cross-network flawlessly.
