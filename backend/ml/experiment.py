"""Offline, time-ordered risk-label experiment. Not used by the production API."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import balanced_accuracy_score, classification_report, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

NUMERIC_FEATURES = [
    "temperature_c",
    "humidity_pct",
    "battery_pct",
    "solar_power_w",
    "load_power_w",
]
CATEGORICAL_FEATURES = ["commodity"]
REQUIRED_COLUMNS = ["timestamp", *NUMERIC_FEATURES, *CATEGORICAL_FEATURES, "risk_label"]


def build_pipeline(estimator: object) -> Pipeline:
    numeric = Pipeline([("imputer", SimpleImputer(strategy="median"))])
    categorical = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessing = ColumnTransformer(
        [
            ("numeric", numeric, NUMERIC_FEATURES),
            ("categorical", categorical, CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline([("preprocessing", preprocessing), ("model", estimator)])


def run_experiment(csv_path: Path, output_dir: Path) -> dict[str, object]:
    data = pd.read_csv(csv_path)
    missing = sorted(set(REQUIRED_COLUMNS) - set(data.columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")
    if len(data) < 50:
        raise ValueError(
            "At least 50 labelled rows are required for this exploratory split; "
            "more representative, independently labelled data is strongly preferred."
        )

    data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True, errors="coerce")
    if data["timestamp"].isna().any():
        raise ValueError("Every row must have a valid ISO-compatible timestamp.")
    if data["risk_label"].isna().any():
        raise ValueError("risk_label cannot be blank; do not invent labels to fill gaps.")
    data = data.sort_values("timestamp").reset_index(drop=True)

    split_at = int(len(data) * 0.8)
    train, test = data.iloc[:split_at], data.iloc[split_at:]
    if train["risk_label"].nunique() < 2 or test["risk_label"].nunique() < 2:
        raise ValueError(
            "The chronological train and test portions must each contain at least "
            "two classes. Gather more time-spanning labelled observations."
        )

    feature_columns = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    x_train, x_test = train[feature_columns], test[feature_columns]
    y_train, y_test = train["risk_label"].astype(str), test["risk_label"].astype(str)

    baseline = build_pipeline(DummyClassifier(strategy="most_frequent"))
    candidate = build_pipeline(
        RandomForestClassifier(
            n_estimators=300,
            min_samples_leaf=3,
            class_weight="balanced",
            random_state=42,
        )
    )
    baseline.fit(x_train, y_train)
    candidate.fit(x_train, y_train)
    baseline_predictions = baseline.predict(x_test)
    candidate_predictions = candidate.predict(x_test)

    metrics: dict[str, object] = {
        "experiment": "chronological_rule_labelled_risk_baseline",
        "rows_total": int(len(data)),
        "rows_train": int(len(train)),
        "rows_test": int(len(test)),
        "train_period_utc": [
            train["timestamp"].min().isoformat(),
            train["timestamp"].max().isoformat(),
        ],
        "test_period_utc": [
            test["timestamp"].min().isoformat(),
            test["timestamp"].max().isoformat(),
        ],
        "labels": sorted(data["risk_label"].astype(str).unique().tolist()),
        "baseline_most_frequent": {
            "macro_f1": float(f1_score(y_test, baseline_predictions, average="macro", zero_division=0)),
            "balanced_accuracy": float(balanced_accuracy_score(y_test, baseline_predictions)),
        },
        "random_forest_candidate": {
            "macro_f1": float(f1_score(y_test, candidate_predictions, average="macro", zero_division=0)),
            "balanced_accuracy": float(balanced_accuracy_score(y_test, candidate_predictions)),
            "classification_report": classification_report(
                y_test, candidate_predictions, output_dict=True, zero_division=0
            ),
        },
        "limitations": [
            "Exploratory only; no evidence of deployment readiness.",
            "Labels require documented provenance and independent review.",
            "Threshold-derived labels only measure agreement with those thresholds, not spoilage outcomes.",
            "A single chronological holdout is not external validation.",
            "Do not use for food-safety decisions or equipment control.",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    joblib.dump(candidate, output_dir / "risk_model.joblib")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", required=True, type=Path, help="Reviewed labelled telemetry CSV")
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/risk-experiment"))
    args = parser.parse_args()
    metrics = run_experiment(args.csv, args.output_dir)
    print(json.dumps({
        "rows_total": metrics["rows_total"],
        "baseline": metrics["baseline_most_frequent"],
        "candidate": metrics["random_forest_candidate"],
        "output_dir": str(args.output_dir),
    }, indent=2))


if __name__ == "__main__":
    main()
