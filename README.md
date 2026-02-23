# AI Emergency Healthcare Platform

Full-stack starter app with:
- React + TypeScript + Tailwind frontend
- FastAPI backend
- AI ranking for doctors and ambulances
- AI emergency triage engine (severity + type + escalation)
- Dynamic AI doctor/ambulance/hospital ranking with explainability
- Hospital intelligence engine + dispatch workflow
- Guided emergency assistant (`location -> problem -> budget`)
- Compare engine
- Chat session APIs + WebSocket live stream
- Analytics dashboard APIs
- Real-time tracking + WebSocket live updates
- WhatsApp direct links

## Project Structure
- `/frontend` web app
- `/backend` API app

## Run Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend runs at `http://127.0.0.1:8000`

## Run AI Microservice (optional)
```bash
cd ai-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```
AI service runs at `http://127.0.0.1:8010`

## Default Admin Login (seeded)
- Email: `admin@medai.com`
- Password: `admin123`

## Run Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://127.0.0.1:5173`

## Core Endpoints
- `GET /doctors`
- `GET /doctor/{id}`
- `GET /ambulances`
- `GET /ambulance/{id}`
- `GET /hospitals`
- `GET /hospitals/{id}`
- `POST /compare`
- `POST /recommend`
- `POST /triage`
- `POST /rank/doctors`
- `POST /rank/ambulances`
- `POST /rank/hospitals`
- `GET /why-ranked/{emergency_id}/{target_type}/{target_id}`
- `POST /dispatch`
- `POST /feedback`
- `POST /auth/register`
- `POST /auth/login`
- `GET /analytics`
- `GET /analytics/forecast`
- `POST /chat/session`
- `GET /chat/{session_id}/messages`
- `POST /chat/{session_id}/message`
- `WS /chat/ws/{session_id}`
- `POST /tracking/start`
- `GET /tracking/{tracking_id}`
- `WS /tracking/ws/{tracking_id}`

## Deployment Strategy
- Frontend: Vercel/Netlify
- Backend: Docker + ECS/EKS/Cloud Run
- DB: PostgreSQL (set `DATABASE_URL`)
- Cache/queue: Redis + Celery/RQ for background ranking refresh

## Hackathon Pitch
We are building an AI Healthcare Optimization Engine that minimizes emergency decision time by ranking doctors and ambulances using multi-factor intelligence instead of simple listings.
