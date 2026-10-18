from app.risk import assess_risk
from app.schemas import TelemetryReading
from app.simulator import generate_readings


def test_simulator_is_reproducible_for_seed() -> None:
    first = generate_readings(samples=8, seed=7)
    second = generate_readings(samples=8, seed=7)
    fields = ("temperature_c", "humidity_pct", "battery_pct", "solar_power_w", "load_power_w")
    assert [[getattr(item, field) for field in fields] for item in first] == [
        [getattr(item, field) for field in fields] for item in second
    ]


def test_simulator_bounds_sample_count() -> None:
    try:
        generate_readings(samples=0)
    except ValueError as exc:
        assert "samples" in str(exc)
    else:
        raise AssertionError("Expected invalid sample count to fail")


def test_risk_increases_for_high_temperature_and_low_battery() -> None:
    reading = TelemetryReading(
        timestamp="2026-01-01T00:00:00Z",
        temperature_c=10,
        humidity_pct=70,
        battery_pct=15,
        solar_power_w=0,
        load_power_w=330,
    )
    result = assess_risk([reading])
    assert result.score >= 65
    assert result.level in {"high", "critical"}
    assert result.advisory_only is True


def test_normal_conditions_are_low_risk() -> None:
    reading = TelemetryReading(
        timestamp="2026-01-01T00:00:00Z",
        temperature_c=4,
        humidity_pct=65,
        battery_pct=80,
        solar_power_w=300,
        load_power_w=320,
    )
    result = assess_risk([reading])
    assert result.score == 0
    assert result.level == "low"
