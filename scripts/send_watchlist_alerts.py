from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.alerts import generate_watchlist_alerts
from utils.telegram import send_telegram_message


if __name__ == "__main__":
    alerts = generate_watchlist_alerts()
    if alerts:
        send_telegram_message("Devin Investment OS Watchlist Alerts\n" + "\n".join(alerts))
    else:
        print("No watchlist alerts.")
