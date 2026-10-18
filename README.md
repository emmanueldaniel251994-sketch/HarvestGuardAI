# HarvestGuard AI

**Predict. Protect. Preserve.** An evidence-driven monitoring and predictive-risk platform for solar-powered agricultural cold storage, initially targeting Nigeria.

> **Data transparency:** The current prototype uses deterministic simulated telemetry. It does not connect to physical sensors and does not control refrigeration, batteries, inverters, or electrical circuits. Outputs are advisory.

## Architecture

- `frontend/`: Next.js + TypeScript dashboard.
- `backend/`: FastAPI API, SQLAlchemy persistence, Alembic migrations, simulator, rule-based risk assessment, and an optional offline ML experiment.
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
- Device-key-protected single and batch telemetry ingestion, plus a separate synthetic-demo seeding endpoint and stored history.
- Per-cold-room advisory risk endpoint based on stored readings and each site's configured temperature bounds.
- Dashboard view for registered rooms, stored reading history, risk factors, and CSV export.
- SQLAlchemy cold-room and telemetry models with Alembic migrations.
- Reproducible simulated telemetry endpoint.
- Explainable threshold-based risk assessment.
- Dashboard component that requests telemetry from the API.
- Database readiness endpoint and Render deployment blueprint (`render.yaml`).
- Sensor integration contract, device API-key configuration, and hackathon demo walkthrough in `docs/`.
- Optional chronological ML experiment comparing a most-frequent baseline with a random-forest candidate; requires reviewed labelled CSV data.

## Planned next

- Verify CI and frontend production build.
- Add per-device identity, key rotation/revocation, user authentication for room/history/risk endpoints, and rate limiting before public production use.
- Add commodity-specific profiles with reviewed thresholds.
- Collect representative independently labelled data, run and review the optional ML experiment, and publish metrics/model card before making predictive claims.
- Deploy frontend to Vercel and backend to Render.

All demo readings and prototype risk scores are illustrative. Do not use them for food-safety decisions or equipment control.
