from __future__ import annotations

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.i18n import LANG_ZH, set_lang, t


FORBIDDEN = ["Home", "Macro Dashboard", "Portfolio", "Watchlist", "Asset Scores", "Daily Playbook", "Data Quality", "Settings", "History", "Buy Zones", "Sector Heat / Capital Rotation"]
KEYS = ["home", "macro_dashboard", "portfolio", "watchlist", "asset_scores", "daily_playbook", "data_quality", "settings", "history", "buy_zones", "sector_heat_page"]


def main() -> int:
    set_lang(LANG_ZH)
    labels = [t(key) for key in KEYS]
    findings = [label for label in labels if label in FORBIDDEN]
    if findings:
        print("FAIL navigation i18n audit")
        for label in findings:
            print(f"- zh navigation contains English label: {label}")
        return 1
    print("PASS navigation i18n audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
