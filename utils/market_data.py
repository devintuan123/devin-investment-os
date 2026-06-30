from __future__ import annotations

from typing import Iterable

import pandas as pd
import yfinance as yf


FALLBACK_PRICES = {
    "SPY": 550.0,
    "QQQ": 480.0,
    "DIA": 390.0,
    "IWM": 205.0,
    "^VIX": 16.0,
    "DX-Y.NYB": 105.0,
    "GC=F": 2350.0,
    "BTC-USD": 65000.0,
    "NVDA": 125.0,
    "TSM": 175.0,
    "GEV": 980.0,
    "PLTR": 118.0,
    "MRVL": 270.0,
    "VWRA.L": 185.0,
    "CNX1.L": 1255.0,
    "IEMA.L": 63.0,
    "SGLD.L": 438.0,
    "WHEA.L": 66.0,
    "0050.TW": 102.0,
    "00878.TW": 31.5,
    "2330.TW": 2250.0,
    "2454.TW": 3750.0,
    "2327.TW": 930.0,
}


def safe_fetch_with_fallback(ticker: str, fallback: float | None = None) -> dict:
    fallback_price = fallback if fallback is not None else FALLBACK_PRICES.get(ticker, 0.0)
    try:
        history = yf.Ticker(ticker).history(period="5d")
        close = history["Close"].dropna()
        if close.empty:
            raise ValueError("No close prices returned")
        latest = float(close.iloc[-1])
        previous = float(close.iloc[-2]) if len(close) > 1 else latest
        change_pct = ((latest - previous) / previous * 100) if previous else 0.0
        return {"ticker": ticker, "price": latest, "change_pct": change_pct, "warning": ""}
    except Exception as exc:
        return {
            "ticker": ticker,
            "price": float(fallback_price),
            "change_pct": 0.0,
            "warning": f"Using fallback for {ticker}: {exc}",
        }


def get_latest_price(ticker: str) -> float:
    return safe_fetch_with_fallback(ticker)["price"]


def get_price_change(ticker: str) -> float:
    return safe_fetch_with_fallback(ticker)["change_pct"]


def get_prices(tickers: Iterable[str]) -> pd.DataFrame:
    rows = [safe_fetch_with_fallback(str(ticker).strip()) for ticker in tickers if str(ticker).strip()]
    return pd.DataFrame(rows)


def get_history(ticker: str, period: str = "6mo") -> tuple[pd.DataFrame, str]:
    try:
        history = yf.Ticker(ticker).history(period=period)
        if history.empty:
            raise ValueError("No history returned")
        return history, ""
    except Exception as exc:
        price = FALLBACK_PRICES.get(ticker, 100.0)
        dates = pd.date_range(end=pd.Timestamp.today(), periods=90)
        history = pd.DataFrame({"Close": [price for _ in dates]}, index=dates)
        return history, f"Using fallback history for {ticker}: {exc}"
