# Local API Secrets

`api_keys.local.env` is local only and must never be committed.

Use read-only API keys wherever possible:

- Binance keys must have trading, withdrawals, futures, and margin disabled.
- Telegram token is only for notifications.
- TradingView webhook receives alerts only; it does not execute trades.
- IBKR fields are placeholders for future read-only workflows.

Optional hardening: IP whitelist API access to the VPS IP `45.32.52.205`.
