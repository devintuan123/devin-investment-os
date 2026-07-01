from __future__ import annotations

import pandas as pd

from utils.market_data import FALLBACK_PRICES, get_history, normalize_ticker, safe_fetch_with_fallback
from utils.market_regime import calculate_market_regime


DEFAULT_BUY_ZONE_TICKERS = [
    "VWRA.L",
    "0050.TW",
    "CNX1.L",
    "PLTR",
    "SGLD.L",
    "BTC-USD",
    "IEMA.L",
    "WHEA.L",
    "GEV",
    "MRVL",
    "2330.TW",
    "2454.TW",
    "2327.TW",
]


def score_buy_zones(tickers: list[str] | None = None) -> list[dict]:
    regime = calculate_market_regime()
    return [score_buy_zone(ticker, regime["market_regime"]) for ticker in tickers or DEFAULT_BUY_ZONE_TICKERS]


def score_buy_zone(ticker: str, market_regime: str = "Neutral") -> dict:
    ticker = normalize_ticker(ticker)
    quote = safe_fetch_with_fallback(ticker, FALLBACK_PRICES.get(ticker))
    history, warning = get_history(ticker, period="1y")
    close = history["Close"].dropna() if "Close" in history else pd.Series(dtype=float)
    latest = float(quote.get("price") or (close.iloc[-1] if not close.empty else 0.0))
    ma20 = _ma(close, 20)
    ma60 = _ma(close, 60)
    ma120 = _ma(close, 120)
    high_52w = float(close.max()) if not close.empty else latest
    drawdown = ((latest - high_52w) / high_52w * 100) if high_52w else 0.0
    volatility = _volatility(close)
    trend_status = _trend_status(latest, ma20, ma60, ma120)
    zone1 = min(ma20, high_52w * 0.95) if ma20 else latest * 0.95
    zone2 = min(ma60, high_52w * 0.90) if ma60 else latest * 0.90
    zone3 = min(ma120, high_52w * 0.82) if ma120 else latest * 0.82
    zone_status, action_label = _zone_action(ticker, latest, ma20, ma60, ma120, drawdown, trend_status, market_regime)
    return {
        "ticker": ticker,
        "latest_price": latest,
        "ma20": ma20,
        "ma60": ma60,
        "ma120": ma120,
        "high_52w": high_52w,
        "drawdown_52w_pct": drawdown,
        "volatility_proxy": volatility,
        "trend_status": trend_status,
        "buy_zone_1": zone1,
        "buy_zone_2": zone2,
        "buy_zone_3": zone3,
        "current_zone_status": zone_status,
        "action_label": action_label,
        "provider": quote.get("provider_label") or quote.get("source"),
        "freshness_status": quote.get("freshness_status"),
        "confidence": quote.get("confidence"),
        "warning": quote.get("provider_warning") or quote.get("warning") or warning,
    }


def _trend_status(latest: float, ma20: float, ma60: float, ma120: float) -> str:
    if latest > ma20 > ma60 > ma120:
        return "Healthy"
    if latest > ma60 and latest > ma120:
        return "Constructive"
    if latest < ma120:
        return "Broken"
    return "Mixed"


def _zone_action(
    ticker: str,
    latest: float,
    ma20: float,
    ma60: float,
    ma120: float,
    drawdown: float,
    trend_status: str,
    market_regime: str,
) -> tuple[str, str]:
    is_etf = ticker.endswith(".L") or ticker.endswith(".TW") or ticker in {"VWRA.L", "CNX1.L", "IEMA.L", "SGLD.L", "WHEA.L"}
    if trend_status == "Broken" or (ma120 and latest < ma120):
        return "Below long-term trend", "Broken trend, avoid"
    if drawdown > -3 and latest > ma20 * 1.08 and not is_etf:
        return "Extended", "Extended, do not chase"
    if trend_status in {"Healthy", "Constructive"} and ma20 and abs((latest - ma20) / ma20 * 100) <= 3:
        return "Near MA20", "Potential Layer 1"
    if trend_status in {"Healthy", "Constructive", "Mixed"} and -15 <= drawdown <= -8:
        return "Normal pullback", "Potential Layer 2"
    if -25 <= drawdown <= -15 and market_regime != "Risk-Off":
        return "Deep pullback", "Deep Pullback Watch"
    if is_etf and trend_status != "Broken":
        return "DCA reference", "Hold"
    return "Watch", "Hold"


def _ma(close: pd.Series, window: int) -> float:
    if close.empty:
        return 0.0
    return float(close.tail(min(window, len(close))).mean())


def _volatility(close: pd.Series) -> float:
    if len(close) < 20:
        return 0.0
    returns = close.pct_change().dropna()
    return float(returns.tail(20).std() * 100)
