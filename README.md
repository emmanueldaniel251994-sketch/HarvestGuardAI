# HarvestGuard AI

**Predict. Protect. Preserve.** An evidence-driven monitoring and predictive-risk platform for solar-powered agricultural cold storage, initially targeting Nigeria.

> **Data transparency:** The initial release uses deterministic simulated telemetry. It does not connect to physical sensors and does not control refrigeration, batteries, inverters, or electrical circuits. Outputs are advisory.

## Architecture

- `frontend/`: Next.js + TypeScript application.
- `backend/`: FastAPI service, validation, domain logic, persistence, simulator and ML interfaces.
- `ml/`: datasets, experiments and evaluation artifacts.
- `docs/`: architecture, API, model card, data dictionary, deployment, security and demo documentation.

See [Architecture](docs/ARCHITECTURE.md) and [Deployment](docs/DEPLOYMENT.md).

## Prerequisites

- Python 3.11+ (3.12 recommended for broad package compatibility)
- Node.js 20.9+ and npm
- Docker Compose (optional, for local PostgreSQL)
- Git

## Local setup

### Backend

```bash
cd backend
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
cp .env.example .env  # Windows: Copy-Item .env.example .env
uvicorn app.main:app --reload
```

API health: `http://127.0.0.1:8000/health`. API docs: `http://127.0.0.1:8000/docs` in development.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local  # Windows: Copy-Item .env.example .env.local
npm run dev
```

Frontend: `http://localhost:3000`.

### PostgreSQL (optional in the initial foundation)

From the repository root, run `docker compose up -d db`. Set `DATABASE_URL` in `backend/.env` to the local PostgreSQL connection string. The current health endpoint does not yet assert database readiness; that will be added with the persistence phase.

## Tests

```bash
cd backend
pip install -r requirements.txt
pytest
```

## Current status

Phase 1 foundation: project structure, configuration examples, initial health endpoint, tests, CI skeleton, and architecture/deployment/security documentation. Cold-room persistence, telemetry simulation, risk calculations, frontend dashboard, predictive evaluation, Meta AI provider, and production deployment are subsequent phases and must not be represented as completed yet.

### Database migrations

From `backend/`, set `DATABASE_URL` to the intended database and run `alembic upgrade head`. Review migration scripts before applying them to production. The first migration creates the `cold_rooms` table.
