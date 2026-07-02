from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import pandas as pd

from utils.binance_provider import binance_configured, get_public_price
from utils.fred_provider import fred_configured, get_latest_observation, get_recent_observations
from utils.market_data import get_batch_history, get_batch_prices

REPORT_MD = ROOT_DIR / "reports" / "data_source_audit.md"
REPORT_JSON = ROOT_DIR / "reports" / "data_source_audit.json"
LOCAL_FILES = [
    "data/portfolio.csv",
    "data/watchlist.csv",
    "data/theme_universe.csv",
    "data/strategy_rules.yaml",
    "data/alert_rules.yaml",
]
YFINANCE_TICKERS = ["SPY", "QQQ", "NVDA", "TSM", "0050.TW", "2330.TW", "GC=F", "^VIX", "BTC-USD"]
FRED_SERIES = ["DGS10", "DGS2", "FEDFUNDS", "CPIAUCSL", "M2SL"]


def main() -> int:
    REPORT_MD.parent.mkdir(exist_ok=True)
    audit = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "yfinance": audit_yfinance(),
        "binance": audit_binance(),
        "fred": audit_fred(),
        "local_files": audit_local_files(),
        "snapshots": audit_snapshots(),
        "failures": [],
    }
    audit["failures"] = collect_failures(audit)
    write_reports(audit)
    print(REPORT_MD.read_text(encoding="utf-8"))
    return 1 if audit["failures"] else 0


def audit_yfinance() -> dict:
    prices = get_batch_prices(YFINANCE_TICKERS)
    histories = get_batch_history(YFINANCE_TICKERS, period="6mo")
    rows = []
    for ticker in YFINANCE_TICKERS:
        quote = prices.get(ticker, {})
        history, warning = histories.get(ticker, (pd.DataFrame(), "missing history"))
        close = history["Close"].dropna() if not history.empty and "Close" in history else pd.Series(dtype=float)
        rows.append({
            "ticker": ticker,
            "latest_price": quote.get("price"),
            "quote_timestamp": quote.get("quote_timestamp"),
            "historical_rows": int(len(close)),
            "missing_columns": [col for col in ["Close"] if col not in history.columns],
            "all_nan": bool(close.empty),
            "source": quote.get("source"),
            "freshness_status": quote.get("freshness_status"),
            "confidence": quote.get("confidence"),
            "warning": quote.get("warning") or warning or quote.get("provider_warning"),
        })
    nonzero = [row["latest_price"] for row in rows if isinstance(row.get("latest_price"), (int, float)) and row.get("latest_price")]
    return {"provider": "yfinance", "tickers_requested": YFINANCE_TICKERS, "rows": rows, "all_same_values": len(set(round(float(v), 4) for v in nonzero)) <= 1 if len(nonzero) > 1 else False}


def audit_binance() -> dict:
    rows = []
    for symbol in ["BTCUSDT", "ETHUSDT"]:
        try:
            payload = get_public_price(symbol)
            rows.append({"symbol": symbol, "connected": True, "latest_price": float(payload.get("price", 0)), "timestamp": datetime.now(timezone.utc).isoformat(), "confidence": 85, "warning": "Read-only public endpoint."})
        except Exception as exc:
            rows.append({"symbol": symbol, "connected": False, "latest_price": None, "timestamp": None, "confidence": 40, "warning": str(exc)})
    return {"configured": binance_configured(), "rows": rows}


def audit_fred() -> dict:
    rows = []
    for series_id in FRED_SERIES:
        try:
            latest = get_latest_observation(series_id)
            recent = get_recent_observations(series_id, limit=2).get("observations", [])
            previous = recent[1]["value"] if len(recent) > 1 else None
            rows.append({"series_id": series_id, "connected": bool(latest.get("connected")), "latest_observation_date": latest.get("date"), "latest_value": latest.get("value"), "previous_value": previous, "confidence": 78 if latest.get("connected") else 40, "warning": "daily/lagged macro data" if latest.get("connected") else latest.get("message", "unavailable")})
        except Exception as exc:
            rows.append({"series_id": series_id, "connected": False, "latest_observation_date": None, "latest_value": None, "previous_value": None, "confidence": 40, "warning": str(exc)})
    return {"configured": fred_configured(), "rows": rows}


