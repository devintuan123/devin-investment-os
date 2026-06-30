from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.alerts import deduplicate_alerts, generate_risk_alerts, generate_watchlist_alerts
from utils.scoring import calculate_market_score
from utils.telegram import send_telegram_message


def build_daily_report() -> str:
    score = calculate_market_score({"liquidity": 68, "sentiment": 62, "breadth": 58, "ai_tech": 74, "defensive": 52})
    alerts = deduplicate_alerts(generate_watchlist_alerts() + generate_risk_alerts())

    return "\n".join(
        [
            "Devin Investment OS Daily Report",
            f"Market Score: {score['score']}/100",
            f"Regime: {score['regime']}",
            "Top Actions:",
            *[f"- {action}" for action in score["actions"][:3]],
            "Watchlist Alerts:",
            *(alerts or ["- None"]),
        ]
    )


if __name__ == "__main__":
    report = build_daily_report()
    if not send_telegram_message(report):
        print(report)
