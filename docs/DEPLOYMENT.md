# Deployment plan

This document describes the intended deployment path; it does not mean the services are already deployed.

## Frontend — Vercel

1. Import this GitHub repository into Vercel.
2. Set the project root directory to `frontend`.
3. Set `NEXT_PUBLIC_API_URL` to the deployed backend URL.
4. Deploy and verify the dashboard loads without build errors.

## Backend — Render

1. Create a Web Service from this repository.
2. Set the root directory to `backend`.
3. Build command: `pip install -r requirements.txt`.
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
5. Verify `/health` and `/docs` after deployment.

## Database

Use a managed PostgreSQL instance for production and configure its connection string as a secret environment variable. Do not commit credentials. Before production data is used, add and test migrations, backups, retention policies, and database readiness checks.

## Release checklist

- [ ] Backend tests pass in CI.
- [ ] Frontend production build succeeds.
- [ ] Health endpoint responds on the deployed API.
- [ ] Frontend points to the deployed API.
- [ ] No secrets are committed.
- [ ] Demo values are clearly labelled as simulated.
- [ ] Physical sensor and equipment-control claims are not made unless implemented and validated.
