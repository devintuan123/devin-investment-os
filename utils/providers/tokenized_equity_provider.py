from __future__ import annotations

import os
from functools import lru_cache

import requests
from dotenv import load_dotenv

from utils.market_data import get_latest_price


load_dotenv()

REFERENCE_WARNING = "Verify with broker quote before trading."
SOURCE_NAME = "Binance Tokenized/Synthetic Reference"
TRACKED_UNDERLYINGS = ["AAPL", "MSFT", "NVDA", "TSLA", "META", "GOOGL", "AMZN"]


def discover_supported_tokenized_equities() -> list[dict]:
    exchange_info = _exchange_info()
    symbols = {item.get("symbol") for item in exchange_info.get("symbols", []) if item.get("status") == "TRADING"}
    supported = []
    for underlying in TRACKED_UNDERLYINGS:
        candidate = f"{underlying}USDT"
        supported.append(
            {
                "underlying": underlying,
                "symbol": candidate,
                "available": candidate in symbols,
                "source": SOURCE_NAME,
                "warning": REFERENCE_WARNING,
            }
        )
    return supported


def get_tokenized_equity_price(symbol: str) -> dict:
    normalized = _normalize_symbol(symbol)
    available_symbols = {item["symbol"] for item in discover_supported_tokenized_equities() if item["available"]}
    if normalized not in available_symbols:
        return _unavailable(normalized)

    try:
        response = requests.get(
            f"{_base_url()}/api/v3/ticker/price",
            params={"symbol": normalized},
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
        return {
            "symbol": normalized,
            "available": True,
            "price": float(payload["price"]),
            "source": SOURCE_NAME,
            "freshness": "fresh",
            "reliability_cap": 70,
            "confidence": 70,
            "warning": REFERENCE_WARNING,
        }
    except Exception as exc:
        result = _unavailable(normalized)
        result["warning"] = f"{REFERENCE_WARNING} Provider error: {exc}"
        return result


def get_tokenized_equity_basis(symbol: str, official_price: float | None = None) -> dict:
    reference = get_tokenized_equity_price(symbol)
    if not reference["available"]:
        return {**reference, "basis_pct": None}

    underlying = reference["symbol"].removesuffix("USDT")
    official = official_price if official_price is not None else _official_price(underlying)
    if not official:
        return {
            **reference,
            "official_price": None,
            "basis_pct": None,
            "confidence": min(reference["confidence"], 60),
            "warning": f"{REFERENCE_WARNING} No official comparison price available.",
        }

    basis = (reference["price"] - official) / official * 100
    confidence = reference["confidence"]
    warning = REFERENCE_WARNING
    if abs(basis) > 1:
        confidence = min(confidence, 50)
    if abs(basis) > 3:
        warning = f"{REFERENCE_WARNING} Strong warning: tokenized basis exceeds 3%."

    return {
        **reference,
        "official_price": official,
        "basis_pct": basis,
        "confidence": confidence,
        "warning": warning,
    }


def tokenized_equity_health_check() -> dict:
    supported = discover_supported_tokenized_equities()
    available = [item["symbol"] for item in supported if item["available"]]
    return {
        "provider": "Tokenized Equity",
        "source": SOURCE_NAME,
        "available_count": len(available),
        "supported_symbols": available,
        "freshness": "fresh if public ticker is available",
        "reliability_cap": 70,
        "warning": REFERENCE_WARNING,
    }


@lru_cache(maxsize=1)
def _exchange_info() -> dict:
    try:
        response = requests.get(f"{_base_url()}/api/v3/exchangeInfo", timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {"symbols": []}


def _base_url() -> str:
    return os.getenv("BINANCE_BASE_URL", "https://api.binance.com").rstrip("/")


def _normalize_symbol(symbol: str) -> str:
    normalized = str(symbol or "").strip().upper().replace("-", "")
    if not normalized.endswith("USDT"):
        normalized = f"{normalized}USDT"
    return normalized


def _official_price(underlying: str) -> float | None:
    try:
        return float(get_latest_price(underlying))
    except Exception:
        return None


def _unavailable(symbol: str) -> dict:
    return {
        "symbol": symbol,
        "available": False,
        "price": None,
        "source": SOURCE_NAME,
        "freshness": "unavailable",
        "reliability_cap": 0,
        "confidence": 0,
        "warning": REFERENCE_WARNING,
    }
