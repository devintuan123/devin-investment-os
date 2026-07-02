from __future__ import annotations

from datetime import datetime
from statistics import mean

import pandas as pd

from utils.binance_provider import get_public_price
from utils.cache import cache_market_regime
from utils.data_freshness import TW_REFERENCE_WARNING
from utils.fred_provider import get_latest_observation, get_recent_observations
from utils.market_data import FALLBACK_PRICES, get_batch_history, get_batch_prices, get_history, safe_fetch_with_fallback


MARKET_TICKERS = [
    "SPY",
    "QQQ",
    "^VIX",
    "DX-Y.NYB",
    "GC=F",
    "BTC-USD",
    "NVDA",
    "TSM",
    "PLTR",
    "GEV",
    "MRVL",
    "0050.TW",
    "2330.TW",
    "2454.TW",
    "2327.TW",
    "VWRA.L",
    "CNX1.L",
    "IEMA.L",
    "SGLD.L",
    "WHEA.L",
]

WARNINGS = [
    "yfinance data may be delayed or best-effort.",
    "FRED macro data may be daily or lagged.",
    "Verify broker quote before actual trading.",
]


@cache_market_regime
def calculate_market_regime() -> dict:
    assets = _asset_snapshots(MARKET_TICKERS)
    fred = _fred_snapshot()
    binance = _binance_snapshot()

    components = {
        "US Market": _average([_trend_score(assets["SPY"]), _trend_score(assets["QQQ"])]),
        "US Tech": _average([_trend_score(assets[ticker]) for ticker in ["NVDA", "TSM", "PLTR", "GEV", "MRVL"]]),
        "Taiwan": _average([_trend_score(assets[ticker]) for ticker in ["0050.TW", "2330.TW", "2454.TW", "2327.TW"]]),
        "Crypto": _crypto_score(assets["BTC-USD"], binance),
        "Gold": _gold_score(assets["GC=F"], assets["SPY"], assets["QQQ"]),
        "Macro": _macro_score(fred, assets["DX-Y.NYB"]),
        "Volatility": _volatility_score(assets["^VIX"]),
        "Liquidity": _liquidity_score(assets["DX-Y.NYB"], assets["^VIX"], fred),
        "Sentiment": _sentiment_score(assets["SPY"], assets["QQQ"], assets["^VIX"]),
        "Breadth": _breadth_score([assets[ticker] for ticker in ["SPY", "QQQ", "0050.TW", "VWRA.L"]]),
    }
    score = int(round(_average(list(components.values()))))
    regime = _regime(score, assets["^VIX"])
    action_label = _action_label(score, assets["^VIX"])
    warnings = list(WARNINGS)
    warnings.extend(_data_warnings(assets, fred, binance))
    confidence_score = max(35, 92 - (len([w for w in warnings if "fallback" in w.lower() or "missing" in w.lower()]) * 8))
    confidence_level = _confidence_label(confidence_score)

    return {
        "market_score": score,
        "score": score,
        "market_regime": regime,
        "regime": regime,
        "action_label": action_label,
        "today_action": action_label,
        "confidence_level": confidence_level,
        "confidence_score": confidence_score,
        "components": components,
        "warnings": warnings,
        "recommended_action": _recommended_action(score, regime, components),
        "what_changed": _what_changed(assets, fred, binance),
        "what_to_watch": _what_to_watch(assets, fred),
        "risk_warnings": _risk_warnings(assets, components),
        "provider_quality": _provider_quality(assets, fred, binance, confidence_score),
        "key_metrics": {
            "VIX": assets["^VIX"]["price"],
            "10Y Yield": fred.get("DGS10", {}).get("value"),
            "2Y Yield": fred.get("DGS2", {}).get("value"),
            "Fed Funds": fred.get("FEDFUNDS", {}).get("value"),
            "BTC": binance.get("BTCUSDT", {}).get("price") or assets["BTC-USD"]["price"],
            "Gold": assets["GC=F"]["price"],
        },
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def _asset_snapshot(ticker: str) -> dict:
    price_row = safe_fetch_with_fallback(ticker, FALLBACK_PRICES.get(ticker))
    history, warning = get_history(ticker, period="1y")
    close = history["Close"].dropna() if "Close" in history else pd.Series(dtype=float)
    latest = float(close.iloc[-1]) if not close.empty else float(price_row.get("price", 0.0))
    return {
        "ticker": ticker,
        "price": float(price_row.get("price", latest)),
        "history_price": latest,
        "ma20": _ma(close, 20),
        "ma60": _ma(close, 60),
        "ma120": _ma(close, 120),
        "return_20d": _return(close, 20),
        "return_60d": _return(close, 60),
        "drawdown_52w": _drawdown(close),
        "source": price_row.get("source", "unknown"),
        "fetch_timestamp": price_row.get("fetch_timestamp"),
        "quote_timestamp": price_row.get("quote_timestamp"),
        "provider_label": price_row.get("provider_label"),
        "freshness_status": price_row.get("freshness_status"),
        "confidence": price_row.get("confidence"),
        "provider_warning": price_row.get("provider_warning"),
        "warning": price_row.get("warning") or warning,
    }


def _asset_snapshots(tickers: list[str]) -> dict[str, dict]:
    prices = get_batch_prices(tickers)
    histories = get_batch_history(tickers, period="1y")
    return {ticker: _asset_snapshot_from_rows(ticker, prices.get(ticker), histories.get(ticker)) for ticker in tickers}


def _asset_snapshot_from_rows(ticker: str, price_row: dict | None, history_row: tuple[pd.DataFrame, str] | None) -> dict:
    price_row = price_row or safe_fetch_with_fallback(ticker, FALLBACK_PRICES.get(ticker))
    history, warning = history_row or get_history(ticker, period="1y")
    close = history["Close"].dropna() if "Close" in history else pd.Series(dtype=float)
    latest = float(close.iloc[-1]) if not close.empty else float(price_row.get("price", 0.0))
    return {
        "ticker": ticker,
        "price": float(price_row.get("price", latest)),
        "history_price": latest,
        "ma20": _ma(close, 20),
        "ma60": _ma(close, 60),
        "ma120": _ma(close, 120),
        "return_20d": _return(close, 20),
        "return_60d": _return(close, 60),
        "drawdown_52w": _drawdown(close),
        "source": price_row.get("source", "unknown"),
        "fetch_timestamp": price_row.get("fetch_timestamp"),
        "quote_timestamp": price_row.get("quote_timestamp"),
        "provider_label": price_row.get("provider_label"),
        "freshness_status": price_row.get("freshness_status"),
        "confidence": price_row.get("confidence"),
        "provider_warning": price_row.get("provider_warning"),
        "warning": price_row.get("warning") or warning,
    }


def _fred_snapshot() -> dict:
    series = {"DGS10": "10Y Treasury Yield", "DGS2": "2Y Treasury Yield", "FEDFUNDS": "Fed Funds", "CPIAUCSL": "CPI", "M2SL": "M2"}
    output = {}
    for series_id, label in series.items():
        try:
            latest = get_latest_observation(series_id)
            recent = get_recent_observations(series_id, limit=30)
            values = recent.get("observations", [])
            previous = values[-1]["value"] if len(values) > 1 else latest.get("value")
            output[series_id] = {
                "label": label,
                "connected": bool(latest.get("connected")),
                "date": latest.get("date"),
                "value": latest.get("value"),
                "change": (latest.get("value") - previous) if latest.get("value") is not None and previous is not None else 0.0,
            }
        except Exception as exc:
            output[series_id] = {"label": label, "connected": False, "value": None, "date": None, "change": 0.0, "warning": str(exc)}
    return output


def _binance_snapshot() -> dict:
    output = {}
    for symbol in ["BTCUSDT", "ETHUSDT"]:
        try:
            payload = get_public_price(symbol)
            output[symbol] = {"connected": True, "price": float(payload["price"]), "source": "Binance read-only"}
        except Exception as exc:
            output[symbol] = {"connected": False, "price": None, "source": "unavailable", "warning": str(exc)}
    return output


def _trend_score(asset: dict) -> int:
    price = asset["price"]
    score = 50
    if price > asset["ma20"]:
        score += 15
    else:
        score -= 10
    if price > asset["ma60"]:
        score += 15
    else:
        score -= 12
    if asset["return_20d"] > 0:
        score += 8
    if asset["drawdown_52w"] < -15:
        score -= 10
    return _bound(score)


def _volatility_score(vix: dict) -> int:
    value = vix["price"]
    if value < 18:
        return 82
    if value <= 25:
        return 55
    return 25


def _macro_score(fred: dict, dxy: dict) -> int:
    score = 62
    ten_year = fred.get("DGS10", {})
    two_year = fred.get("DGS2", {})
    if ten_year.get("change", 0) > 0.25:
        score -= 18
    if ten_year.get("value") and two_year.get("value") and ten_year["value"] < two_year["value"]:
        score -= 8
    if dxy["price"] > dxy["ma60"] and dxy["return_20d"] > 1:
        score -= 8
    if not ten_year.get("connected"):
        score -= 10
    return _bound(score)


def _liquidity_score(dxy: dict, vix: dict, fred: dict) -> int:
    score = 60
    if dxy["price"] > dxy["ma60"]:
        score -= 8
    if vix["price"] < 18:
        score += 12
    elif vix["price"] > 25:
        score -= 18
    if fred.get("DGS10", {}).get("change", 0) > 0.25:
        score -= 10
    return _bound(score)


def _sentiment_score(spy: dict, qqq: dict, vix: dict) -> int:
    score = _average([_trend_score(spy), _trend_score(qqq)])
    if vix["price"] < 18:
        score += 8
    elif vix["price"] > 25:
        score -= 15
    return _bound(score)


def _breadth_score(assets: list[dict]) -> int:
    if not assets:
        return 50
    above_ma = sum(1 for asset in assets if asset["price"] > asset["ma60"])
    positive_momentum = sum(1 for asset in assets if asset["return_20d"] > 0)
    return _bound(35 + above_ma / len(assets) * 35 + positive_momentum / len(assets) * 30)


def _crypto_score(btc: dict, binance: dict) -> int:
    score = _trend_score(btc)
    if binance.get("BTCUSDT", {}).get("connected"):
        score += 5
    if binance.get("ETHUSDT", {}).get("connected"):
        score += 3
    return _bound(score)


def _gold_score(gold: dict, spy: dict, qqq: dict) -> int:
    gold_trend = _trend_score(gold)
    equity_trend = _average([_trend_score(spy), _trend_score(qqq)])
    if gold_trend >= 70 and equity_trend < 50:
        return 35
    if gold_trend >= 60:
        return 58
    return 52


def _regime(score: int, vix: dict) -> str:
    if vix["price"] > 25 or score < 40:
        return "Risk-Off"
    if score >= 65 and vix["price"] < 22:
        return "Risk-On"
    return "Neutral"


def _action_label(score: int, vix: dict) -> str:
    if vix["price"] > 25 or score < 35:
        return "Reduce Risk"
    if score >= 78:
        return "Aggressive Buy Zone"
    if score >= 62:
        return "Gradual Buy Zone"
    if score >= 48:
        return "Hold / DCA Only"
    return "Watch / Wait"


def _recommended_action(score: int, regime: str, components: dict) -> str:
    if regime == "Risk-Off":
        return "Reduce weak exposure, protect cash, and wait for volatility confirmation before adding risk."
    if score >= 70:
        return "Hold core positions. Add only in planned layers on pullbacks. Avoid chasing extended names."
    if score >= 50:
        return "DCA core ETFs only. Keep watchlist orders patient and verify broker quotes before acting."
    return "Watch and wait. Keep cash available until breadth, volatility, and macro pressure improve."


def _what_changed(assets: dict, fred: dict, binance: dict) -> list[str]:
    changes = []
    spy = assets["SPY"]
    qqq = assets["QQQ"]
    vix = assets["^VIX"]["price"]
    changes.append(f"SPY is {'above' if spy['price'] > spy['ma20'] else 'below'} its 20D average.")
    changes.append(f"QQQ is {'above' if qqq['price'] > qqq['ma20'] else 'below'} its 20D average.")
    changes.append(f"VIX is {vix:.1f}, which is {'constructive' if vix < 18 else 'mixed' if vix <= 25 else 'risk-off'} for risk appetite.")
    ten_year = fred.get("DGS10", {})
    if ten_year.get("value") is not None:
        changes.append(f"10Y yield latest FRED reading is {ten_year['value']:.2f}%.")
    if binance.get("BTCUSDT", {}).get("connected"):
        changes.append("Binance BTCUSDT read-only price is available.")
    return changes


def _what_to_watch(assets: dict, fred: dict) -> list[str]:
    watch = ["SPY/QQQ 20D and 60D moving-average confirmation.", "VIX below 18 for clean risk-on confirmation."]
    if fred.get("DGS10", {}).get("change", 0) > 0.25:
        watch.append("10Y yield is rising quickly; watch macro pressure on growth stocks.")
    if assets["GC=F"]["price"] > assets["GC=F"]["ma20"] and assets["SPY"]["price"] < assets["SPY"]["ma20"]:
        watch.append("Gold strength versus weak equities may be a defensive warning.")
    watch.append("Broker quotes before any real trading decision.")
    return watch


def _risk_warnings(assets: dict, components: dict) -> list[str]:
    warnings = []
    if assets["^VIX"]["price"] > 25:
        warnings.append("VIX above 25: risk-off warning.")
    if components["US Tech"] > 75:
        warnings.append("AI / Tech strength is extended; avoid chasing vertical moves.")
    if components["Macro"] < 45:
        warnings.append("Macro pressure is elevated; size risk more conservatively.")
    if not warnings:
        warnings.append("No major risk-off trigger, but data remains decision-support only.")
    return warnings


def _provider_quality(assets: dict, fred: dict, binance: dict, confidence: int) -> list[dict]:
    yfinance_warnings = [asset["warning"] for asset in assets.values() if asset.get("warning")]
    return [
        {
            "Provider": "yfinance",
            "Latest successful fetch": "available" if not yfinance_warnings else "partial/fallback",
            "Freshness": "delayed / best-effort",
            "Confidence": max(45, confidence - len(yfinance_warnings) * 3),
            "Warning": "Some fallback data used." if yfinance_warnings else "Not guaranteed real-time.",
        },
        {
            "Provider": "Binance",
            "Latest successful fetch": "BTCUSDT connected" if binance.get("BTCUSDT", {}).get("connected") else "unavailable",
            "Freshness": "near real-time public endpoint",
            "Confidence": 85 if binance.get("BTCUSDT", {}).get("connected") else 45,
            "Warning": "Read-only crypto reference data.",
        },
        {
            "Provider": "FRED",
            "Latest successful fetch": fred.get("DGS10", {}).get("date") or "unavailable",
            "Freshness": "daily / lagged",
            "Confidence": 78 if fred.get("DGS10", {}).get("connected") else 45,
            "Warning": "Macro data may update with delay.",
        },
        {
            "Provider": "Telegram",
            "Latest successful fetch": "configured status only",
            "Freshness": "on send",
            "Confidence": 80,
            "Warning": "Outbound notifications only.",
        },
    ]


def _data_warnings(assets: dict, fred: dict, binance: dict) -> list[str]:
    warnings = []
    fallback_assets = [ticker for ticker, asset in assets.items() if asset.get("source") == "fallback" or asset.get("warning")]
    tw_uncertain = [
        ticker
        for ticker, asset in assets.items()
        if ticker.endswith(".TW") and asset.get("freshness_status") in {"Delayed / uncertain", "Reference / delayed", "Fallback"}
    ]
    if fallback_assets:
        warnings.append(f"Fallback or partial yfinance data used for: {', '.join(fallback_assets[:6])}.")
    if tw_uncertain:
        warnings.append(TW_REFERENCE_WARNING)
    if not fred.get("DGS10", {}).get("connected"):
        warnings.append("FRED 10Y yield is missing.")
    if not binance.get("BTCUSDT", {}).get("connected"):
        warnings.append("Binance BTCUSDT unavailable; BTC uses yfinance/fallback.")
    return warnings


def _ma(close: pd.Series, window: int) -> float:
    if close.empty:
        return 0.0
    return float(close.tail(min(window, len(close))).mean())


def _return(close: pd.Series, periods: int) -> float:
    if len(close) <= periods:
        return 0.0
    previous = float(close.iloc[-periods - 1])
    latest = float(close.iloc[-1])
    return ((latest - previous) / previous * 100) if previous else 0.0


def _drawdown(close: pd.Series) -> float:
    if close.empty:
        return 0.0
    latest = float(close.iloc[-1])
    high = float(close.max())
    return ((latest - high) / high * 100) if high else 0.0


def _average(values: list[int | float]) -> int:
    clean = [float(value) for value in values if value is not None]
    return int(round(mean(clean))) if clean else 50


def _bound(score: int | float) -> int:
    return int(max(0, min(100, round(score))))


def _confidence_label(score: int) -> str:
    if score >= 75:
        return "High"
    if score >= 55:
        return "Medium"
    return "Low"
