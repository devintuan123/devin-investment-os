# API Provider Matrix

Devin Investment OS supports read-only API onboarding only. Trading, order placement, order modification, order cancellation, withdrawals, futures, margin, and automated orders are explicitly forbidden.

## IBKR

Preferred path:

1. Web API first.
2. TWS API only as fallback.
3. FIX is not suitable for this project.

Use cases:

- Account summary.
- Portfolio positions.
- Cash.
- Unrealized P/L.
- Market data snapshot if available.
- Reports and activity later.

Do not implement:

- Order placement.
- Order modification.
- Order cancellation.
- Trading automation.

Credential fields:

```env
IBKR_ENABLED=false
IBKR_API_MODE=webapi
IBKR_ACCOUNT_ID=
IBKR_GATEWAY_URL=http://127.0.0.1:5000
IBKR_FLEX_TOKEN=
IBKR_FLEX_QUERY_ID=
```

## Yuanta SparkAPI

Architecture:

- YuantaSparkAPI is .NET8 C# DLL based.
- Python uses `pythonnet`.
- Supports Windows, Linux, and macOS.
- Use read-only query/subscription functions only.

Allowed functions:

- `Open`
- `Close`
- `Dispose`
- `Login`
- `LogOut`
- `SubscribeWatchlistAll`
- `UnSubscribeWatchlistAll`
- `GetWatchListAll`
- `GetStoreSummary`
- `GetUnrealizedGainLossDetail`
- `GetHisRealizedGainLoss`
- `GetStkTransactionOutlay`
- `GetBankBalance`
- `GetKLine` only if needed for analysis

Forbidden functions:

- `SendStockOrder`
- `SendFutureOrder`
- `SendOVFutureOrder`
- `SendFutureCombined`
- `SendFutureApart`
- `SendAlgoCOOdrStrategy`
- `DeleteAlgoCOOdrStrategy`
- Any trading/order/cancel/modify function

Credential fields:

```env
YUANTA_ENABLED=false
YUANTA_MODE=local_bridge
YUANTA_ACCOUNT=
YUANTA_LOGIN_ID=
YUANTA_LOGIN_PASSWORD=
YUANTA_CERT_PATH=
YUANTA_CERT_PASSWORD=
YUANTA_DLL_DIR=
YUANTA_QUOTE_JSON_PATH=data/yuanta_quotes.json
YUANTA_POSITION_JSON_PATH=data/yuanta_positions.json
```

## Binance

Use cases:

- `BTCUSDT` price.
- `ETHUSDT` price.
- Spot balances.

Read-only only. No trading, withdrawals, futures, margin, or order endpoints.

```env
BINANCE_ENABLED=false
BINANCE_API_KEY=
BINANCE_API_SECRET=
BINANCE_BASE_URL=https://api.binance.com
```

## OKX

Read-only backup crypto provider.

```env
OKX_ENABLED=false
OKX_API_KEY=
OKX_API_SECRET=
OKX_API_PASSPHRASE=
OKX_BASE_URL=https://www.okx.com
```

## Bitget

Read-only backup crypto provider.

```env
BITGET_ENABLED=false
BITGET_API_KEY=
BITGET_API_SECRET=
BITGET_API_PASSPHRASE=
BITGET_BASE_URL=https://api.bitget.com
```

## TradingView

Use as webhook signal source, not a market data API.

```env
TRADINGVIEW_ENABLED=false
TRADINGVIEW_WEBHOOK_SECRET=
```

## Telegram

Use for notifications.

```env
TELEGRAM_ENABLED=false
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

## FRED

Use for macro data.

```env
FRED_ENABLED=false
FRED_API_KEY=
```

## yfinance

Fallback only. No credentials.

## Implementation Order

1. Read-only credential onboarding and validation.
2. Read-only data freshness and status display.
3. CSV/manual import bridges.
4. Read-only API fetchers.
5. Alerts and reporting from validated read-only data.
