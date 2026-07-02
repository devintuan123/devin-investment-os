from __future__ import annotations

import os

import requests
from dotenv import load_dotenv

from utils.cache import cache_binance_price


load_dotenv()


@cache_binance_price
def get_public_price(symbol: str) -> dict:
    base_url = os.getenv("BINANCE_BASE_URL", "https://api.binance.com").rstrip("/")
    response = requests.get(f"{base_url}/api/v3/ticker/price", params={"symbol": symbol}, timeout=15)
    response.raise_for_status()
    return response.json()


def get_btcusdt_price() -> dict:
    payload = get_public_price("BTCUSDT")
    return {
        "ticker": "BTC-USD",
        "source": "binance",
        "price": float(payload["price"]),
        "warning": "",
    }


def binance_configured() -> bool:
    return bool(os.getenv("BINANCE_API_KEY") and os.getenv("BINANCE_API_SECRET"))


def account_snapshot_placeholder() -> dict:
    return {
        "enabled": bool(os.getenv("BINANCE_API_KEY") and os.getenv("BINANCE_API_SECRET")),
        "mode": "read-only placeholder",
        "message": "Private Binance account reads are not active yet. Trading endpoints are not implemented.",
    }


def place_order(*args, **kwargs) -> None:
    raise NotImplementedError("Trading is not implemented in this app.")


def withdraw(*args, **kwargs) -> None:
    raise NotImplementedError("Withdrawals are not implemented in this app.")


def futures_request(*args, **kwargs) -> None:
    raise NotImplementedError("Futures are not implemented in this app.")
