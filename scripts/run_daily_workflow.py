from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from scripts.send_daily_report import build_daily_report
from utils.alert_engine import send_alerts_if_needed
from utils.i18n import LANG_EN, LANG_ZH
from utils.snapshot_store import save_snapshot
from utils.telegram import send_telegram_message


def main() -> int:
    parser = argparse.ArgumentParser(description="Run daily read-only Devin Investment OS workflow.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Create local snapshot and print reports only.")
    mode.add_argument("--send", action="store_true", help="Create snapshot and send Telegram reports.")
    parser.add_argument("--lang", choices=[LANG_ZH, LANG_EN], default=LANG_ZH)
    args = parser.parse_args()
    snapshot_path = save_snapshot()
    print(f"snapshot_saved {snapshot_path}")
    send_alerts_if_needed(lang=args.lang, dry_run=not args.send)
    report = build_daily_report(args.lang)
    if args.send:
        sent = send_telegram_message(report)
        print("daily_report_sent" if sent else "daily_report_not_sent")
        return 0 if sent else 1
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
