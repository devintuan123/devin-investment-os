from __future__ import annotations

import hashlib
import hmac
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlencode

import requests

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.config import load_app_env, safety_status
from utils.fred_provider import get_latest_observation
from utils.telegram import send_telegram_message


def _status(label: str, ok: bool, detail: str = "") -> None:
    suffix = f" - {detail}" if detail else ""
    print(f"{label}: {'connected' if ok else 'failed'}{suffix}")


def _binance_base_url() -> str:
    return os.getenv("BINANCE_BASE_URL", "https://api.binance.com").rstrip("/")


def _binance_server_time() -> int:
    response = requests.get(f"{_binance_base_url()}/api/v3/time", timeout=15)
    response.raise_for_status()
    return int(response.json()["serverTime"])


def test_binance_public() -> tuple[bool, bool]:
    base_url = _binance_base_url()
    _binance_server_time()
    _status("Binance server time", True)

    price = requests.get(f"{base_url}/api/v3/ticker/price", params={"symbol": "BTCUSDT"}, timeout=15)
    price.raise_for_status()
    btc_price = float(price.json()["price"])
    _status("Binance BTCUSDT price", True, f"price received ({btc_price:,.2f})")
    return True, True


def test_binance_account_snapshot() -> bool:
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        _status("Binance read-only account snapshot", False, "not configured")
        return False

    query = urlencode({"timestamp": _binance_server_time(), "recvWindow": 5000})
    signature = hmac.new(api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
    response = requests.get(
        f"{_binance_base_url()}/api/v3/account?{query}&signature={signature}",
        headers={"X-MBX-APIKEY": api_key},
        timeout=15,
    )
    if not response.ok:
        try:
            payload = response.json()
            detail = f"HTTP {response.status_code} code {payload.get('code')} {payload.get('msg')}"
        except ValueError:
            detail = f"HTTP {response.status_code}"
        _status("Binance read-only account snapshot", False, detail)
        return False
    balances = response.json().get("balances", [])
    non_zero = sum(
        1
        for balance in balances
        if float(balance.get("free", 0) or 0) > 0 or float(balance.get("locked", 0) or 0) > 0
    )
    _status("Binance read-only account snapshot", True, f"{non_zero} non-zero assets")
    return True


def test_fred() -> bool:
    latest = get_latest_observation("DGS10")
    ok = bool(latest.get("connected"))
    detail = ""
    if ok:
        detail = f"{latest['series_id']} {latest['date']} value received"
    elif not latest.get("configured"):
        detail = "not configured"
    _status("FRED latest 10Y yield", ok, detail)
    return ok


def test_telegram() -> bool:
    ok = send_telegram_message("Devin Investment OS: API connection test successful.")
    _status("Telegram test message", ok)
    return ok


def main() -> int:
    load_app_env()
    safety = safety_status()
    all_safe = all(
        safety[key]
        for key in [
            "trading_disabled",
            "withdrawals_disabled",
            "futures_disabled",
            "margin_disabled",
            "auto_order_disabled",
        ]
    )
    print(f"Safety flags: {'all false' if all_safe else 'review required'}")

    results = []
    try:
        results.extend(test_binance_public())
    except Exception as exc:
        _status("Binance public endpoints", False, type(exc).__name__)
        results.extend([False, False])

    try:
        results.append(test_binance_account_snapshot())
    except Exception as exc:
        _status("Binance read-only account snapshot", False, type(exc).__name__)
        results.append(False)

    try:
        results.append(test_fred())
    except Exception as exc:
        _status("FRED latest 10Y yield", False, type(exc).__name__)
        results.append(False)

    try:
        results.append(test_telegram())
    except Exception as exc:
        _status("Telegram test message", False, type(exc).__name__)
        results.append(False)

    return 0 if all(results) and all_safe else 1


if __name__ == "__main__":
    raise SystemExit(main())
