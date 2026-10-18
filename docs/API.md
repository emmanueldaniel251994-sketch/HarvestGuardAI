# API reference (current foundation)

Base URL for local development: `http://127.0.0.1:8000`. Interactive documentation is available at `/docs` when running locally.

## Health

`GET /health`

Returns a simple service health response. It does not prove database connectivity.

`GET /health/ready`

Executes a lightweight database query and returns `503` if the database cannot be reached. Use this for readiness checks where database availability is required.

## Cold rooms

### List cold rooms

`GET /api/v1/cold-rooms`

Returns registered cold-room records in ID order.

### Register a cold room

`POST /api/v1/cold-rooms`

Example JSON body:

```json
{
  "name": "Ado Produce Store",
  "location": "Ado-Ekiti, Ekiti State",
  "commodity": "Tomatoes",
  "target_min_c": 3,
  "target_max_c": 8,
  "notes": "Optional notes",
  "active": true
}
```

Temperature bounds are configurable metadata only; they are not verified commodity-specific recommendations. The API rejects a minimum temperature that is greater than or equal to the maximum.

## Stored telemetry history

### Record a reading

`POST /api/v1/cold-rooms/{cold_room_id}/readings`

Submit one validated reading for an existing cold room. The endpoint returns `404` when the cold-room ID is unknown. This endpoint does not authenticate sensor devices yet; do not expose it publicly until authentication and rate limiting are added.

### Record a batch of readings

`POST /api/v1/cold-rooms/{cold_room_id}/readings/bulk`

Request body:

```json
{
  "readings": [
    {
      "timestamp": "2026-10-18T10:00:00Z",
      "temperature_c": 4.5,
      "humidity_pct": 68,
      "battery_pct": 77,
      "solar_power_w": 410,
      "load_power_w": 320
    }
  ]
}
```

Accepts 1–168 readings and stores them in one database transaction. The endpoint is intended for demos and trusted clients until device authentication is implemented. It returns `404` when the cold room does not exist.

### List readings

`GET /api/v1/cold-rooms/{cold_room_id}/readings?limit=100`

Returns stored readings newest first. `limit` is between 1 and 500, default 100. A missing cold room returns `404`.

### Assess stored-reading risk

`GET /api/v1/cold-rooms/{cold_room_id}/risk?limit=24`

Returns an advisory rule-based score and explanatory factors for up to the newest 168 stored readings (default 24). Temperature excursions use the selected cold room's configured `target_min_c` and `target_max_c` metadata. Returns `404` if the cold room does not exist. With no stored readings, the score is zero and the factors state that no readings are available. Configured ranges must be reviewed for the commodity; the score is not a trained ML prediction or validated food-safety advice.

## Simulated telemetry

`GET /api/v1/demo/telemetry?samples=24&seed=42`

Returns deterministic illustrative readings and a transparent threshold-based risk assessment.

Query parameters:
- `samples`: integer from 1 to 168, default 24.
- `seed`: non-negative integer, default 42. Reusing the same seed and sample count reproduces measurement values and risk result; timestamps are based on request time.

Response fields:
- `mode`: always `simulated` for this endpoint.
- `readings`: timestamp, temperature in °C, relative humidity percentage, battery percentage, solar power in watts, and load power in watts.
- `risk`: 0–100 rule-based score, severity level, and explanatory factors.
- `notice`: explicit warning that the readings are not live sensor data.

Thresholds are prototype heuristics, not validated food-safety guidance or a trained predictive model. Never use this endpoint to control physical equipment or replace applicable food-safety procedures.
