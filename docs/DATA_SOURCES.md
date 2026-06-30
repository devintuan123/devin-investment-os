# Data Sources

## Current

- `yfinance` for public market prices and history.
- Local fallback prices in `utils/market_data.py`.
- Local CSV files for holdings and watchlist rules.

## Fallback Policy

If yfinance fails, the app returns fallback values and warning strings instead of crashing.

## Future

- Broker CSV import.
- Snapshot history.
- Optional paid market data sources if needed.
