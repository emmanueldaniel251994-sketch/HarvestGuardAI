from app.schemas import RiskAssessment, TelemetryReading


def assess_risk(readings: list[TelemetryReading]) -> RiskAssessment:
    """Score simulated readings using transparent thresholds, not a trained model."""
    if not readings:
        return RiskAssessment(score=0, level="low", factors=["No readings available"])

    latest = readings[-1]
    score = 0
    factors: list[str] = []

    temperatures = [reading.temperature_c for reading in readings]
    excursion_count = sum(temp > 8.0 or temp < 2.0 for temp in temperatures)
    if latest.temperature_c > 8.0:
        score += 40
        factors.append("Latest temperature is above 8°C")
    elif latest.temperature_c < 2.0:
        score += 25
        factors.append("Latest temperature is below 2°C")
    if excursion_count >= max(2, len(readings) // 4):
        score += 20
        factors.append("Repeated temperature excursions in the selected window")
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
