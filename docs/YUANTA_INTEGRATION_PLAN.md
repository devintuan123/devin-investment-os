# Yuanta Integration Plan

Yuanta integration is a future item after account approval.

## First approach

- Manual CSV import of Taiwan holdings.
- Normalize symbols, quantities, average cost, currency, and update timestamps.
- Use yfinance Taiwan tickers as the current market-data fallback.

## Safety

- Do not implement trading.
- Do not store account credentials in git.
- Do not add order placement until explicitly approved.
