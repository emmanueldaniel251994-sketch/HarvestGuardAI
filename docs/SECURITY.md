# Security and safety notes

## Current prototype boundaries

- Demo telemetry is synthetic and must be labelled as simulated.
- The API currently has no user authentication or role-based access control.
- Cold-room registration endpoints are suitable only for controlled demos until access controls and abuse protections are implemented.
- Do not store credentials, provider tokens, customer personal data, or production secrets in the repository.
- The prototype does not send equipment commands and must never be used to bypass physical refrigeration, battery, inverter, or electrical protections.

## Before public production deployment

- Add authentication and authorization for write endpoints.
- Add request throttling and payload limits.
- Configure CORS with exact trusted frontend origins; do not use wildcard origins with credentials.
- Store secrets only in hosting-provider environment settings.
- Use TLS, least-privilege database credentials, managed backups, and a documented retention policy.
- Add database readiness checks and structured, redacted logs.
- Validate and monitor sensor provenance, timestamps, units, missing readings, and outliers.
- Review commodity-specific storage ranges with qualified food-storage experts. Prototype risk scores are not food-safety advice.
- Evaluate any ML model against a documented baseline and representative labelled data before making predictive claims.
