# Data Freshness Policy

Devin Investment OS is a read-only decision-support dashboard. It is not an execution system and must not be used as the final quote source for trading.

## yfinance / Yahoo Finance

- yfinance data is best-effort and not guaranteed real-time.
- Stocks, ETFs, Taiwan tickers, and gold quotes may be delayed or incomplete.
- Taiwan stock quotes from yfinance may be delayed during TWSE trading hours.
- Taiwan tickers ending in `.TW` are labeled as reference data with a confidence cap.
- If a Taiwan quote timestamp is missing or stale while TWSE is open, the app displays a delayed / uncertain warning.

## Taiwan Stock Quotes

- TWSE regular market reference hours are approximately 09:00 to 13:30 Taipei time, Monday to Friday.
- Holiday handling is intentionally not implemented yet.
- A flat price during market hours is not treated as an error by itself.
- If price does not change after refresh, the app warns that the source may be delayed.
- Always verify Taiwan stock prices with a broker quote before trading.

## Binance

- Binance is used only as a read-only crypto data provider.
- Binance crypto quotes are higher freshness and treated as near real-time public endpoint data.
- Trading, withdrawals, futures, margin, and order endpoints are not implemented.

## FRED

- FRED macro data is reliable for macro context.
- FRED is daily or lagged and should not be treated as intraday market data.

## Execution Safety

- Devin Investment OS is decision-support only.
- Verify broker quotes before trading.
- Do not use dashboard prices as the sole basis for execution.
