from __future__ import annotations

import os
from datetime import datetime, timezone

import pandas as pd
import requests

from utils.cache import cache_fred_data
from utils.config import load_app_env


load_app_env()

FRED_BASE_URL = "https://api.stlouisfed.org/fred"

MACRO_SERIES = {
    "DGS10": "10Y Treasury yield",
    "DGS2": "2Y Treasury yield",
    "FEDFUNDS": "Fed funds rate",
    "CPIAUCSL": "CPI",
    "M2SL": "M2 money supply",
    "BAMLH0A0HYM2": "High yield spread",
    "T10Y2Y": "10Y-2Y yield spread",
    "DFF": "Effective federal funds rate",
}


def fred_configured() -> bool:
    return bool(os.getenv("FRED_API_KEY"))


@cache_fred_data
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


@cache_fred_data
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


def get_macro_series_snapshot() -> pd.DataFrame:
    rows = []
    configured = fred_configured()
    for series_id, label in MACRO_SERIES.items():
        row = {
            "series_id": series_id,
            "label": label,
            "latest_date": None,
            "latest_value": None,
            "previous_date": None,
            "previous_value": None,
            "change": None,
            "provider": "FRED",
            "freshness_status": "Unavailable",
            "confidence": 20 if not configured else 35,
            "error": "" if configured else "FRED_API_KEY missing",
            "fallback_used": False,
            "rows_fetched": 0,
            "missing": True,
            "stale": True,
            "connected": False,
            "configured": configured,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            recent = get_recent_observations(series_id, limit=90)
            observations = recent.get("observations", [])
            row["rows_fetched"] = len(observations)
            row["connected"] = bool(recent.get("connected"))
            row["error"] = recent.get("message") or row["error"]
            if observations:
                latest = observations[0]
                previous = observations[1] if len(observations) > 1 else latest
                row.update(
                    {
                        "latest_date": latest.get("date"),
                        "latest_value": latest.get("value"),
                        "previous_date": previous.get("date"),
                        "previous_value": previous.get("value"),
                        "change": _safe_change(latest.get("value"), previous.get("value")),
                        "freshness_status": "Daily / lagged",
                        "confidence": 78,
                        "missing": False,
                        "stale": False,
                    }
                )
            elif configured and not row["error"]:
                row["error"] = "No observations returned"
        except Exception as exc:
            row["error"] = str(exc)
        rows.append(row)
    return pd.DataFrame(rows)


def _safe_change(latest: object, previous: object) -> float | None:
    try:
        if latest is None or previous is None:
            return None
        return float(latest) - float(previous)
    except (TypeError, ValueError):
        return None
