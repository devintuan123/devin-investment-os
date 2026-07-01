from __future__ import annotations

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
REPORT_DIR = ROOT_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

import pandas as pd

from utils.i18n import LANG_EN, LANG_ZH, set_lang, t, translate_action_label, translate_regime, translate_warning
from utils.table_i18n import translate_dataframe


PAGES = [
    "home",
    "macro_dashboard",
    "portfolio",
    "watchlist",
    "asset_scores",
    "daily_playbook",
    "buy_zones",
    "history",
    "tv_alerts",
    "data_quality",
    "settings",
]
LABELS = [
    "market_score",
    "market_regime",
    "today_action",
    "data_confidence",
    "provider_status",
    "refresh_data",
    "portfolio_value",
    "target_allocation",
    "current_allocation",
    "drift",
    "freshness",
    "confidence",
    "warning",
]
ACTIONS = [
    "Potential buy zone - verify quote",
    "Extended / Do not chase",
    "Healthy trend / Hold",
    "Pullback watch",
    "Broken trend / Avoid",
    "Potential Layer 1",
    "Potential Layer 2",
    "Deep Pullback Watch",
    "Broken trend, avoid",
    "Extended, do not chase",
    "Hold",
]
WARNINGS = [
    "Taiwan stock data is reference-only. Do not use for execution.",
    "yfinance data may be delayed or best-effort.",
    "FRED macro data may be daily or lagged.",
    "Verify broker quote before actual trading.",
]


def main() -> int:
    for lang, path in [(LANG_ZH, REPORT_DIR / "i18n_snapshot_zh.txt"), (LANG_EN, REPORT_DIR / "i18n_snapshot_en.txt")]:
        set_lang(lang)
        lines = [f"Language snapshot: {lang}", ""]
        lines.append("Pages:")
        lines.extend([f"- {t(key)}" for key in PAGES])
        lines.append("")
        lines.append("Key labels:")
        lines.extend([f"- {key}: {t(key)}" for key in LABELS])
        lines.append("")
        lines.append("Action labels:")
        lines.extend([f"- {label}: {translate_action_label(label)}" for label in ACTIONS])
        lines.append("")
        lines.append("Regimes:")
        lines.extend([f"- {label}: {translate_regime(label)}" for label in ["Risk-On", "Neutral", "Risk-Off"]])
        lines.append("")
        lines.append("Warnings:")
        lines.extend([f"- {translate_warning(warning)}" for warning in WARNINGS])
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(path)
        table_path = REPORT_DIR / f"i18n_table_snapshot_{lang}.txt"
        table_lines = [f"Table language snapshot: {lang}", ""]
        for title, frame in _sample_tables():
            table_lines.append(title)
            table_lines.append(translate_dataframe(frame, lang).to_string(index=False))
            table_lines.append("")
        table_path.write_text("\n".join(table_lines).rstrip() + "\n", encoding="utf-8")
        print(table_path)
    return 0


def _sample_tables() -> list[tuple[str, pd.DataFrame]]:
    watchlist = pd.DataFrame(
        [
            {
                "symbol": "2330.TW",
                "latest_price": 1000,
                "action_label": "Potential Buy Zone - verify quote",
                "risk_label": "Medium",
                "freshness_status": "Delayed / uncertain",
                "category": "Stock",
            }
        ]
    )
    providers = pd.DataFrame(
        [
            {
                "provider": "Binance",
                "configured": "Yes",
                "connected": "Connected",
                "freshness": "Near real-time",
                "confidence": 90,
                "warning": "Verify broker quote before actual trading.",
            },
            {
                "provider": "FRED",
                "configured": "Yes",
                "connected": "Connected",
                "freshness": "Daily / lagged",
                "confidence": 85,
                "warning": "FRED macro data may be daily or lagged.",
            },
        ]
    )
    portfolio = pd.DataFrame(
        [
            {
                "symbol": "SPY",
                "category": "ETF",
                "market_value": 10000,
                "current_weight": 40,
                "target_weight": 45,
                "drift": -5,
                "action_suggestion": "Add",
            }
        ]
    )
    return [("Watchlist", watchlist), ("Provider status", providers), ("Portfolio", portfolio)]


if __name__ == "__main__":
    raise SystemExit(main())
