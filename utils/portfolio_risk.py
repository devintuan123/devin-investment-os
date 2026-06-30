from __future__ import annotations

import pandas as pd


HIGH_BETA = {"PLTR", "MRVL", "GEV", "NVDA"}
HEDGES = {"SGLD.L", "GC=F", "BTC-USD", "IB1T"}
CORE = {"VWRA.L", "0050.TW", "CNX1.L", "IEMA.L", "00878.TW"}


def portfolio_summary(df: pd.DataFrame) -> dict:
    data = df.copy()
    data["market_value"] = pd.to_numeric(data.get("market_value"), errors="coerce").fillna(0)
    total = float(data["market_value"].sum())
    return {
        "total_value": total,
        "allocation_by_asset_type": _allocation(data, "asset_type", total),
        "allocation_by_currency": _allocation(data, "currency", total),
        "high_beta_exposure": _exposure(data, HIGH_BETA, total),
        "hedge_allocation": _exposure(data, HEDGES, total),
        "core_allocation": _exposure(data, CORE, total),
        "single_name_concentration": _single_name(data, total),
        "us_individual_stock_exposure": _us_stock_exposure(data, total),
        "cash_level": _cash_level(data, total),
        "risk_score": _risk_score(data, total),
        "suggestions": portfolio_suggestions(data, total),
    }


def holding_action(row: pd.Series) -> str:
    ticker = str(row.get("ticker", ""))
    if ticker == "VWRA.L":
        return "Core hold / accumulate on pullback"
    if ticker == "CNX1.L":
        return "Hold, do not overweight tech"
    if ticker == "IEMA.L":
        return "Hold / add near buy zone"
    if ticker == "MRVL":
        return "Hold, avoid averaging down"
    if ticker == "PLTR":
        return "Reduced risk, no averaging down"
    if ticker == "SGLD.L":
        return "Hedge hold"
    if ticker == "WHEA.L":
        return "Diversifier hold"
    if ticker == "GEV":
        return "Buy only in pullback zone"
    if ticker == "0050.TW":
        return "Core Taiwan buyback below plan"
    if ticker == "2330.TW":
        return "Core Taiwan semis"
    if ticker == "2454.TW":
        return "Watch support zone"
    if ticker == "2327.TW":
        return "Trim if extended, buyback lower"
    return "Hold"


def portfolio_suggestions(df: pd.DataFrame, total: float) -> list[str]:
    summary = []
    high_beta = _exposure(df, HIGH_BETA, total)
    concentration = _single_name(df, total)
    hedge = _exposure(df, HEDGES, total)
    if high_beta > 25:
        summary.append("High-beta exposure is elevated; avoid new satellite risk.")
    if concentration > 30:
        summary.append("Single-name concentration is high; rebalance toward core ETFs.")
    if hedge < 5:
        summary.append("Hedge allocation is light; review gold/BTC hedge plan.")
    if not summary:
        summary.append("Portfolio risk is balanced enough for planned pullback buying.")
    return summary


def _allocation(df: pd.DataFrame, column: str, total: float) -> dict:
    if not total or column not in df:
        return {}
    values = df.groupby(column, dropna=False)["market_value"].sum()
    return {str(key): round(float(value) / total * 100, 2) for key, value in values.items()}


def _exposure(df: pd.DataFrame, tickers: set[str], total: float) -> float:
    if not total:
        return 0.0
    value = df[df["ticker"].astype(str).isin(tickers)]["market_value"].sum()
    return round(float(value) / total * 100, 2)


def _single_name(df: pd.DataFrame, total: float) -> float:
    if not total or df.empty:
        return 0.0
    return round(float(df["market_value"].max()) / total * 100, 2)


def _us_stock_exposure(df: pd.DataFrame, total: float) -> float:
    if not total:
        return 0.0
    mask = (df["currency"].astype(str) == "USD") & (df["asset_type"].astype(str).str.contains("Stock", case=False, na=False))
    return round(float(df[mask]["market_value"].sum()) / total * 100, 2)


def _cash_level(df: pd.DataFrame, total: float) -> float:
    if not total:
        return 0.0
    mask = df["asset_type"].astype(str).str.contains("Cash", case=False, na=False)
    return round(float(df[mask]["market_value"].sum()) / total * 100, 2)


def _risk_score(df: pd.DataFrame, total: float) -> int:
    high_beta = _exposure(df, HIGH_BETA, total)
    concentration = _single_name(df, total)
    us_stock = _us_stock_exposure(df, total)
    hedge = _exposure(df, HEDGES, total)
    score = 35 + high_beta * 0.8 + concentration * 0.6 + us_stock * 0.4 - hedge * 0.3
    return int(max(0, min(100, score)))
