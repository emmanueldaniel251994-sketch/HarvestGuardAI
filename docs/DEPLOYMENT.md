# Deployment plan

This document describes the intended deployment path; it does not mean the services are already deployed.

## Frontend — Vercel

1. Import this GitHub repository into Vercel.
2. Set the project root directory to `frontend`.
3. Set `NEXT_PUBLIC_API_URL` to the deployed backend URL (for example, `https://your-api.onrender.com`).
4. Deploy and verify the dashboard loads without build errors.

## Backend — Render

A starter blueprint is provided in the repository root as `render.yaml`. You can create a Render Blueprint from the repository or configure the service manually. The manifest uses the `backend` directory and runs Alembic migrations during the build. Review Render plan limitations and logs during setup.

1. Create a Web Service from this repository.
2. Set the root directory to `backend`.
3. Build command: `pip install -r requirements.txt`.
4. Configure `DATABASE_URL` to a managed PostgreSQL connection string and `CORS_ORIGINS` to the exact deployed frontend origin.
5. Run the migration as a pre-deploy command: `alembic upgrade head`.
6. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
7. Verify `/health`, `/api/v1/demo/telemetry`, and `/docs` after deployment.

## Database

Use a managed PostgreSQL instance for production and configure its connection string as a secret environment variable. Do not commit credentials. Apply Alembic migrations before starting a new release. Before production data is used, add and test backups, retention policies, database readiness checks, and access controls.

For local PostgreSQL development, use `docker compose up -d db` from the repository root. Set `DATABASE_URL` in `backend/.env` to the connection string shown in `backend/.env.example`.

## Release checklist

- [ ] Backend tests pass in CI.
- [ ] Alembic migration succeeds on the target database.
- [ ] Frontend production build succeeds.
- [ ] Health endpoint responds on the deployed API.
- [ ] Frontend points to the deployed API and CORS permits only its origin.
- [ ] No secrets are committed.
- [ ] Demo values are clearly labelled as simulated.
- [ ] Write endpoints have appropriate authentication before public production use.
- [ ] Physical sensor and equipment-control claims are not made unless implemented and validated.
