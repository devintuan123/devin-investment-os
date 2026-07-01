from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.buy_zone_engine import score_buy_zones
from utils.i18n import LANG_EN, LANG_ZH, set_lang, t, translate_action_label, translate_regime, translate_warning
from utils.market_regime import calculate_market_regime
from utils.portfolio_engine import calculate_position_values, load_portfolio, portfolio_health_score
from utils.telegram import send_telegram_message


def build_daily_report(lang: str = LANG_ZH) -> str:
    set_lang(lang)
    regime = calculate_market_regime()
    health = portfolio_health_score(load_portfolio())
    positions = calculate_position_values(load_portfolio())
    buy_zones = score_buy_zones()
    top_candidates = [row for row in buy_zones if row["action_label"] in {"Potential Layer 1", "Potential Layer 2", "Deep Pullback Watch", "Hold"}][:3]
    risk_warnings = [row for row in buy_zones if row["action_label"] in {"Broken trend, avoid", "Extended, do not chase"}][:3]

    drift_summary = t("no_data")
    if not positions.empty:
        average_drift = float(positions["drift"].abs().mean())
        drift_summary = f"{t('portfolio_health')} {health['score']}/100; {t('drift')} {average_drift:.1f}%"

    return "\n".join(
        [
            f"Devin Investment OS {t('daily_playbook')}",
            f"{t('market_score')}: {regime['market_score']}/100",
            f"{t('market_regime')}: {translate_regime(regime['market_regime'])}",
            f"{t('today_action')}: {translate_action_label(regime['today_action'])}",
            drift_summary,
            f"{t('buy_zone_candidates')}:",
            *[f"- {row['ticker']}: {translate_action_label(row['action_label'])} @ {row['latest_price']:.2f}" for row in top_candidates],
            f"{t('risk_warnings')}:",
            *([f"- {row['ticker']}: {translate_action_label(row['action_label'])}" for row in risk_warnings] or [f"- {t('no_data')}"]),
            f"{t('data_quality')}: {t(regime['confidence_level'].lower())}; {translate_warning(regime['warnings'][0])}",
            t("broker_warning"),
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Send Devin Investment OS daily read-only Telegram report.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Print the report without sending.")
    mode.add_argument("--send", action="store_true", help="Send the report to Telegram.")
    parser.add_argument("--lang", choices=[LANG_ZH, LANG_EN], default=LANG_ZH, help="Report language. Defaults to Traditional Chinese.")
    args = parser.parse_args()

    report = build_daily_report(args.lang)
    if args.send:
        sent = send_telegram_message(report)
        print("Telegram daily report sent." if sent else "Telegram daily report not sent.")
        return 0 if sent else 1

    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
