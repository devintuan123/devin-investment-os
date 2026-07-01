# Yuanta SparkAPI Architecture

YuantaSparkAPI is based on a .NET8 C# DLL. Python integration should use `pythonnet` to load the DLL and call read-only functions.

## Recommended Path

1. Start with a local bridge.
2. Export read-only quote and position JSON files.
3. Let Devin Investment OS read those JSON files.
4. Consider a VPS/Linux bridge only after stable local testing.

## Allowed Read-only Functions

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

## Forbidden Trading Functions

- `SendStockOrder`
- `SendFutureOrder`
- `SendOVFutureOrder`
- `SendFutureCombined`
- `SendFutureApart`
- `SendAlgoCOOdrStrategy`
- `DeleteAlgoCOOdrStrategy`
- Any trading/order/cancel/modify function

## Local Files

Suggested output files:

- `data/yuanta_quotes.json`
- `data/yuanta_positions.json`

These files are ignored by git.
