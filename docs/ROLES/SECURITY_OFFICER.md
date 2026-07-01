# Security Officer Role

## Role

- Protects secrets.
- Prevents trading features.

## Checklist

- No API keys printed.
- No secrets committed.
- `.env` is ignored.
- `secrets/api_keys.local.env` is ignored.
- `secrets/ssh` is ignored.
- `ENABLE_TRADING=false`.
- `ENABLE_WITHDRAWALS=false`.
- `ENABLE_FUTURES=false`.
- `ENABLE_MARGIN=false`.
- `ENABLE_AUTO_ORDER=false`.
- No order endpoints.
- No withdrawal endpoints.
- No futures or margin trading endpoints.
