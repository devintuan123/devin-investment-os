# Data Sources

## Current

- `yfinance` for public market prices and history.
- Binance public spot endpoint for BTC when reachable.
- Local fallback prices in `utils/market_data.py`.
- Local CSV files for holdings and watchlist rules.
- TradingView webhook alerts for signal logging.

## Source Hierarchy

- Crypto: Binance > yfinance > fallback.
- US/ETF: IBKR future > yfinance > fallback.
- Taiwan: Yuanta future/CSV > yfinance > fallback.
- Signals: TradingView webhook > internal rules.

## Fallback Policy

If yfinance fails, the app returns fallback values and warning strings instead of crashing.

## Future

- Broker CSV import.
- Snapshot history.
- Optional paid market data sources if needed.
