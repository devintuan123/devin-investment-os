from __future__ import annotations

import math
import re
from typing import Any

import pandas as pd

from utils.i18n import (
    LANG_EN,
    LANG_ZH,
    t,
    translate_action_label,
    translate_regime,
    translate_risk_label,
    translate_warning,
)


PROVIDER_NAMES = {"yfinance", "Yahoo Finance", "Binance", "FRED", "Telegram", "TWSE", "TradingView"}
TICKER_PATTERN = re.compile(r"^[A-Z0-9^=.-]{1,20}(\.[A-Z]{1,4})?$")
PATH_OR_API_PATTERN = re.compile(r"^(https?://|/|[A-Za-z]:\\|[A-Z0-9_]+_API|[A-Z0-9_]+_KEY|[A-Z0-9_]+_TOKEN)")

COLUMN_KEYS = {
    "ticker": "ticker",
    "symbol": "symbol",
    "name": "name",
    "category": "category",
    "market": "market",
    "currency": "currency",
    "quantity": "quantity",
    "avg_cost": "avg_cost",
    "target_weight": "target_weight",
    "current_weight": "current_weight",
    "weight": "weight",
    "price": "price",
    "latest_price": "latest_price",
    "value": "portfolio_value",
    "position_value": "portfolio_value",
    "market_value": "market_value",
    "cost": "cost",
    "unrealized_pl": "unrealized_pl",
    "unrealized_pnl": "unrealized_pl",
    "pnl": "unrealized_pl",
    "drift": "drift",
    "drift_label": "drift",
    "action": "action",
    "action_label": "action_label",
    "action_suggestion": "suggested_action",
    "risk": "risk",
    "risk_label": "risk_label",
    "trend_score": "trend_score",
    "pullback_score": "pullback_score",
    "market_score": "market_score",
    "regime": "market_regime",
    "market_regime": "market_regime",
    "confidence": "confidence",
    "data_confidence": "data_confidence",
    "warning": "warning",
    "warnings": "warnings",
    "provider": "provider",
    "source": "provider",
    "freshness": "freshness",
    "freshness_status": "freshness_status",
    "fetch_time": "fetch_time",
    "quote_time": "quote_time",
    "last_updated": "latest_successful_fetch",
    "market_session": "market_session_status",
    "market_session_status": "market_session_status",
    "ma20": "ma20",
    "ma60": "ma60",
    "ma120": "ma120",
    "drawdown": "drawdown",
    "drawdown_52w": "drawdown_52w_pct",
    "drawdown_52w_pct": "drawdown_52w_pct",
    "drawdown_from_high": "drawdown_52w_pct",
    "buy_zone_1": "buy_zone_1",
    "buy_zone_2": "buy_zone_2",
    "buy_zone_3": "buy_zone_3",
    "zone_status": "zone_status",
    "current_zone_status": "zone_status",
    "trend_status": "trend_status",
    "note": "note",
    "account": "account",
    "cash": "cash",
    "total_value": "total_portfolio_value",
    "portfolio_value": "portfolio_value",
    "unrealized_pl_pct": "unrealized_pl",
    "high_52w": "fifty_two_week_high",
    "volatility_proxy": "volatility_proxy",
    "configured": "configured",
    "connected": "connected",
    "status": "status",
    "score": "score",
    "alerts": "latest_alerts",
    "received_at": "latest_successful_fetch",
    "timeframe": "timeframe",
    "return_5d": "return_5d",
    "return_1m": "return_1m",
    "distance_ma_50d": "distance_ma_50d",
}

COLUMN_LABELS = {
    LANG_EN: {
        "timeframe": "Timeframe",
        "return_5d": "5D Return",
        "return_1m": "1M Return",
        "distance_ma_50d": "Distance from 50D MA",
    },
    LANG_ZH: {
        "timeframe": "\u6642\u9593\u9031\u671f",
        "return_5d": "5 \u65e5\u5831\u916c",
        "return_1m": "1 \u500b\u6708\u5831\u916c",
        "distance_ma_50d": "\u8ddd 50 \u65e5\u5747\u7dda",
    },
}

