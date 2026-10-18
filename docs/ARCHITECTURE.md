# Architecture

HarvestGuard AI is an advisory monitoring concept for solar-powered agricultural cold storage, with an initial focus on Nigerian produce-storage contexts.

## Components

- **Web dashboard:** Next.js and TypeScript UI for status, telemetry, energy, and risk explanations.
- **API:** FastAPI backend for health checks and future cold-room, telemetry, and risk endpoints.
- **Data layer:** PostgreSQL is the intended deployed database. Local development can begin with SQLite while persistence is implemented.
- **Telemetry simulator:** Deterministic synthetic data is planned so demos and tests can be repeated without physical devices.
- **Risk engine:** Planned explainable rules and baseline models for temperature excursions, energy availability, and estimated spoilage risk.

## Data and safety boundaries

The current UI contains illustrative values, not live sensor data. The initial release does not connect to physical sensors and cannot control refrigeration, batteries, inverters, or electrical circuits. All outputs are advisory and must not be used as a substitute for food-safety procedures or equipment protections.

## Planned flow

1. Simulated or explicitly integrated sensor readings enter the API.
2. Validation and persistence retain timestamps, units, and source information.
3. Rules compute transparent warning indicators.
4. The dashboard presents values, risk explanations, and data provenance.
5. Predictive models are evaluated against documented baselines before any claims are made.
