from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="HarvestGuard AI API",
    description=(
        "Advisory monitoring and predictive-risk tools for solar-powered "
        "agricultural cold storage. Initial telemetry is simulated."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "harvestguard-ai-api"}


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"name": "HarvestGuard AI API", "docs": "/docs"}
