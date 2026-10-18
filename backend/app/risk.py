from app.schemas import RiskAssessment, TelemetryReading


def assess_risk(
    readings: list[TelemetryReading],
    target_min_c: float = 2.0,
    target_max_c: float = 8.0,
) -> RiskAssessment:
    """Score readings with transparent configured thresholds, not a trained model."""
    if target_min_c >= target_max_c:
        raise ValueError("target_min_c must be lower than target_max_c")
    if not readings:
        return RiskAssessment(score=0, level="low", factors=["No readings available"])

    latest = readings[-1]
    score = 0
    factors: list[str] = []

    temperatures = [reading.temperature_c for reading in readings]
    excursion_count = sum(
        temp > target_max_c or temp < target_min_c for temp in temperatures
    )
    if latest.temperature_c > target_max_c:
        score += 40
        factors.append(
            f"Latest temperature is above the configured maximum ({target_max_c:g}°C)"
        )
    elif latest.temperature_c < target_min_c:
        score += 25
        factors.append(
            f"Latest temperature is below the configured minimum ({target_min_c:g}°C)"
        )
    if excursion_count >= max(2, len(readings) // 4):
        score += 20
        factors.append(
            f"Repeated temperature excursions outside the configured "
            f"{target_min_c:g}–{target_max_c:g}°C range"
        )
    if latest.battery_pct < 20:
        score += 25
        factors.append("Battery reserve is below 20%")
    elif latest.battery_pct < 35:
        score += 12
        factors.append("Battery reserve is below 35%")
    if latest.load_power_w > max(1.0, latest.solar_power_w) and latest.battery_pct < 35:
        score += 10
        factors.append("Load exceeds solar generation while battery reserve is low")

    score = min(100, score)
    if score >= 75:
        level = "critical"
    elif score >= 50:
        level = "high"
    elif score >= 25:
        level = "moderate"
    else:
        level = "low"

    if not factors:
        factors.append("No configured risk thresholds were crossed")
    return RiskAssessment(score=score, level=level, factors=factors)
