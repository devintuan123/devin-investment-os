from __future__ import annotations

import pandas as pd


def to_float(value: object) -> float:
    try:
        if pd.isna(value) or value == "":
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def watchlist_signal(row: pd.Series) -> str:
    price = to_float(row.get("current_price"))
    if not price:
        return "No price"
    if to_float(row.get("stop_level")) and price <= to_float(row.get("stop_level")):
        return "Risk Alert"
    if to_float(row.get("trim_zone")) and price >= to_float(row.get("trim_zone")):
        return "Trim"
    if to_float(row.get("buy_zone_low")) and to_float(row.get("buy_zone_high")) and to_float(row.get("buy_zone_low")) <= price <= to_float(row.get("buy_zone_high")):
        return "Buy Zone"
    return "Watch"


def distance_to_buy_zone(row: pd.Series) -> float:
    price = to_float(row.get("current_price"))
    low = to_float(row.get("buy_zone_low"))
    high = to_float(row.get("buy_zone_high"))
    if not price or not low or not high:
        return 0.0
    if low <= price <= high:
        return 0.0
    target = high if price > high else low
    return (price - target) / target * 100 if target else 0.0


def distance_to_trim_zone(row: pd.Series) -> float:
    price = to_float(row.get("current_price"))
    trim = to_float(row.get("trim_zone"))
    if not price or not trim:
        return 0.0
    return (trim - price) / price * 100


def no_chase_warning(ticker: str, return_5d: float = 0.0) -> str:
    if ticker in {"PLTR", "MRVL"}:
        return "Avoid blind averaging down; wait for trend repair."
    if return_5d > 8:
        return "Do not chase after a sharp spike."
    return ""


def trend_repair_signal(distance_ma_50d: float, distance_ma_200d: float) -> str:
    if distance_ma_50d > 0 and distance_ma_200d > 0:
        return "Trend repair"
    if distance_ma_50d > 0:
        return "Early repair"
    return "No repair"


def pullback_deployment_signal(drawdown_pct: float) -> str:
    drawdown = abs(min(drawdown_pct, 0))
    if drawdown >= 12:
        return "12-15% staged buying"
    if drawdown >= 8:
        return "8% pullback list"
    if drawdown >= 5:
        return "5% pullback list"
    return "Wait"
