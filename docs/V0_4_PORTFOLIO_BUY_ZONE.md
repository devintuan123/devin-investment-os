# v0.4 Portfolio & Buy Zone Engine

## Purpose

v0.4 turns Devin Investment OS into a personal read-only investment operating system with portfolio drift, position values, and buy-zone reference levels.

It does not implement trading, order placement, order modification, withdrawals, futures, margin, or execution logic.

## Portfolio data model

`data/portfolio.csv` uses these columns:

- `symbol`
- `name`
- `category`
- `market`
- `currency`
- `quantity`
- `avg_cost`
- `target_weight`
- `account`
- `note`

Edit this CSV directly or through the Portfolio page. If an exact quantity is unknown, set `quantity` to `0` and mark the position as planned/watchlist in `account` or `note`.

## Portfolio engine

`utils/portfolio_engine.py` calculates:

- total value
- position values
- category values
- current weights
- target weights
- drift
- unrealized P/L when cost exists
- read-only action suggestions
- portfolio health score

All prices are reference data. yfinance is delayed / best-effort. Binance is used only for read-only crypto reference data.

## Buy zone engine

`utils/buy_zone_engine.py` calculates:

- latest price
- MA20 / MA60 / MA120
- 52-week high
- drawdown from high
- volatility proxy
- trend status
- buy zone levels 1 / 2 / 3
- current zone status
- bilingual action labels

Buy-zone output is decision support only. It is not an order ticket.

## Safety

- Verify broker quote before trading.
- Do not use yfinance Taiwan quotes as real-time execution data.
- Do not treat buy-zone labels as automatic signals.
- No order endpoints are implemented.
- No account secrets are committed.
