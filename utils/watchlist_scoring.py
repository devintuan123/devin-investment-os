from __future__ import annotations

import pandas as pd

from utils.market_data import FALLBACK_PRICES, get_history, normalize_ticker, safe_fetch_with_fallback


DEFAULT_WATCHLIST = [
    "VWRA.L",
    "CNX1.L",
    "IEMA.L",
    "SGLD.L",
    "WHEA.L",
    "PLTR",
    "GEV",
    "MRVL",
    "NVDA",
    "TSM",
    "0050.TW",
    "2330.TW",
    "2454.TW",
    "2327.TW",
    "BTC-USD",
]


def score_watchlist(tickers: list[str] | None = None) -> list[dict]:
    rows = []
    for ticker in tickers or DEFAULT_WATCHLIST:
        rows.append(score_ticker(ticker))
    return rows


def score_ticker(ticker: str) -> dict:
    ticker = normalize_ticker(ticker)
    price_row = safe_fetch_with_fallback(ticker, FALLBACK_PRICES.get(ticker))
    history, warning = get_history(ticker, period="1y")
    close = history["Close"].dropna() if "Close" in history else pd.Series(dtype=float)
    latest = float(price_row.get("price") or (close.iloc[-1] if not close.empty else 0.0))
    ma20 = _ma(close, 20)
    ma60 = _ma(close, 60)
    ma120 = _ma(close, 120)
    distance_ma20 = _distance(latest, ma20)
    distance_ma60 = _distance(latest, ma60)
    drawdown = _drawdown(close)
    trend_score = _trend_score(latest, ma20, ma60, ma120)
    pullback_score = _pullback_score(distance_ma20, distance_ma60, drawdown, trend_score)
    risk_label = _risk_label(trend_score, drawdown, latest, ma60)
    action_label = _action_label(trend_score, pullback_score, drawdown, latest, ma60)
    return {
        "ticker": ticker,
        "latest_price": latest,
        "ma20": ma20,
        "ma60": ma60,
        "ma120": ma120,
        "distance_ma20_pct": distance_ma20,
        "distance_ma60_pct": distance_ma60,
        "drawdown_52w_pct": drawdown,
        "trend_score": trend_score,
        "pullback_score": pullback_score,
        "risk_label": risk_label,
        "action_label": action_label,
        "source": price_row.get("source", "unknown"),
        "provider_label": price_row.get("provider_label"),
        "fetch_timestamp": price_row.get("fetch_timestamp"),
        "quote_timestamp": price_row.get("quote_timestamp"),
        "freshness_status": price_row.get("freshness_status"),
        "confidence": price_row.get("confidence"),
        "provider_warning": price_row.get("provider_warning"),
        "warning": price_row.get("warning") or warning,
    }


def _trend_score(latest: float, ma20: float, ma60: float, ma120: float) -> int:
    score = 50
    if latest > ma20:
        score += 15
    else:
        score -= 10
    if latest > ma60:
        score += 20
    else:
        score -= 15
    if latest > ma120:
        score += 10
    else:
        score -= 8
    return int(max(0, min(100, score)))


def _pullback_score(distance_ma20: float, distance_ma60: float, drawdown: float, trend_score: int) -> int:
    score = 45
    if -8 <= distance_ma20 <= 1:
        score += 22
    if -12 <= distance_ma60 <= 3:
        score += 18
    if -20 <= drawdown <= -5:
        score += 12
    if trend_score < 40:
        score -= 20
    if distance_ma20 > 12:
        score -= 25
    return int(max(0, min(100, score)))


def _risk_label(trend_score: int, drawdown: float, latest: float, ma60: float) -> str:
    if latest < ma60 and trend_score < 40:
        return "High"
    if drawdown < -20:
        return "Elevated"
    if trend_score >= 70:
        return "Moderate"
    return "Balanced"


def _action_label(trend_score: int, pullback_score: int, drawdown: float, latest: float, ma60: float) -> str:
    if latest < ma60 and trend_score < 40:
        return "Broken trend / Avoid"
    if trend_score >= 72 and pullback_score < 45:
        return "Extended / Do not chase"
    if trend_score >= 62 and pullback_score >= 70:
        return "Potential buy zone - verify quote"
    if trend_score >= 58 and -18 <= drawdown <= -3:
        return "Pullback watch"
    if trend_score >= 58:
        return "Healthy trend / Hold"
    return "Pullback watch"


def _ma(close: pd.Series, window: int) -> float:
    if close.empty:
        return 0.0
    return float(close.tail(min(window, len(close))).mean())


def _distance(latest: float, average: float) -> float:
    return ((latest - average) / average * 100) if average else 0.0


def _drawdown(close: pd.Series) -> float:
    if close.empty:
        return 0.0
    latest = float(close.iloc[-1])
    high = float(close.max())
    return ((latest - high) / high * 100) if high else 0.0
