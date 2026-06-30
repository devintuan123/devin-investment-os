from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.data import load_watchlist
from utils.scoring import calculate_market_score
from utils.telegram import send_telegram_message


def build_daily_report() -> str:
    score = calculate_market_score({"liquidity": 68, "sentiment": 62, "breadth": 58, "ai_tech": 74, "defensive": 52})
    watchlist = load_watchlist()
    alerts = []
    if "current_price" in watchlist:
        for _, row in watchlist.iterrows():
            price = _to_float(row.get("current_price"))
            stop = _to_float(row.get("stop_level"))
            if price and stop and price <= stop:
                alerts.append(f"{row.get('ticker')}: Risk Alert")

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


def _to_float(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


if __name__ == "__main__":
    report = build_daily_report()
    if not send_telegram_message(report):
        print(report)
