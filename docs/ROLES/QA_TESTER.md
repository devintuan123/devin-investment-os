# QA Tester Role

## Role

- Tests workflows end-to-end.

## Checklist

- App starts.
- Home works.
- Watchlist works.
- Portfolio works.
- Buy Zones works.
- Daily Playbook works.
- Data Quality works.
- Language switching works.
- Refresh works.
- Telegram dry-run works.
- No page crashes if an external provider fails.
- `python scripts/enforce_macro_data_gate.py` passes.
- Macro Dashboard displays raw FRED and market proxy tables.
- Missing provider data produces a visible warning.
- No silent fallback is shown as normal/high confidence.
