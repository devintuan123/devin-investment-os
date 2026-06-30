# Architecture

Devin Investment OS is a Streamlit app backed by local CSV and JSON files.

## Layers

- `utils/market_data.py`: yfinance access, fallback prices, returns, moving averages, drawdowns.
- `utils/indicators.py`: macro and asset proxy groups.
- `utils/scoring.py`: market score, regimes, category explanations, actions.
- `utils/signals.py`: watchlist zones, trim zones, stops, no-chase and pullback signals.
- `utils/playbook.py`: daily, weekly, and scenario playbooks.
- `utils/portfolio_risk.py`: allocation, high-beta exposure, hedge exposure, concentration, risk score.
- `utils/alerts.py`: alert generation and deduplication.
- `utils/snapshots.py`: daily JSON snapshot creation and history loading.

## Runtime

Streamlit runs under `devin-investment-os.service` on port `8501`. Nginx proxies port `80` to local Streamlit.
