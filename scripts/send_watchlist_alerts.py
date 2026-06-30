from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.data import load_watchlist
from utils.telegram import send_telegram_message


def to_float(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def build_alerts() -> list[str]:
    alerts = []
    for _, row in load_watchlist().iterrows():
        ticker = row.get("ticker")
        price = to_float(row.get("current_price"))
        stop = to_float(row.get("stop_level"))
        trim = to_float(row.get("trim_zone"))
        if price and stop and price <= stop:
            alerts.append(f"{ticker}: Risk Alert at {price}")
        elif price and trim and price >= trim:
            alerts.append(f"{ticker}: Trim zone at {price}")
    return alerts


if __name__ == "__main__":
    alerts = build_alerts()
    if alerts:
        send_telegram_message("Devin Investment OS Watchlist Alerts\n" + "\n".join(alerts))
    else:
        print("No watchlist alerts.")
