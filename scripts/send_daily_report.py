from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.market_regime import calculate_market_regime
from utils.telegram import send_telegram_message
from utils.watchlist_scoring import score_watchlist


def build_daily_report() -> str:
    regime = calculate_market_regime()
    watch_scores = score_watchlist()
    top_signals = watch_scores[:3]
    metrics = regime["key_metrics"]
    ten_year = metrics.get("10Y Yield")
    btc = metrics.get("BTC")
    gold = metrics.get("Gold")

    return "\n".join(
        [
            "Devin Investment OS Daily Report",
            f"Market Score: {regime['market_score']}/100",
            f"Market Regime: {regime['market_regime']}",
            f"Today Action: {regime['today_action']}",
            f"VIX: {_fmt(metrics.get('VIX'))}",
            f"10Y Yield: {_fmt(ten_year, suffix='%')}",
            f"BTC Price: {_fmt(btc, prefix='$')}",
            f"Gold Status: {_gold_status(regime, gold)}",
            "Top 3 Watchlist Signals:",
            *[f"- {row['ticker']}: {row['action_label']}" for row in top_signals],
            f"Risk Warning: {regime['risk_warnings'][0]}",
            "Decision-support only. Verify broker quote before trading.",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Send Devin Investment OS daily read-only Telegram report.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Print the report without sending.")
    mode.add_argument("--send", action="store_true", help="Send the report to Telegram.")
    args = parser.parse_args()

    report = build_daily_report()
    if args.send:
        sent = send_telegram_message(report)
        print("Telegram daily report sent." if sent else "Telegram daily report not sent.")
        return 0 if sent else 1

    print(report)
    return 0


def _fmt(value: object, prefix: str = "", suffix: str = "") -> str:
    if value is None:
        return "n/a"
    try:
        return f"{prefix}{float(value):,.2f}{suffix}"
    except (TypeError, ValueError):
        return str(value)


def _gold_status(regime: dict, gold: object) -> str:
    score = regime["components"].get("Gold", 50)
    label = "defensive bid" if score >= 58 else "neutral"
    return f"{label} ({_fmt(gold, prefix='$')})"


if __name__ == "__main__":
    raise SystemExit(main())
