# Data dictionary

All values from `/api/v1/demo/telemetry` are synthetic demonstration values, not measurements from a real cold room.

| Field | Type | Unit / range | Description |
|---|---|---|---|
| timestamp | ISO 8601 datetime | UTC | Timestamp assigned to the synthetic sample |
| temperature_c | number | °C, -30 to 60 schema bounds | Illustrative storage-air temperature |
| humidity_pct | number | 0–100% | Illustrative relative humidity |
| battery_pct | number | 0–100% | Illustrative battery state-of-charge percentage |
| solar_power_w | number | W, non-negative | Illustrative solar generation |
| load_power_w | number | W, non-negative | Illustrative electrical load |
| risk.score | integer | 0–100 | Prototype rule-based score |
| risk.level | category | low, moderate, high, critical | Severity band derived from the score |
| risk.factors | string list | explanatory text | Threshold conditions that contributed to the score |

Do not interpret this prototype's generic thresholds as crop-specific storage recommendations. Production use requires validated crop/commodity requirements, real sensor calibration, missing-data handling, timestamp quality checks, and domain review.
