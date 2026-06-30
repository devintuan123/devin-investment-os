from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from utils.alerts import generate_risk_alerts, generate_watchlist_alerts
from utils.data import ROOT_DIR, load_portfolio, load_watchlist
from utils.portfolio_risk import portfolio_summary
from utils.scoring import calculate_market_score
from utils.signals import watchlist_signal


SNAPSHOT_DIR = ROOT_DIR / "data" / "snapshots"


def build_snapshot() -> dict:
    portfolio = load_portfolio()
    watchlist = load_watchlist()
    watchlist["signal"] = watchlist.apply(watchlist_signal, axis=1)
    market = calculate_market_score({"liquidity": 68, "sentiment": 62, "breadth": 58, "ai_tech": 74, "defensive": 52})
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "market_score": market["score"],
        "regime": market["regime"],
        "asset_scores": market["categories"],
        "watchlist_signals": watchlist[["ticker", "signal"]].to_dict(orient="records"),
        "portfolio_summary": portfolio_summary(portfolio),
        "alerts": generate_watchlist_alerts(watchlist) + generate_risk_alerts(portfolio),
    }


def save_daily_snapshot() -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = build_snapshot()
    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = SNAPSHOT_DIR / f"snapshot_{stamp}.json"
    path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    return path


def load_snapshots() -> list[dict]:
    if not SNAPSHOT_DIR.exists():
        return []
    snapshots = []
    for path in sorted(SNAPSHOT_DIR.glob("snapshot_*.json")):
        try:
            snapshots.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return snapshots
