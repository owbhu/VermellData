from __future__ import annotations

import httpx
import logging
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

from .settings import settings

BASE_URL = "https://api.purpleair.com/v1"
log = logging.getLogger(__name__)


class PurpleAirError(RuntimeError):
    """Raised when API returns an unexpected payload."""


@retry(
    wait=wait_exponential(multiplier=1, min=2, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(httpx.HTTPStatusError),
)
def get_history(sensor_id: int, minutes: int = 5) -> dict:
    """
    Fetch `minutes` worth of history for one sensor.

    Returns the raw JSON dict the API sends back.
    """
    url = f"{BASE_URL}/sensors/{sensor_id}/history"
    params = {
        "minutes": minutes,
        "fields": "pm2.5_atm,humidity,temperature,pressure",
    }
    headers = {"X-API-Key": settings.purpleair_key}

    with httpx.Client(timeout=10) as client:
        resp = client.get(url, params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    if "data" not in data or "fields" not in data:
        raise PurpleAirError("Malformed history payload")
    
    return data 

