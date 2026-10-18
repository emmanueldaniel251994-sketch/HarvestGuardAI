# Offline risk-model experiments

This is an optional research workflow. The FastAPI application does **not** load or serve this model. The current API risk score remains a transparent threshold-based heuristic.

## Data requirements

Install optional packages from \`backend/requirements-ml.txt\`. Prepare a CSV with at least 50 time-spanning labelled records and these columns:

| Column | Meaning |
|---|---|
| \`timestamp\` | Observation time, preferably UTC ISO 8601 |
| \`temperature_c\` | Measured temperature in degrees Celsius |
| \`humidity_pct\` | Relative humidity percentage |
| \`battery_pct\` | Battery state-of-charge percentage |
| \`solar_power_w\` | Measured solar input power in watts |
| \`load_power_w\` | Measured electrical load power in watts |
| \`commodity\` | Commodity identifier/name |
| \`risk_label\` | Reviewed target class, such as \`low\`, \`moderate\`, \`high\`, \`critical\` |

Use measured, consented, de-identified data where applicable. Record sensor provenance, calibration, gaps, data collection period, label definitions, who assigned labels, and the independent evidence supporting labels. Never label records by copying the current heuristic's output and then claim the model predicts real spoilage risk; that only trains it to imitate the heuristic.

## Run

From \`backend/\`:

\`\`\`bash
pip install -r requirements-ml.txt
python -m ml.experiment --csv path/to/reviewed-labels.csv --output-dir artifacts/risk-experiment
\`\`\`

The script sorts observations by timestamp and uses the earliest 80% for training and latest 20% for holdout evaluation. It compares a most-frequent-class baseline with a random-forest candidate and writes \`metrics.json\` and \`risk_model.joblib\` into the output directory.

Do not use random row splitting for time-correlated telemetry: nearby readings can leak almost identical conditions across train and test. The chronological split is still only a preliminary evaluation; it does not replace validation on a different site, season, sensor setup, or independently labelled dataset.

## Release gates

Before considering production use, require:
- Documented label provenance and a target tied to a real, meaningful outcome.
- Adequate examples for each class and analysis of class imbalance.
- Evaluation across sites and time periods, calibration/error analysis, and comparison with the rule-based baseline.
- Expert review of commodity-specific thresholds and operational alert consequences.
- Model versioning, reproducible data preparation, monitoring for drift, and a rollback path.
- A separately reviewed API integration and security assessment.

Until these conditions are met, treat experiment results as exploratory. Never use the model for food-safety decisions or automatic equipment control.
