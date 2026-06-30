# Cron Setup

Do not add cron until `.env` is configured on the VPS.

Suggested entries:

```cron
0 8 * * 1-5 cd /root/devin-investment-os && .venv/bin/python scripts/send_daily_report.py
30 8,15 * * 1-5 cd /root/devin-investment-os && .venv/bin/python scripts/send_watchlist_alerts.py
0 21 * * 1-5 cd /root/devin-investment-os && .venv/bin/python scripts/create_daily_snapshot.py
0 9 * * 1 cd /root/devin-investment-os && .venv/bin/python scripts/generate_weekly_report.py
```

Logs can be redirected to `/var/log/devin-investment-os-cron.log`.
