# Sensor integration plan

## Current status

The current application has no physical sensor connection. The demo endpoint generates synthetic telemetry, and the ingestion endpoint accepts a JSON reading submitted by a client. This document is an integration contract proposal, not evidence of deployed hardware.

## Proposed data path

1. A temperature/humidity sensor and power-system telemetry source connect to an edge controller (for example, an appropriately engineered ESP32 or industrial gateway).
2. The edge controller validates sensor readings, attaches a UTC timestamp, and buffers readings when connectivity is unavailable.
3. The controller sends readings over HTTPS to the API after device authentication is implemented.
4. The API validates and stores readings associated with a registered cold-room ID.
5. The dashboard retrieves the stored history and calculates an advisory threshold-based risk score.

Do not connect this prototype to compressor relays, battery protection circuits, inverters, or other equipment-control outputs.

## Proposed reading contract

```json
{
  "timestamp": "2026-10-18T10:00:00Z",
  "temperature_c": 4.5,
  "humidity_pct": 68.0,
  "battery_pct": 77.0,
  "solar_power_w": 410.0,
  "load_power_w": 320.0
}
```

Units:
- `timestamp`: ISO 8601 timestamp; UTC is recommended.
- `temperature_c`: degrees Celsius.
- `humidity_pct`: relative humidity from 0 to 100.
- `battery_pct`: state-of-charge percentage from 0 to 100.
- `solar_power_w`: measured solar input power in watts.
- `load_power_w`: measured electrical load power in watts.

Current API endpoint: `POST /api/v1/cold-rooms/{cold_room_id}/readings`. It is not authenticated. Do not send real operational telemetry to a publicly accessible instance until device identity, authentication, authorization, replay protection, throttling, and audit logging are implemented.

## Reliability requirements before field use

- Record sensor model, calibration status, location within the cold room, sampling interval, firmware version, and installation date.
- Reject or flag impossible values, stale timestamps, duplicate messages, missing samples, and abrupt implausible changes.
- Preserve the original reading and record quality flags instead of silently replacing measurements.
- Buffer locally during network outages and retry safely with idempotency keys.
- Monitor API availability, ingestion delay, clock drift, sensor disconnection, and database capacity.
- Have qualified technicians validate electrical installation and isolation. Do not use software estimates as substitutes for hardware safety controls.
- Establish commodity-specific operating ranges with qualified cold-chain/food-safety experts before operational alerts are relied on.
