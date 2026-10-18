# Security and safety notes

## Current prototype boundaries

- Demo telemetry is synthetic and must be labelled as simulated.
- Device single-reading and batch ingestion require `X-Device-API-Key` when `DEVICE_API_KEY` is configured. Production (`APP_ENV=production`) rejects sensor writes with `503` if the key is missing; local development without a key is intentionally permissive for testing.
- The synthetic `/api/v1/cold-rooms/{id}/readings/demo` endpoint is separate and does not accept client-supplied sensor values. It remains a demo-only write surface and should be rate-limited before public launch.
- Cold-room registration, reading history, and risk endpoints still have no user authentication or role-based access control.
- Cold-room registration endpoints are suitable only for controlled demos until access controls and abuse protections are implemented.
- Do not store credentials, provider tokens, customer personal data, or production secrets in the repository.
- The prototype does not send equipment commands and must never be used to bypass physical refrigeration, battery, inverter, or electrical protections.

## Before public production deployment

- Add user authentication and authorization for cold-room creation, reading history, and risk endpoints; the shared device API key only protects sensor-write endpoints.
- Replace the shared device key with per-device identity, secure key provisioning and rotation, and revocation.
- Add request throttling and payload limits, particularly for public synthetic-demo generation.
- Configure CORS with exact trusted frontend origins; do not use wildcard origins with credentials.
- Store secrets only in hosting-provider environment settings.
- Use TLS, least-privilege database credentials, managed backups, and a documented retention policy.
- Add database readiness checks and structured, redacted logs.
- Validate and monitor sensor provenance, timestamps, units, missing readings, and outliers.
- Review commodity-specific storage ranges with qualified food-storage experts. Prototype risk scores are not food-safety advice.
- Evaluate any ML model against a documented baseline and representative labelled data before making predictive claims.
