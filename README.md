# AI Emergency Healthcare Platform

Full-stack starter app with:
- React + TypeScript + Tailwind frontend
- FastAPI backend
- AI ranking for doctors and ambulances
- Guided emergency assistant (`location -> problem -> budget`)
- Compare engine
- Chat session APIs + WebSocket live stream
- Analytics dashboard APIs
- Real-time tracking simulation APIs
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
- `POST /compare`
- `POST /recommend`
- `GET /analytics`
- `POST /chat/session`
- `GET /chat/{session_id}/messages`
- `POST /chat/{session_id}/message`
- `WS /chat/ws/{session_id}`
- `POST /tracking/start`
- `GET /tracking/{tracking_id}`

## Deployment Strategy
- Frontend: Vercel/Netlify
- Backend: Docker + ECS/EKS/Cloud Run
- DB: PostgreSQL (set `DATABASE_URL`)
- Cache/queue: Redis + Celery/RQ for background ranking refresh

## Hackathon Pitch
We are building an AI Healthcare Optimization Engine that minimizes emergency decision time by ranking doctors and ambulances using multi-factor intelligence instead of simple listings.
