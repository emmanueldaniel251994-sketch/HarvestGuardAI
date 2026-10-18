from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.risk import assess_risk
from app.schemas import TelemetryResponse
from app.simulator import generate_readings\nfrom app.rooms import router as cold_rooms_router

app = FastAPI(
    title="HarvestGuard AI API",
    description=(
        "Advisory monitoring and predictive-risk tools for solar-powered "
        "agricultural cold storage. Initial telemetry is simulated."
    ),
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "harvestguard-ai-api"}


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"name": "HarvestGuard AI API", "docs": "/docs", "version": app.version}


@app.get(
    "/api/v1/demo/telemetry",
    response_model=TelemetryResponse,
    tags=["demo"],
    summary="Get simulated cold-room telemetry and advisory risk",
)
def demo_telemetry(
    samples: int = Query(default=24, ge=1, le=168),
    seed: int = Query(default=42, ge=0, le=2_147_483_647),
) -> TelemetryResponse:
    try:
        readings = generate_readings(samples=samples, seed=seed)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return TelemetryResponse(
        readings=readings,
        risk=assess_risk(readings),
    )
