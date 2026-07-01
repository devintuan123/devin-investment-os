# Tokenized Equity Reference Provider

Tokenized or synthetic equity instruments are reference data only.

They may be derivatives, synthetic contracts, or exchange-specific instruments. They are not official NYSE/Nasdaq stock quotes and may not grant shareholder rights, voting rights, dividends, or legal ownership of the underlying equity.

## Usage Rules

- Use only as reference pricing and sentiment input.
- Do not use tokenized prices as the sole basis for buy/sell signals.
- Do not treat them as official stock prices.
- Do not implement trading, orders, futures, margin, or withdrawals.
- Always verify with a broker quote before trading.

## Data Quality

- Freshness can be high if the exchange ticker endpoint is live.
- Reliability is capped at `70`.
- If no official comparison price exists, confidence is capped at `60`.
- If basis versus official price exceeds `1%`, confidence is capped at `50`.
- If basis exceeds `3%`, a strong warning is shown.

## Risks

- Liquidity risk.
- Basis risk versus official exchange prices.
- Regulatory treatment may change.
- Instrument availability can change without notice.

Broker quote remains final before any real-world investment decision.
