# HarvestGuard AI demo script

Target duration: 3–4 minutes.

## 1. Introduce the problem (30 seconds)

Explain that unreliable cold storage and power interruptions can increase spoilage risk for perishable produce. HarvestGuard AI is a prototype concept for making storage conditions and energy risk easier to observe.

## 2. Show the simulated dashboard (45 seconds)

Open the dashboard and point out the temperature, battery reserve, solar generation, and advisory risk indicators.

Say clearly: **these values are simulated**. The current build has no connected sensor and does not control refrigeration or electrical equipment.

## 3. Register a storage site (45 seconds)

Use the registration form to create a demo site, for example:
- Name: Ado Produce Store
- Location: Ado-Ekiti, Ekiti State
- Commodity: Tomatoes
- Configured temperature metadata: 2–8 °C

Explain that these temperature bounds are demo metadata, not certified storage guidance for a particular crop or cultivar.

## 4. Persist demo readings (45 seconds)

Select the new site and choose **Save 24 demo readings**. Explain that the simulator sends a batch to the API, which stores the readings against that site.

Show the stored-reading history and explain the temperature, humidity, battery, solar power, and electrical load fields.

## 5. Explain the risk result (45 seconds)

Point out the stored-reading risk score and its factors. Explain that the score comes from transparent prototype thresholds. It is not a trained ML prediction and has not been validated for operational food-safety decisions.

## 6. Close with the roadmap (30 seconds)

Describe the next milestones:
- Verify automated tests and frontend production build.
- Deploy the API with a persistent managed PostgreSQL database and deploy the frontend.
- Add authenticated sensor ingestion and real hardware telemetry.
- Collect representative labelled data and evaluate ML against the rule-based baseline.
- Review commodity-specific thresholds with cold-chain and food-safety experts.

## Demo safety note

Do not imply that the prototype has detected a real cold-room failure, prevented spoilage, connected to live sensors, or autonomously controlled equipment. Use a demo environment and never submit real operational data to the unauthenticated ingestion endpoints.
