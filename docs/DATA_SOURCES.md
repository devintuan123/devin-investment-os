# Data Sources

## Current

- `yfinance` for public market prices and history.
- Binance public spot endpoint for BTC when reachable.
- Optional Binance tokenized/synthetic equity references when symbols exist in `exchangeInfo`.
- Local fallback prices in `utils/market_data.py`.
- Local CSV files for holdings and watchlist rules.
- TradingView webhook alerts for signal logging.

## Source Hierarchy

- Crypto: Binance > yfinance > fallback.
- US/ETF: IBKR future > yfinance > fallback.
- Taiwan: Yuanta future/CSV > yfinance > fallback.
- Signals: TradingView webhook > internal rules.
- Tokenized equities: exchange reference only > official broker quote remains final.

## Tokenized/Synthetic Equity References

Tokenized equity data is marked as `Tokenized/Synthetic Reference` and is never treated as an official stock quote. It can supplement sentiment for US Market and AI / Tech scores, but it never replaces yfinance, IBKR, or broker quotes.

## Fallback Policy

If yfinance fails, the app returns fallback values and warning strings instead of crashing.

## Future

- Broker CSV import.
- Snapshot history.
- Optional paid market data sources if needed.