def audit_local_files() -> list[dict]:
    required = {
        "data/portfolio.csv": ["symbol", "quantity", "avg_cost", "target_weight"],
        "data/watchlist.csv": ["ticker"],
        "data/theme_universe.csv": ["theme", "market", "symbol"],
    }
    rows = []
    for rel in LOCAL_FILES:
        path = ROOT_DIR / rel
        row = {"file": rel, "exists": path.exists(), "warnings": []}
        if path.suffix == ".csv" and path.exists():
            df = pd.read_csv(path, encoding="utf-8")
            row["row_count"] = int(len(df))
            row["columns"] = list(df.columns)
            missing = [col for col in required.get(rel, []) if col not in df.columns]
            row["missing_required_columns"] = missing
            symbol_col = "symbol" if "symbol" in df.columns else "ticker" if "ticker" in df.columns else None
            if symbol_col:
                duplicates = df[symbol_col].astype(str).str.upper().duplicated().sum()
                row["duplicate_symbols"] = int(duplicates)
            for col in ["quantity", "avg_cost", "target_weight"]:
                if col in df.columns:
                    invalid = pd.to_numeric(df[col], errors="coerce").isna() & df[col].notna()
                    if bool(invalid.any()):
                        row["warnings"].append(f"invalid numeric values in {col}")
        rows.append(row)
    return rows


def audit_snapshots() -> dict:
    path = ROOT_DIR / "data" / "snapshots"
    files = sorted(path.glob("*.json")) if path.exists() else []
    latest = files[-1].name if files else None
    return {"exists": path.exists(), "snapshot_count": len(files), "latest_snapshot": latest}


def collect_failures(audit: dict) -> list[str]:
    failures = []
    if audit["yfinance"]["all_same_values"]:
        failures.append("yfinance returned identical values for different tickers")
    for row in audit["yfinance"]["rows"]:
        if row["all_nan"]:
            failures.append(f"yfinance all-NaN or missing history for {row['ticker']}")
        if row.get("source") == "fallback" and (row.get("confidence") or 0) > 50:
            failures.append(f"fallback shown with high confidence for {row['ticker']}")
    for row in audit["fred"]["rows"]:
        if row["latest_value"] is None and row["confidence"] > 50:
            failures.append(f"FRED missing value shown with high confidence for {row['series_id']}")
    for row in audit["binance"]["rows"]:
        if not row["connected"] and row["confidence"] > 50:
            failures.append(f"Binance missing value shown with high confidence for {row['symbol']}")
    for row in audit["local_files"]:
        if not row["exists"]:
            failures.append(f"local file missing: {row['file']}")
        if row.get("missing_required_columns"):
            failures.append(f"local file missing columns: {row['file']} {row['missing_required_columns']}")
    return failures


def write_reports(audit: dict) -> None:
    REPORT_JSON.write_text(json.dumps(audit, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    lines = ["# Data Source Audit", "", f"Generated: {audit['generated_at']}", ""]
    lines.append(f"Status: {'FAIL' if audit['failures'] else 'PASS'}")
    lines.append("\n## yfinance")
    for row in audit["yfinance"]["rows"]:
        lines.append(f"- {row['ticker']}: price={row['latest_price']} rows={row['historical_rows']} source={row['source']} confidence={row['confidence']} warning={row['warning'] or 'none'}")
    lines.append("\n## Binance")
    for row in audit["binance"]["rows"]:
        lines.append(f"- {row['symbol']}: connected={row['connected']} price={row['latest_price']} confidence={row['confidence']} warning={row['warning']}")
    lines.append("\n## FRED")
    for row in audit["fred"]["rows"]:
        lines.append(f"- {row['series_id']}: connected={row['connected']} date={row['latest_observation_date']} value={row['latest_value']} previous={row['previous_value']} confidence={row['confidence']} warning={row['warning']}")
    lines.append("\n## Local Files")
    for row in audit["local_files"]:
        lines.append(f"- {row['file']}: exists={row['exists']} rows={row.get('row_count', 'n/a')} missing={row.get('missing_required_columns', [])} duplicates={row.get('duplicate_symbols', 'n/a')} warnings={row.get('warnings', [])}")
    lines.append("\n## Snapshots")
    lines.append(f"- exists={audit['snapshots']['exists']} count={audit['snapshots']['snapshot_count']} latest={audit['snapshots']['latest_snapshot']}")
    lines.append("\n## Failures")
    lines.extend([f"- {failure}" for failure in audit["failures"]] or ["- none"])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
