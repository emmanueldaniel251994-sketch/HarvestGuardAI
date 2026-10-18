from datetime import datetime, timedelta, timezone
import random

from app.schemas import TelemetryReading


def generate_readings(samples: int = 24, seed: int = 42) -> list[TelemetryReading]:
    """Generate reproducible illustrative readings; never represents live hardware."""
    if not 1 <= samples <= 168:
        raise ValueError("samples must be between 1 and 168")

    rng = random.Random(seed)
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    readings: list[TelemetryReading] = []
    temperature = 4.0
    battery = 82.0

    for index in range(samples):
        temperature += rng.uniform(-0.45, 0.55)
        temperature = max(1.0, min(12.0, temperature))
        battery += rng.uniform(-2.2, 1.5)
        battery = max(5.0, min(100.0, battery))
        # Use a fixed synthetic daily cycle so values remain reproducible across requests.\n        hour = index % 24
        solar = max(0.0, 900 * rng.random()) if 6 <= hour <= 18 else 0.0
        load = 280 + 70 * rng.random()
        readings.append(
            TelemetryReading(
                timestamp=now - timedelta(hours=samples - index - 1),
                temperature_c=round(temperature, 2),
                humidity_pct=round(65 + rng.uniform(-8, 10), 1),
                battery_pct=round(battery, 1),
                solar_power_w=round(solar, 1),
                load_power_w=round(load, 1),
            )
        )
    return readings
