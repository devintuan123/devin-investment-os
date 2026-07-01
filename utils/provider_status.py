from __future__ import annotations

import os

from utils.config import is_configured, load_app_env


load_app_env()


def active_provider_rows() -> list[dict]:
    return [
        {"Provider": "yfinance", "Status": "available", "Mode": "market data fallback"},
        {
            "Provider": "Binance",
            "Status": "configured" if is_configured("BINANCE_API_KEY", "BINANCE_API_SECRET") else "missing",
            "Mode": "read-only crypto data",
        },
        {
            "Provider": "FRED",
            "Status": "configured" if is_configured("FRED_API_KEY") else "missing",
            "Mode": "read-only macro data",
        },
        {
            "Provider": "Telegram",
            "Status": "configured" if is_configured("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID") else "missing",
            "Mode": "outbound alerts only",
        },
    ]


def future_disabled_provider_rows() -> list[dict]:
    return [
        {"Provider": "IBKR", "Status": "future disabled", "Mode": "read-only planning"},
        {"Provider": "Yuanta", "Status": "future disabled", "Mode": "CSV/manual planning"},
        {"Provider": "OKX", "Status": "future disabled", "Mode": "not active"},
        {"Provider": "Bitget", "Status": "future disabled", "Mode": "not active"},
        {"Provider": "TradingView", "Status": "future disabled", "Mode": "webhook source when configured"},
    ]
