from __future__ import annotations

import os

import requests

from utils.config import load_app_env


load_app_env()

FRED_BASE_URL = "https://api.stlouisfed.org/fred"


def fred_configured() -> bool:
    return bool(os.getenv("FRED_API_KEY"))


def get_latest_observation(series_id: str = "DGS10") -> dict:
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        return {
            "configured": False,
            "connected": False,
            "series_id": series_id,
            "message": "FRED_API_KEY missing",
        }

    response = requests.get(
        f"{FRED_BASE_URL}/series/observations",
        params={
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 1,
        },
        timeout=15,
    )
    response.raise_for_status()
    observations = response.json().get("observations", [])
    latest = observations[0] if observations else {}
    value = latest.get("value")
    return {
        "configured": True,
        "connected": bool(latest),
        "series_id": series_id,
        "date": latest.get("date"),
        "value": None if value in {None, "."} else float(value),
    }


def get_recent_observations(series_id: str = "DGS10", limit: int = 30) -> dict:
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        return {"configured": False, "connected": False, "series_id": series_id, "observations": []}

    response = requests.get(
        f"{FRED_BASE_URL}/series/observations",
        params={
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": limit,
        },
        timeout=15,
    )
    response.raise_for_status()
    rows = []
    for item in response.json().get("observations", []):
        value = item.get("value")
        if value in {None, "."}:
            continue
        rows.append({"date": item.get("date"), "value": float(value)})
    return {"configured": True, "connected": bool(rows), "series_id": series_id, "observations": rows}
