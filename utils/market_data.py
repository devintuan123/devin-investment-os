from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

import pandas as pd
import yfinance as yf

from utils.binance_provider import get_btcusdt_price
from utils.cache import cache_yfinance_history, cache_yfinance_prices
from utils.data_freshness import classify_quote_freshness, format_freshness_warning
from utils.tw_market_time import is_tw_market_open


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


def normalize_ticker(ticker: object) -> str:
    return str(ticker or "").strip().upper()


def safe_fetch_with_fallback(ticker: str, fallback: float | None = None) -> dict:
    ticker = normalize_ticker(ticker)
    batch = get_batch_prices([ticker])
    if ticker in batch:
        return batch[ticker]
    if ticker == "BTCUSDT" and "BTC-USD" in batch:
        return batch["BTC-USD"]
    return _fallback_quote(ticker, fallback, "No batch quote returned")


def _fetch_single_quote(ticker: str, fallback: float | None = None) -> dict:
    ticker = normalize_ticker(ticker)
    fetch_timestamp = datetime.now(timezone.utc).isoformat()
    fallback_price = fallback if fallback is not None else FALLBACK_PRICES.get(ticker, 0.0)
    if ticker in {"BTC-USD", "BTCUSDT"}:
        try:
            btc = get_btcusdt_price()
            freshness = classify_quote_freshness("BTC-USD", "binance", fetch_timestamp, fetch_timestamp, False)
            return {
                "ticker": "BTC-USD",
                "price": btc["price"],
                "previous_close": btc["price"],
                "change_pct": 0.0,
                "return_1d": 0.0,
                "return_5d": 0.0,
                "return_1m": 0.0,
                "return_3m": 0.0,
                "ma_20d": btc["price"],
                "ma_50d": btc["price"],
                "ma_200d": btc["price"],
                "drawdown_52w": 0.0,
                "distance_ma_20d": 0.0,
                "distance_ma_50d": 0.0,
                "distance_ma_200d": 0.0,
                "source": "binance",
                "fetch_timestamp": fetch_timestamp,
                "quote_timestamp": fetch_timestamp,
                "provider_label": freshness["provider_label"],
                "real_time": freshness["real_time"],
                "freshness_status": freshness["freshness_status"],
                "confidence": freshness["confidence"],
                "provider_warning": freshness["warning"],
                "warning": "",
            }
        except Exception:
            pass
    try:
        history, history_warning = get_history(ticker, period="1y")
        close = history["Close"].dropna()
        if close.empty:
            raise ValueError("No close prices returned")
        latest = float(close.iloc[-1])
        previous = float(close.iloc[-2]) if len(close) > 1 else latest
        quote_timestamp = _timestamp_to_iso(close.index[-1])
        provider = "Yahoo Finance / yfinance" if ticker.endswith(".TW") else "yfinance"
        freshness = classify_quote_freshness(ticker, "yfinance", quote_timestamp, fetch_timestamp, is_tw_market_open())
        provider_warning = freshness["warning"] if ticker.endswith(".TW") else "yfinance data may be delayed or best-effort."
        change_pct = ((latest - previous) / previous * 100) if previous else 0.0
        return {
            "ticker": ticker,
            "price": latest,
            "previous_close": previous,
            "change_pct": change_pct,
            "return_1d": _return(close, 1),
            "return_5d": _return(close, 5),
            "return_1m": _return(close, 21),
            "return_3m": _return(close, 63),
            "ma_20d": _moving_average(close, 20),
            "ma_50d": _moving_average(close, 50),
            "ma_200d": _moving_average(close, 200),
            "drawdown_52w": _drawdown(close),
            "distance_ma_20d": _distance_from_ma(latest, close, 20),
            "distance_ma_50d": _distance_from_ma(latest, close, 50),
            "distance_ma_200d": _distance_from_ma(latest, close, 200),
            "fetch_timestamp": fetch_timestamp,
            "quote_timestamp": quote_timestamp,
            "provider_label": freshness["provider_label"] if ticker.endswith(".TW") else "yfinance",
            "real_time": freshness["real_time"] if ticker.endswith(".TW") else False,
            "freshness_status": freshness["freshness_status"] if ticker.endswith(".TW") else "Delayed / best-effort",
            "confidence": freshness["confidence"] if ticker.endswith(".TW") else 75,
            "provider_warning": provider_warning,
            "warning": history_warning,
            "source": "yfinance",
        }
    except Exception as exc:
        return _fallback_quote(ticker, fallback_price, str(exc))


