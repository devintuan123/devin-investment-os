from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from utils.buy_zone_engine import score_buy_zones
from utils.data import ROOT_DIR
from utils.market_regime import calculate_market_regime
from utils.portfolio_engine import calculate_position_values, load_portfolio, portfolio_health_score
from utils.provider_status import active_provider_rows
from utils.sector_heat_engine import calculate_theme_heat_score
from utils.strategy_rules import get_cash_deployment_mode


SNAPSHOT_DIR = ROOT_DIR / "data" / "snapshots"


def create_snapshot() -> dict:
    timestamp = datetime.now(timezone.utc)
    regime = calculate_market_regime()
    portfolio = load_portfolio()
    positions = calculate_position_values(portfolio)
    health = portfolio_health_score(portfolio)
    drift = _average_drift(positions)
    buy_zones = score_buy_zones()
    sector_heat = calculate_theme_heat_score()
    risk_warnings = [row for row in buy_zones if row.get("strategy_action") in {"Avoid chasing", "Reduce risk"}][:5]
    return {
        "timestamp": timestamp.isoformat(timespec="seconds"),
        "market_score": regime.get("market_score"),
        "market_regime": regime.get("market_regime"),
        "today_action": regime.get("today_action"),
        "provider_status": active_provider_rows(),
        "data_quality_summary": {
            "confidence_level": regime.get("confidence_level"),
            "warnings": regime.get("warnings", []),
        },
        "portfolio_summary": {
            "health_score": health.get("score"),
            "summary": health.get("summary"),
            "warnings": health.get("warnings", []),
        },
        "portfolio_drift_summary": {
            "average_abs_drift": drift,
            "positions": _safe_records(positions[["symbol", "current_weight", "target_weight", "drift"]] if not positions.empty else positions),
        },
        "buy_zone_candidates": [
            row for row in buy_zones if row.get("strategy_action") in {"DCA only", "Potential buy zone", "Consider gradual allocation", "Hold"}
        ][:10],
        "sector_heat_summary": _safe_records(sector_heat.head(10)),
        "top_hot_themes": _safe_records(sector_heat.head(5)),
        "top_risk_warnings": risk_warnings,
        "cash_deployment_mode": get_cash_deployment_mode(regime.get("market_score", 0), regime.get("market_regime", ""), drift),
    }


def save_snapshot(snapshot: dict | None = None) -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = create_snapshot() if snapshot is None else snapshot
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = SNAPSHOT_DIR / f"{stamp}.json"
    path.write_text(json.dumps(_redact(snapshot), ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_latest_snapshot() -> dict:
    snapshots = list_snapshots()
    if not snapshots:
        return {}
    return _load_json(snapshots[-1])


def list_snapshots() -> list[Path]:
    if not SNAPSHOT_DIR.exists():
        return []
    return sorted(SNAPSHOT_DIR.glob("*.json"))


def load_snapshot_history() -> list[dict]:
    return [_load_json(path) for path in list_snapshots()]


def summarize_snapshot_trend() -> dict:
    history = load_snapshot_history()
    if not history:
        return {"count": 0, "latest_market_score": None, "score_change": None, "latest_regime": None}
    latest = history[-1]
    first = history[0]
    return {
        "count": len(history),
        "latest_market_score": latest.get("market_score"),
        "score_change": _num(latest.get("market_score")) - _num(first.get("market_score")),
        "latest_regime": latest.get("market_regime"),
        "latest_snapshot": latest.get("timestamp"),
    }


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _safe_records(df: pd.DataFrame) -> list[dict]:
    if df is None or df.empty:
        return []
    clean = df.copy()
    for column in clean.columns:
        clean[column] = clean[column].map(lambda value: value.item() if hasattr(value, "item") else value)
    return clean.to_dict(orient="records")


def _average_drift(positions: pd.DataFrame) -> float:
    if positions.empty or "drift" not in positions:
        return 0.0
    return float(pd.to_numeric(positions["drift"], errors="coerce").abs().mean())


def _num(value) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _redact(snapshot: dict) -> dict:
    forbidden = {"api_key", "secret", "token", "password", "credential"}

    def scrub(value):
        if isinstance(value, dict):
            return {key: ("[REDACTED]" if any(term in key.lower() for term in forbidden) else scrub(item)) for key, item in value.items()}
        if isinstance(value, list):
            return [scrub(item) for item in value]
        return value

    return scrub(snapshot)
