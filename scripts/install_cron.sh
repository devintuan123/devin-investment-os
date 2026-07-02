#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/root/devin-investment-os}"

cat <<'INFO'
This script prints optional Devin Investment OS cron entries.
It does not install them automatically.

Review timezone and Telegram settings first, then install manually with:
  crontab -e
INFO

cat <<CRON
# Devin Investment OS optional read-only jobs
15 7 * * * cd ${APP_DIR} && . .venv/bin/activate && python scripts/create_daily_snapshot.py
30 7 * * 1-5 cd ${APP_DIR} && . .venv/bin/activate && python scripts/send_daily_report.py --send --lang zh
15 22 * * 1-5 cd ${APP_DIR} && . .venv/bin/activate && python scripts/send_daily_report.py --send --lang zh
*/30 * * * * cd ${APP_DIR} && . .venv/bin/activate && python scripts/send_alerts.py --send --lang zh
CRON
