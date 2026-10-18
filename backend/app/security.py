import secrets

from fastapi import Header, HTTPException, status

from app.config import settings


def require_device_api_key(
    x_device_api_key: str | None = Header(default=None, alias="X-Device-API-Key"),
) -> None:
    """Protect sensor-ingestion endpoints; production fails closed without a key."""
    expected = settings.device_api_key
    if not expected:
        if settings.app_env.strip().lower() in {"production", "prod"}:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Device ingestion is not configured",
            )
        # Local development remains usable; configure DEVICE_API_KEY to test auth.
        return
    if x_device_api_key is None or not secrets.compare_digest(x_device_api_key, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid device API key",
            headers={"WWW-Authenticate": "API key"},
        )
