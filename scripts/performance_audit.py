from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from scripts.send_daily_report import build_daily_report
from utils.alert_engine import evaluate_alerts
from utils.binance_provider import get_btcusdt_price
from utils.buy_zone_engine import DEFAULT_BUY_ZONE_TICKERS, score_buy_zones
from utils.fred_provider import get_latest_observation
from utils.market_data import get_history, get_prices
from utils.market_regime import calculate_market_regime
from utils.portfolio_engine import calculate_position_values, load_portfolio
from utils.sector_heat_engine import calculate_theme_heat_score, load_theme_universe
from utils.snapshot_store import create_snapshot
from utils.watchlist_scoring import DEFAULT_WATCHLIST, score_watchlist


REPORT_MD = ROOT_DIR / "reports" / "performance_audit.md"
REPORT_JSON = ROOT_DIR / "reports" / "performance_audit.json"


def main() -> int:
    ROOT_DIR.joinpath("reports").mkdir(exist_ok=True)
    rows = []
    rows.append(_measure("Market regime calculation", calculate_market_regime))
    rows.append(_measure("Watchlist scoring", lambda: score_watchlist(DEFAULT_WATCHLIST), len(DEFAULT_WATCHLIST)))
    rows.append(_measure("Portfolio valuation", lambda: calculate_position_values(load_portfolio()), len(load_portfolio())))
    rows.append(_measure("Buy zone scoring", lambda: score_buy_zones(DEFAULT_BUY_ZONE_TICKERS), len(DEFAULT_BUY_ZONE_TICKERS)))
    rows.append(_measure("Sector heat calculation", calculate_theme_heat_score, len(load_theme_universe())))
    rows.append(_measure("Daily Playbook generation", lambda: build_daily_report("zh")))
    rows.append(_measure("Snapshot creation", create_snapshot))
    rows.append(_measure("Alert evaluation", evaluate_alerts))
    rows.append(_measure("yfinance batch fetch", lambda: get_prices(DEFAULT_WATCHLIST[:8]), 8))
    rows.append(_measure("yfinance history fetch", lambda: [get_history(ticker, period="6mo") for ticker in DEFAULT_WATCHLIST[:5]], 5))
    rows.append(_measure("Binance fetch", get_btcusdt_price, 1))
    rows.append(_measure("FRED fetch", lambda: get_latest_observation("DGS10"), 1))
    _write_reports(rows)
    print(REPORT_MD)
    print(REPORT_JSON)
    return 0


def _measure(name: str, func, ticker_count: int | None = None) -> dict:
    started = time.perf_counter()
    ok = True
    warning = ""
    try:
        result = func()
        size = len(result) if hasattr(result, "__len__") and not isinstance(result, (str, bytes, dict)) else None
    except Exception as exc:
        ok = False
        size = None
        warning = str(exc)
    duration = time.perf_counter() - started
    return {
        "module": name,
        "duration_seconds": round(duration, 3),
        "ticker_count": ticker_count,
        "cache": "not measurable in CLI audit",
        "status": "pass" if ok else "fail",
        "result_size": size,
        "warning": warning,
        "bottleneck": _bottleneck(name, duration),
        "recommendation": _recommendation(name, duration),
    }


def _bottleneck(name: str, duration: float) -> str:
    if duration >= 20:
        return "critical"
    if duration >= 8:
        return "high"
    if duration >= 3:
        return "medium"
    return "low"


def _recommendation(name: str, duration: float) -> str:
    if duration < 3:
        return "Acceptable"
    if "Sector" in name:
        return "Use quick scan, batch yfinance history, and cache results"
    if "yfinance" in name or "Watchlist" in name or "Buy zone" in name:
        return "Batch yfinance calls and reuse cached history"
    if "Market regime" in name:
        return "Cache regime and batch core market tickers"
    return "Cache expensive market data and avoid recomputation on Home"


def _write_reports(rows: list[dict]) -> None:
    payload = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "rows": rows}
    REPORT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "# Devin Investment OS Performance Audit",
        "",
        f"Generated UTC: {payload['generated_at']}",
        "",
        "| Function / Module | Duration (s) | Tickers | Cache | Bottleneck | Recommendation |",
        "|---|---:|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['module']} | {row['duration_seconds']} | {row.get('ticker_count') or ''} | {row['cache']} | {row['bottleneck']} | {row['recommendation']} |"
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
