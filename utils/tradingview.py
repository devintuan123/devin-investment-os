from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from utils.data import ROOT_DIR


ALERT_LOG_PATH = ROOT_DIR / "data" / "tradingview_alerts.jsonl"


def validate_webhook_secret(payload: dict) -> bool:
    expected = os.getenv("TRADINGVIEW_WEBHOOK_SECRET", "")
    provided = str(payload.get("secret", ""))
    return bool(expected) and provided == expected


def sanitize_alert(payload: dict) -> dict:
    blocked = {"secret", "TRADINGVIEW_WEBHOOK_SECRET"}
    return {
        "received_at": datetime.utcnow().isoformat() + "Z",
        "source": "tradingview",
        "ticker": payload.get("ticker") or payload.get("symbol") or "",
        "alert": payload.get("alert") or payload.get("message") or "",
        "timeframe": payload.get("timeframe", ""),
        "price": payload.get("price", ""),
        "raw": {key: value for key, value in payload.items() if key not in blocked},
        "action": "log_only_no_trade",
    }


def log_alert(payload: dict) -> dict:
    ALERT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    alert = sanitize_alert(payload)
    with ALERT_LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(alert, ensure_ascii=False) + "\n")
    return alert


def load_alerts(limit: int = 200) -> list[dict]:
    if not ALERT_LOG_PATH.exists():
        return []
    rows = []
    for line in ALERT_LOG_PATH.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows[-limit:]
