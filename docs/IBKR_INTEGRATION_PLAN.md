# IBKR Integration Plan

Do not store IBKR credentials in git.

## Phase 1

- Add manual CSV import for IBKR holdings exports.
- Normalize tickers, currencies, quantities, and cost basis.

## Phase 2

- Add validation reports for missing currency, cost, or symbol mapping.

## Phase 3

- Consider API integration only after the CSV workflow is stable.
- Keep credentials outside the repo in local environment variables or secure server storage.
