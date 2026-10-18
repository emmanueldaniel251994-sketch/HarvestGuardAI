# API reference (current foundation)

Base URL for local development: `http://127.0.0.1:8000`. Interactive documentation is available at `/docs` when running locally.

## Health

`GET /health`

Returns a simple service health response. It does not yet prove database connectivity.

## Simulated telemetry

`GET /api/v1/demo/telemetry?samples=24&seed=42`

Returns deterministic illustrative readings and a transparent threshold-based risk assessment.

Query parameters:
- `samples`: integer from 1 to 168, default 24.
- `seed`: non-negative integer, default 42. Reusing the same seed and sample count reproduces the measurement values and risk result; timestamps are based on request time.

Response fields:
- `mode`: always `simulated` for this endpoint.
- `readings`: timestamp, temperature in °C, relative humidity percentage, battery percentage, solar power in watts, and load power in watts.
- `risk`: 0–100 rule-based score, severity level, and explanatory factors.
- `notice`: explicit warning that the readings are not live sensor data.

Thresholds are prototype heuristics, not validated food-safety guidance or a trained predictive model. Never use this endpoint to control physical equipment or replace applicable food-safety procedures.
