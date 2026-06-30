from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.alerts import deduplicate_alerts, generate_portfolio_alerts, generate_risk_alerts
from utils.telegram import send_telegram_message


if __name__ == "__main__":
    alerts = deduplicate_alerts(generate_risk_alerts() + generate_portfolio_alerts())
    if alerts:
        send_telegram_message("Devin Investment OS Risk Alerts\n" + "\n".join(f"- {alert}" for alert in alerts))
    else:
        print("No risk alerts.")
