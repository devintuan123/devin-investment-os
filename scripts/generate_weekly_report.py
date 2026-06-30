from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.playbook import weekly_playbook
from utils.snapshots import load_snapshots


def generate_weekly_report() -> str:
    snapshots = load_snapshots()
    latest = snapshots[-1] if snapshots else {}
    playbook = weekly_playbook()
    lines = [
        "Devin Investment OS Weekly Report",
        f"Latest Market Score: {latest.get('market_score', 'N/A')}",
        f"Latest Regime: {latest.get('regime', 'N/A')}",
        "Next Week Focus:",
        *[f"- {item}" for item in playbook["focus"]],
        f"Rebalance Bias: {playbook['rebalance_bias']}",
        f"Risk Review: {playbook['risk_review']}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(generate_weekly_report())