def get_latest_price(ticker: str) -> float:
    return safe_fetch_with_fallback(ticker)["price"]


def get_price_change(ticker: str) -> float:
    return safe_fetch_with_fallback(ticker)["change_pct"]


def get_prices(tickers: Iterable[str]) -> pd.DataFrame:
    return pd.DataFrame(get_batch_prices(list(tickers)).values())


@cache_yfinance_prices
def get_batch_prices(tickers: Iterable[str]) -> dict[str, dict]:
    normalized = _normalize_tickers(tickers)
    output: dict[str, dict] = {}
    for ticker in normalized:
        if ticker in {"BTC-USD", "BTCUSDT"}:
            output["BTC-USD"] = _fetch_single_quote("BTC-USD", FALLBACK_PRICES.get("BTC-USD"))
    yfinance_tickers = [ticker for ticker in normalized if ticker not in {"BTC-USD", "BTCUSDT"}]
    histories = get_batch_history(yfinance_tickers, period="1y") if yfinance_tickers else {}
    for ticker in yfinance_tickers:
        history, warning = histories.get(ticker, (pd.DataFrame(), "No history returned"))
        output[ticker] = _quote_from_history(ticker, history, warning)
    return output


@cache_yfinance_history
def get_batch_history(tickers: Iterable[str], period: str = "6mo") -> dict[str, tuple[pd.DataFrame, str]]:
    normalized = _normalize_tickers(tickers)
    if not normalized:
        return {}
    try:
        raw = yf.download(
            tickers=" ".join(normalized),
            period=period,
            group_by="ticker",
            threads=True,
            progress=False,
            auto_adjust=False,
        )
    except Exception as exc:
        return {ticker: _fallback_history(ticker, exc) for ticker in normalized}
    output: dict[str, tuple[pd.DataFrame, str]] = {}
    for ticker in normalized:
        try:
            if len(normalized) == 1:
                frame = raw.copy()
            elif isinstance(raw.columns, pd.MultiIndex) and ticker in raw.columns.get_level_values(0):
                frame = raw[ticker].copy()
            else:
                frame = pd.DataFrame()
            if frame.empty or "Close" not in frame or frame["Close"].dropna().empty:
                raise ValueError("No history returned")
            output[ticker] = (frame.dropna(how="all"), "")
        except Exception as exc:
            output[ticker] = _fallback_history(ticker, exc)
    return output


def get_history(ticker: str, period: str = "6mo") -> tuple[pd.DataFrame, str]:
    ticker = normalize_ticker(ticker)
    batch = get_batch_history([ticker], period=period)
    if ticker in batch:
        return batch[ticker]
    return _fallback_history(ticker, "No batch history returned")


def _download_history_uncached(ticker: str, period: str = "6mo") -> tuple[pd.DataFrame, str]:
    try:
        history = yf.Ticker(ticker).history(period=period)
        if history.empty:
            raise ValueError("No history returned")
        return history, ""
    except Exception as exc:
        return _fallback_history(ticker, exc)


