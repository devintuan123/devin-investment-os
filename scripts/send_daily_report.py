from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.scoring import calculate_market_score
from utils.telegram import send_telegram_message


def build_daily_report() -> str:
    score_result = calculate_market_score(
        {
            "liquidity": 68,
            "sentiment": 62,
            "breadth": 58,
            "ai_tech": 74,
            "defensive": 52,
        }
    )
    top_actions = [
        "Review portfolio concentration.",
        "Check watchlist buy and risk zones.",
        "Keep new risk aligned with the current regime.",
    ]

    return "\n".join(
        [
            "Devin Investment OS Daily Report",
            f"Market Score: {score_result['score']}/100",
            f"Regime: {score_result['regime']}",
            "Top Actions:",
            *[f"- {action}" for action in top_actions],
        ]
    )


def main() -> None:
    report = build_daily_report()
    sent = send_telegram_message(report)
    if sent:
        print("Daily report sent.")
    else:
        print(report)
        print("Daily report was not sent.")


if __name__ == "__main__":
    main()
