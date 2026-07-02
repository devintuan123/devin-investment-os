# Devin Investment OS Cron Setup

Cron is optional and should be installed manually only after confirming the VPS timezone, Telegram configuration, and read-only safety flags.

Recommended jobs:

```cron
# Daily snapshot
15 7 * * * cd /root/devin-investment-os && . .venv/bin/activate && python scripts/create_daily_snapshot.py

# Morning report
30 7 * * 1-5 cd /root/devin-investment-os && . .venv/bin/activate && python scripts/send_daily_report.py --send --lang zh

# Market close report
15 22 * * 1-5 cd /root/devin-investment-os && . .venv/bin/activate && python scripts/send_daily_report.py --send --lang zh

# Alert check
*/30 * * * * cd /root/devin-investment-os && . .venv/bin/activate && python scripts/send_alerts.py --send --lang zh
```

Dry-run first:

```bash
cd /root/devin-investment-os
. .venv/bin/activate
python scripts/run_daily_workflow.py --dry-run
python scripts/send_alerts.py --dry-run --lang zh
```

Safety notes:

- Jobs are decision-support only.
- No order placement, withdrawals, futures, margin, or auto-trading are enabled.
- Snapshot JSON files must not contain secrets.
- Broker quote verification remains required before real trading decisions.
