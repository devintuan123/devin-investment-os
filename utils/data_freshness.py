from __future__ import annotations

from datetime import datetime, timezone


TW_DELAY_WARNING = "TW quote may be delayed. Verify with broker quote before trading."
TW_REFERENCE_WARNING = "Taiwan stock data is reference-only. Do not use for execution."


def classify_quote_freshness(
    ticker: str,
    provider: str,
    quote_timestamp: object,
    fetch_timestamp: object,
    market_open: bool,
) -> dict:
    ticker = str(ticker or "").upper()
    provider = str(provider or "")
    quote_dt = _parse_datetime(quote_timestamp)
    fetch_dt = _parse_datetime(fetch_timestamp) or datetime.now(timezone.utc)

    if ticker.endswith(".TW") and provider.lower() in {"yfinance", "yahoo finance / yfinance", "yahoo finance"}:
        age_minutes = _age_minutes(quote_dt, fetch_dt)
        if market_open and (quote_dt is None or age_minutes is None or age_minutes > 5):
            return {
                "provider_label": "Yahoo Finance / yfinance",
                "real_time": False,
                "freshness_status": "Delayed / uncertain",
                "confidence": 60,
                "warning": TW_DELAY_WARNING,
            }
        return {
            "provider_label": "Yahoo Finance / yfinance",
            "real_time": False,
            "freshness_status": "Reference / delayed",
            "confidence": 60,
            "warning": TW_REFERENCE_WARNING,
        }

    if provider.lower() == "binance":
        return {
            "provider_label": "Binance",
            "real_time": True,
            "freshness_status": "Near real-time",
            "confidence": 90,
            "warning": "Read-only crypto reference data.",
        }

    if provider.lower() == "fred":
        return {
            "provider_label": "FRED",
            "real_time": False,
            "freshness_status": "Daily / lagged",
            "confidence": 85,
            "warning": "FRED macro data is daily or lagged.",
        }

    return {
        "provider_label": provider or "Unknown",
        "real_time": False,
        "freshness_status": "Best-effort",
        "confidence": 70,
        "warning": "Verify broker quote before trading.",
    }


def detect_stale_quote(
    ticker: str,
    price: object,
    previous_price: object,
    quote_timestamp: object,
    fetch_timestamp: object,
) -> dict:
    unchanged = _to_float(price) is not None and _to_float(price) == _to_float(previous_price)
    return {
        "ticker": ticker,
        "stale": bool(unchanged),
        "warning": "No change after refresh; source may be delayed." if unchanged else "",
        "quote_timestamp": quote_timestamp,
        "fetch_timestamp": fetch_timestamp,
    }


def format_freshness_warning(freshness: dict, stale: dict | None = None) -> str:
    warnings = [freshness.get("warning", "")]
    if stale and stale.get("warning"):
        warnings.append(stale["warning"])
    return " ".join([warning for warning in warnings if warning]).strip()


def _parse_datetime(value: object) -> datetime | None:
    if value in {None, ""}:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _age_minutes(quote_dt: datetime | None, fetch_dt: datetime) -> float | None:
    if quote_dt is None:
        return None
    return max(0.0, (fetch_dt.astimezone(timezone.utc) - quote_dt.astimezone(timezone.utc)).total_seconds() / 60)


def _to_float(value: object) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
