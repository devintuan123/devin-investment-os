from __future__ import annotations

import pandas as pd

from utils.market_data import safe_fetch_with_fallback


INDICATOR_GROUPS = {
    "Liquidity": ["DX-Y.NYB", "^VIX"],
    "Sentiment": ["^VIX", "QQQ", "SPY"],
    "Breadth": ["SPY", "QQQ", "IWM", "DIA"],
    "AI / Tech": ["NVDA", "TSM", "GEV", "PLTR", "MRVL"],
    "Defensive / Hedge": ["GC=F", "BTC-USD", "SGLD.L"],
    "Taiwan Market": ["0050.TW", "2330.TW", "2454.TW", "2327.TW"],
    "BTC / Gold": ["BTC-USD", "GC=F", "SGLD.L"],
}


def market_indicators() -> dict:
    return {group: score_indicator_group(tickers) for group, tickers in INDICATOR_GROUPS.items()}


def score_indicator_group(tickers: list[str]) -> dict:
    rows = [safe_fetch_with_fallback(ticker) for ticker in tickers]
    df = pd.DataFrame(rows)
    if df.empty:
        return {"score": 50, "status": "Neutral", "indicators": [], "explanation": "No indicator data.", "what_changed": "No change."}

    trend_points = (df["distance_ma_50d"] > 0).sum() * 12
    momentum = df["return_1m"].mean()
    drawdown_penalty = abs(min(df["drawdown_52w"].mean(), 0)) * 0.8
    score = int(max(0, min(100, 45 + trend_points + momentum - drawdown_penalty)))
    return {
        "score": score,
        "status": _status(score),
        "indicators": tickers,
        "explanation": _explain(score),
        "what_changed": _changed(df),
        "data": rows,
    }


def simple_breadth_proxy(tickers: list[str]) -> float:
    rows = [safe_fetch_with_fallback(ticker) for ticker in tickers]
    if not rows:
        return 0.0
    above = [row["distance_ma_50d"] > 0 for row in rows]
    return sum(above) / len(above) * 100


def _status(score: int) -> str:
    if score >= 70:
        return "Constructive"
    if score >= 45:
        return "Mixed"
    return "Defensive"


def _explain(score: int) -> str:
    if score >= 70:
        return "Trend and momentum are supportive."
    if score >= 45:
        return "Signals are mixed; confirmation matters."
    return "Risk controls should take priority."


def _changed(df: pd.DataFrame) -> str:
    strongest = df.sort_values("return_5d", ascending=False).iloc[0]
    weakest = df.sort_values("return_5d", ascending=True).iloc[0]
    return f"{strongest['ticker']} led 5D momentum; {weakest['ticker']} lagged."