def _quote_from_history(ticker: str, history: pd.DataFrame, warning: str = "") -> dict:
    ticker = normalize_ticker(ticker)
    fallback = FALLBACK_PRICES.get(ticker, 0.0)
    fetch_timestamp = datetime.now(timezone.utc).isoformat()
    close = history["Close"].dropna() if "Close" in history else pd.Series(dtype=float)
    if close.empty:
        return _fallback_quote(ticker, fallback, warning or "No close prices returned")
    latest = float(close.iloc[-1])
    previous = float(close.iloc[-2]) if len(close) > 1 else latest
    quote_timestamp = _timestamp_to_iso(close.index[-1])
    freshness = classify_quote_freshness(ticker, "yfinance", quote_timestamp, fetch_timestamp, is_tw_market_open())
    provider_warning = freshness["warning"] if ticker.endswith(".TW") else "yfinance data may be delayed or best-effort."
    change_pct = ((latest - previous) / previous * 100) if previous else 0.0
    return {
        "ticker": ticker,
        "price": latest,
        "previous_close": previous,
        "change_pct": change_pct,
        "return_1d": _return(close, 1),
        "return_5d": _return(close, 5),
        "return_1m": _return(close, 21),
        "return_3m": _return(close, 63),
        "ma_20d": _moving_average(close, 20),
        "ma_50d": _moving_average(close, 50),
        "ma_200d": _moving_average(close, 200),
        "drawdown_52w": _drawdown(close),
        "distance_ma_20d": _distance_from_ma(latest, close, 20),
        "distance_ma_50d": _distance_from_ma(latest, close, 50),
        "distance_ma_200d": _distance_from_ma(latest, close, 200),
        "fetch_timestamp": fetch_timestamp,
        "quote_timestamp": quote_timestamp,
        "provider_label": freshness["provider_label"] if ticker.endswith(".TW") else "yfinance",
        "real_time": freshness["real_time"] if ticker.endswith(".TW") else False,
        "freshness_status": freshness["freshness_status"] if ticker.endswith(".TW") else "Delayed / best-effort",
        "confidence": freshness["confidence"] if ticker.endswith(".TW") else 75,
        "provider_warning": provider_warning,
        "warning": warning,
        "source": "yfinance" if not warning else "fallback" if "fallback" in warning.lower() else "yfinance",
    }


def _fallback_quote(ticker: str, fallback: float | None = None, warning_detail: str = "") -> dict:
    ticker = normalize_ticker(ticker)
    fetch_timestamp = datetime.now(timezone.utc).isoformat()
    fallback_price = fallback if fallback is not None else FALLBACK_PRICES.get(ticker, 0.0)
    freshness = classify_quote_freshness(ticker, "yfinance", None, fetch_timestamp, is_tw_market_open())
    warning = f"Using fallback for {ticker}: {warning_detail}"
    return {
        "ticker": ticker,
        "price": float(fallback_price),
        "previous_close": float(fallback_price),
        "change_pct": 0.0,
        "return_1d": 0.0,
        "return_5d": 0.0,
        "return_1m": 0.0,
        "return_3m": 0.0,
        "ma_20d": float(fallback_price),
        "ma_50d": float(fallback_price),
        "ma_200d": float(fallback_price),
        "drawdown_52w": 0.0,
        "distance_ma_20d": 0.0,
        "distance_ma_50d": 0.0,
        "distance_ma_200d": 0.0,
        "fetch_timestamp": fetch_timestamp,
        "quote_timestamp": None,
        "provider_label": freshness["provider_label"],
        "real_time": False,
        "freshness_status": "Fallback",
        "confidence": min(40, freshness["confidence"]),
        "provider_warning": format_freshness_warning(freshness),
        "warning": warning,
        "source": "fallback",
    }


def _fallback_history(ticker: str, exc: object) -> tuple[pd.DataFrame, str]:
    price = FALLBACK_PRICES.get(normalize_ticker(ticker), 100.0)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=90)
    history = pd.DataFrame({"Close": [price for _ in dates]}, index=dates)
    return history, f"Using fallback history for {ticker}: {exc}"


def _normalize_tickers(tickers: Iterable[str]) -> list[str]:
    seen = set()
    output = []
    for ticker in tickers:
        normalized = normalize_ticker(ticker)
        if normalized and normalized not in seen:
            seen.add(normalized)
            output.append(normalized)
    return output


def _return(close: pd.Series, periods: int) -> float:
    if len(close) <= periods:
        return 0.0
    previous = float(close.iloc[-periods - 1])
    latest = float(close.iloc[-1])
    return ((latest - previous) / previous * 100) if previous else 0.0


def _moving_average(close: pd.Series, window: int) -> float:
    if close.empty:
        return 0.0
    return float(close.tail(min(window, len(close))).mean())


def _drawdown(close: pd.Series) -> float:
    if close.empty:
        return 0.0
    latest = float(close.iloc[-1])
    high = float(close.max())
    return ((latest - high) / high * 100) if high else 0.0


def _distance_from_ma(latest: float, close: pd.Series, window: int) -> float:
    ma = _moving_average(close, window)
    return ((latest - ma) / ma * 100) if ma else 0.0


def _timestamp_to_iso(value: object) -> str | None:
    try:
        timestamp = pd.Timestamp(value)
        if timestamp.tzinfo is None:
            timestamp = timestamp.tz_localize(timezone.utc)
        return timestamp.isoformat()
    except Exception:
        return None