VALUE_KEYS = {
    "Yes": "yes",
    "No": "no",
    "Connected": "connected",
    "Disconnected": "disconnected",
    "Configured": "configured",
    "Not configured": "not_configured",
    "Available": "available",
    "Missing": "missing",
    "Active": "active",
    "Disabled": "disabled",
    "Future": "future",
    "Future disabled": "future_disabled",
    "Error": "error",
    "No data": "no_data",
    "Loading": "loading",
    "High": "high",
    "Elevated": "elevated",
    "Medium": "moderate",
    "Moderate": "moderate",
    "Balanced": "balanced",
    "Low": "balanced",
    "Fresh": "available",
    "Stale": "delayed_verify_broker_quote",
    "Unknown": "no_data",
    "Delayed / uncertain": "delayed_verify_broker_quote",
    "Delayed / best-effort": "yf_warning",
    "Delayed / verify broker quote": "delayed_verify_broker_quote",
    "Daily / lagged": "fred_warning",
    "Reference / delayed": "delayed_verify_broker_quote",
    "Reference-only": "tw_reference_warning",
    "Fallback": "yf_warning",
    "Near real-time": "available",
    "Stock": "stock",
    "ETF": "etf",
    "Crypto": "crypto",
    "Gold": "gold",
    "Cash": "cash",
    "Taiwan": "taiwan",
    "US": "us",
    "UCITS": "ucits",
    "On target": "balanced",
    "Underweight": "add",
    "Overweight": "trim_later",
    "Healthy": "healthy_trend_hold",
    "Constructive": "gradual_buy_zone",
    "Mixed": "watch_wait",
    "Broken": "broken_trend_avoid",
    "Near MA20": "potential_layer_1",
    "Normal pullback": "potential_layer_2",
    "Deep pullback": "deep_pullback_watch",
    "Below long-term trend": "broken_trend_avoid_short",
    "Extended": "extended_do_not_chase_short",
    "DCA reference": "dca_only",
}


def translate_column_name(column: Any, lang: str) -> Any:
    if lang == LANG_EN:
        return str(column).replace("_", " ").title() if str(column) not in COLUMN_KEYS else t(COLUMN_KEYS[str(column)])
    column_text = str(column)
    key = COLUMN_KEYS.get(column_text)
    if key:
        return t(key)
    return COLUMN_LABELS.get(lang, {}).get(column_text, column)


def translate_cell_value(value: Any, lang: str) -> Any:
    if lang == LANG_EN or _should_preserve(value):
        return value

    text = str(value).strip()
    if not text:
        return value
    if _looks_like_ticker_or_provider(text):
        return value
    if PATH_OR_API_PATTERN.match(text):
        return value
    if "Verify broker quote" in text or "yfinance data" in text or "FRED macro data" in text or "Taiwan stock data" in text:
        return translate_warning(text)

    translated = translate_action_label(text)
    if translated != text:
        return translated
    translated = translate_risk_label(text)
    if translated != text:
        return translated
    translated = translate_regime(text)
    if translated != text:
        return translated
    key = VALUE_KEYS.get(text)
    if key:
        return t(key)
    return value


def translate_dataframe(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    translated = df.copy()
    for column in translated.columns:
        if pd.api.types.is_object_dtype(translated[column]) or pd.api.types.is_string_dtype(translated[column]):
            translated[column] = translated[column].map(lambda value: translate_cell_value(value, lang))
    translated = translated.rename(columns={column: translate_column_name(column, lang) for column in translated.columns})
    return translated


def format_percent(value: Any, decimals: int = 1) -> str:
    try:
        return f"{float(value):,.{decimals}f}%"
    except (TypeError, ValueError):
        return ""


def format_currency(value: Any, currency: str = "") -> str:
    try:
        prefix = f"{currency} " if currency else ""
        return f"{prefix}{float(value):,.2f}"
    except (TypeError, ValueError):
        return ""


def translated_column_config(df: pd.DataFrame, lang: str) -> dict[str, Any]:
    return {column: translate_column_name(column, lang) for column in df.columns}


def _should_preserve(value: Any) -> bool:
    if value is None or isinstance(value, (int, float, bool)):
        return True
    try:
        if isinstance(value, float) and math.isnan(value):
            return True
    except TypeError:
        pass
    return pd.isna(value) if not isinstance(value, (list, tuple, dict, set)) else False


def _looks_like_ticker_or_provider(text: str) -> bool:
    if text in PROVIDER_NAMES:
        return True
    if text.upper().endswith(("USDT", "USD", ".TW", ".T", ".L")):
        return True
    return bool(TICKER_PATTERN.match(text)) and any(char.isupper() for char in text)
