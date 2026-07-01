# IBKR Read-only Integration Plan

IBKR integration starts read-only.

## Supported placeholders

1. CSV import for holdings exports.
2. Flex Web Service import placeholder.
3. Client Portal / Web API read-only portfolio placeholder.
4. Market data snapshot placeholder.

## Requirements

- IBKR account and session setup.
- Market data subscriptions for live data.
- Read-only permissions where possible.
- `_updated` timestamps for freshness checks.

## Safety

- No order endpoints.
- No automatic trading.
- No credential storage in git.
