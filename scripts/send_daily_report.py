from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.buy_zone_engine import score_buy_zones
from utils.market_regime import calculate_market_regime
from utils.portfolio_engine import calculate_position_values, load_portfolio, portfolio_health_score
from utils.telegram import send_telegram_message


def build_daily_report() -> str:
    regime = calculate_market_regime()
    health = portfolio_health_score(load_portfolio())
    positions = calculate_position_values(load_portfolio())
    buy_zones = score_buy_zones()
    top_candidates = [row for row in buy_zones if row["action_label"] in {"Potential Layer 1", "Potential Layer 2", "Deep Pullback Watch", "Hold"}][:3]
    risk_warnings = [row for row in buy_zones if row["action_label"] in {"Broken trend, avoid", "Extended, do not chase"}][:3]

    drift_summary = "No portfolio data"
    if not positions.empty:
        average_drift = float(positions["drift"].abs().mean())
        drift_summary = f"Portfolio health {health['score']}/100; average drift {average_drift:.1f}%"

    return "\n".join(
        [
            "Devin Investment OS Daily Report",
            f"Market Score: {regime['market_score']}/100",
            f"Regime: {regime['market_regime']}",
            f"Today Action: {regime['today_action']}",
            drift_summary,
            "Top Buy-Zone Candidates:",
            *[f"- {row['ticker']}: {row['action_label']} @ {row['latest_price']:.2f}" for row in top_candidates],
            "Top Risk Warnings:",
            *([f"- {row['ticker']}: {row['action_label']}" for row in risk_warnings] or ["- None"]),
            f"Data Quality: {regime['confidence_level']} confidence; {regime['warnings'][0]}",
            "Read-only decision support. Verify broker quote before trading.",
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


if __name__ == "__main__":
    raise SystemExit(main())
