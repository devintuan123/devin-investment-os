# Devin Investment OS Performance

## Current bottlenecks

- Repeated yfinance calls for market regime, buy zones, sector heat, snapshots, and alerts.
- Sector Heat can be slow when scanning the full theme universe.
- Daily Playbook, snapshots, and alerts share several expensive calculations.

## Cache TTL policy

- yfinance prices: 300 seconds.
- yfinance history: 900 seconds.
- FRED macro data: 3600 seconds.
- Binance public price: 30 seconds.
- Market regime: 300 seconds.
- Portfolio prices: 300 seconds.
- Sector heat: 900 seconds.

## Quick scan vs full scan

Sector Heat defaults to a quick scan using up to 3 representative tickers per theme and up to 60 symbols total.
Full Scan uses the full `data/theme_universe.csv` universe and may be slower.

## Refreshing data

Use the sidebar Refresh Data button to clear in-memory market-data caches. Normal page interaction uses cached data for responsiveness.

## If the VPS is slow

Run:

```bash
bash scripts/check_server_resources.sh
```

Check memory pressure, disk usage, service status, and whether port 8501 is listening.

## Upgrade path

- Move to a VPS with more RAM/CPU if full scans are used often.
- Schedule daily snapshots so Home and History can render from saved summaries.
- Keep heavy provider checks behind explicit refresh actions.
