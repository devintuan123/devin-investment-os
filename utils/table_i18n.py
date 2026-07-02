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
    translate_term,
    translate_warning,
)


PROVIDER_NAMES = {"yfinance", "Yahoo Finance", "Binance", "FRED", "Telegram", "TWSE", "TradingView"}
TICKER_PATTERN = re.compile(r"^[A-Z0-9^=.-]{1,20}(\.[A-Z]{1,4})?$")
PATH_OR_API_PATTERN = re.compile(r"^(https?://|/|[A-Za-z]:\\|[A-Z0-9_]+_API|[A-Z0-9_]+_KEY|[A-Z0-9_]+_TOKEN)")

COLUMN_KEYS = {
    "ticker": "ticker",
    "symbol": "symbol",
    "series_id": "symbol",
    "label": "name",
    "name": "name",
    "category": "category",
    "asset_category": "category",
    "strategy_category": "strategy_category",
    "market": "market",
    "currency": "currency",
    "quantity": "quantity",
    "avg_cost": "avg_cost",
    "target_weight": "target_weight",
    "strategy_target_weight": "strategy_target_weight",
    "current_weight": "current_weight",
    "strategy_drift": "strategy_drift",
    "strategy_max_weight": "strategy_max_weight",
    "weight": "weight",
    "price": "price",
    "latest_value": "value",
    "previous_value": "value",
    "change": "what_changed",
    "current_price": "current_price",
    "latest_price": "latest_price",
    "latest_date": "latest_successful_fetch",
    "previous_date": "latest_successful_fetch",
    "value": "value",
    "position_value": "position_value",
    "market_value": "market_value",
    "cost": "cost",
    "unrealized_pl": "unrealized_pl",
    "unrealized_pnl": "unrealized_pl",
    "pnl": "unrealized_pl",
    "drift": "drift",
    "target_drift": "target_drift",
    "current_drift": "current_drift",
    "allocation_drift": "allocation_drift",
    "drift_abs": "drift_abs",
    "drift_pct": "drift_pct",
    "drift_label": "drift",
    "action": "action",
    "action_label": "action_label",
    "strategy_action": "strategy_action",
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
    "error": "error",
    "strategy_warning": "strategy_warning",
    "warnings": "warnings",
    "provider": "provider",
    "source": "provider",
    "freshness": "freshness",
    "freshness_status": "freshness_status",
    "fallback_used": "fallback_used",
    "missing": "missing",
    "stale": "freshness_status",
    "rows_fetched": "rows",
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
    "buy_zone_low": "buy_zone_low",
    "buy_zone_high": "buy_zone_high",
    "trim_zone": "trim_zone",
    "stop_level": "stop_level",
    "priority": "priority",
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
    "Connected": "connected",
    "status": "status",
    "Status": "status",
    "score": "score",
    "alerts": "latest_alerts",
    "active_alerts": "active_alerts",
    "alert_count": "active_alerts",
    "cash_deployment_mode": "cash_deployment_mode",
    "latest_snapshot": "latest_snapshot",
    "snapshot_status": "snapshot_status",
    "received_at": "latest_successful_fetch",
    "timeframe": "timeframe",
    "return_5d": "return_5d",
    "return_1m": "return_1m",
    "distance_ma_50d": "distance_ma_50d",
    "theme": "theme",
    "theme_zh": "theme",
    "sector": "sector",
    "heat_score": "heat_score",
    "rotation_score": "rotation_score",
    "rotation_label": "rotation_signal",
    "heat_label": "theme_heat",
    "return_1d": "one_day_return",
    "return_20d": "twenty_day_return",
    "relative_strength": "relative_strength",
    "breadth": "breadth",
    "action_type": "action",
    "timestamp": "latest_successful_fetch",
    "fees": "fees",
    "realized_pl": "realized_pl",
    "No.": "no_column",
    "No": "no_column",
    "no": "no_column",
    "index": "no_column",
    "Index": "no_column",
    "#": "no_column",
}

COLUMN_LABELS = {
    LANG_EN: {
        "timeframe": "Timeframe",
        "return_5d": "5D Return",
        "return_1m": "1M Return",
        "distance_ma_50d": "Distance from 50D MA",
    },
    LANG_ZH: {
        "timeframe": "時間週期",
        "return_5d": "5 日報酬",
        "return_1m": "1 個月報酬",
        "distance_ma_50d": "距 50 日均線",
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
    "US Market": "us_market",
    "US Tech": "us_tech",
    "Taiwan Market": "taiwan_market",
    "Macro": "macro",
    "Volatility": "volatility",
    "US": "us",
    "UCITS": "ucits",
    "On target": "balanced",
    "Underweight": "add",
    "Overweight": "trim_later",
    "Healthy": "healthy_trend_hold",
    "Constructive": "gradual_buy_zone",
    "Mixed": "watch_wait",
    "Sentiment": "sentiment",
    "Breadth": "breadth",
    "Broken": "broken_trend_avoid",
    "Near MA20": "potential_layer_1",
    "Normal pullback": "potential_layer_2",
    "Deep pullback": "deep_pullback_watch",
    "Below long-term trend": "broken_trend_avoid_short",
    "Extended": "extended_do_not_chase_short",
    "DCA reference": "dca_only",
    "Add gradually": "gradual_buy_zone",
    "Watch only": "watch",
    "Need target weight": "target_weight",
    "No target": "not_configured",
    "Heating Up": "heating_up",
    "Hot / Extended": "hot_extended",
    "Cooling": "cooling",
    "Rotation In": "rotation_in",
    "Rotation Out": "rotation_out",
    "Watchlist Candidate": "watchlist_candidate",
    "Avoid chasing": "avoid_chasing",
    "Potential buy zone": "potential_buy_zone_short",
    "Consider gradual allocation": "consider_gradual_allocation",
    "DCA only": "dca_only",
    "Reduce risk": "reduce_risk",
    "Core ETF": "etf",
    "Satellite Stock": "stock",
    "Taiwan Stock": "taiwan",
    "Liquidity": "liquidity",
    "Defensive": "defensive",
    "Defensive / Hedge": "defensive",
    "Signals are mixed; confirmation matters.": "signals_mixed_confirmation",
    "Trend and momentum are supportive.": "trend_momentum_supportive",
    "Risk controls should take priority.": "risk_controls_priority",
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
    translated = translate_term(text)
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
    translated.columns = _dedupe_columns([str(column) for column in translated.columns])
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
    labels = _dedupe_columns([str(translate_column_name(column, lang)) for column in df.columns])
    return {column: label for column, label in zip(df.columns, labels)}


def _dedupe_columns(columns: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    output = []
    for column in columns:
        counts[column] = counts.get(column, 0) + 1
        output.append(column if counts[column] == 1 else f"{column}_{counts[column]}")
    return output


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
