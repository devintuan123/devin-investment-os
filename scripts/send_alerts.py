from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.alert_engine import send_alerts_if_needed
from utils.i18n import LANG_EN, LANG_ZH


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate read-only Devin Investment OS alerts.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Print alert summary without sending.")
    mode.add_argument("--send", action="store_true", help="Send alert summary to Telegram.")
    parser.add_argument("--lang", choices=[LANG_ZH, LANG_EN], default=LANG_ZH)
    args = parser.parse_args()
    dry_run = not args.send
    ok = send_alerts_if_needed(lang=args.lang, dry_run=dry_run)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
