# HarvestGuard AI

**Predict. Protect. Preserve.** An evidence-driven monitoring and predictive-risk platform for solar-powered agricultural cold storage, initially targeting Nigeria.

> **Data transparency:** The current prototype uses deterministic simulated telemetry. It does not connect to physical sensors and does not control refrigeration, batteries, inverters, or electrical circuits. Outputs are advisory.

## Architecture

- `frontend/`: Next.js + TypeScript dashboard.
- `backend/`: FastAPI API, SQLAlchemy persistence, Alembic migrations, simulator, and rule-based risk assessment.
- `docs/`: architecture, API, data dictionary, deployment and safety notes.

## Prerequisites

- Python 3.11+
- Node.js 20.9+ and npm
- Git
- Docker Compose (optional, for local PostgreSQL)

## Local setup

### Backend

```bash
cd backend
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
cp .env.example .env  # Windows: Copy-Item .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

API health: `http://127.0.0.1:8000/health`. Interactive API docs: `http://127.0.0.1:8000/docs`.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local  # Windows: Copy-Item .env.example .env.local
npm run dev
```

Frontend: `http://localhost:3000`. Set `NEXT_PUBLIC_API_URL` to the backend base URL when the API is deployed.

### PostgreSQL (optional for local development)

From the repository root, run `docker compose up -d db`. Configure `DATABASE_URL` in `backend/.env` to the local PostgreSQL connection string before running migrations.

## Tests

```bash
cd backend
pip install -r requirements.txt
pytest
```

## Implemented so far

- FastAPI health endpoint.
- Cold-room registration and listing API.
- Persisted telemetry ingestion and history endpoints.\n- Per-cold-room advisory risk endpoint based on stored readings.\n- Dashboard view for registered rooms, stored reading history, and risk factors.
- SQLAlchemy cold-room and telemetry models with Alembic migrations.
- Reproducible simulated telemetry endpoint.
- Explainable threshold-based risk assessment.
- Dashboard component that requests telemetry from the API.
- Backend tests and GitHub Actions workflow configuration.

## Planned next

- Verify CI and frontend production build.
- Connect cold-room selection and stored history to the dashboard.
- Add commodity-specific profiles with reviewed thresholds.
- Add baseline ML experiments, metrics and model card before making predictive claims.
- Deploy frontend to Vercel and backend to Render.

All demo readings and prototype risk scores are illustrative. Do not use them for food-safety decisions or equipment control.
