# Devin Investment OS

Devin Investment OS is a Streamlit dashboard for a personal investment workflow. It tracks market regime, portfolio risk, watchlist buy zones, asset scores, and a daily playbook.

This is not financial advice.

## Features

- Home dashboard with Market Score, regime, actions, portfolio preview, and watchlist preview.
- Macro dashboard covering Liquidity, Sentiment, Breadth, AI / Tech, and Defensive / Hedge.
- Portfolio editor with price refresh, market value, unrealized P/L, allocation, and high-beta exposure.
- Watchlist editor with Buy Zone, Watch, Trim, and Risk Alert signals.
- Asset Scores and Daily Playbook pages.
- History page for daily snapshots and regime changes.
- TradingView alert page with secure webhook logging.
- Telegram report and alert scripts that skip gracefully when `.env` is missing.
- Nginx reverse proxy and systemd server workflow.

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Server Deployment

```bash
git clone https://github.com/devintuan123/devin-investment-os.git
cd devin-investment-os
bash scripts/deploy_ubuntu.sh
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Install root systemd service:

```bash
bash scripts/install_service_root.sh
```

## Update Workflow

On the VPS:

```bash
bash /root/update_devin_investos.sh
```

Or from this repo:

```bash
bash scripts/update_server.sh
```

Health check:

```bash
bash /root/check_devin_investos.sh
bash scripts/health_check.sh
```

## Telegram Setup

Copy `.env.example` to `.env` on the server and fill in:

```bash
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Do not commit `.env`.

For the full local Windows secrets workflow, see `docs/API_KEYS_SETUP.md`.

Manual report scripts:

```bash
python scripts/send_daily_report.py
python scripts/send_watchlist_alerts.py
python scripts/send_risk_alerts.py
python scripts/create_daily_snapshot.py
python scripts/generate_weekly_report.py
```

More docs live in `docs/`, including architecture, cron setup, security, data sources, TODOs, and the Level 3 roadmap.

Provider docs:

- `docs/TRADINGVIEW_WEBHOOK.md`
- `docs/IBKR_READ_ONLY_PLAN.md`
- `docs/YUANTA_INTEGRATION_PLAN.md`
- `docs/TOKENIZED_EQUITY_PROVIDER.md`
- `docs/API_PROVIDER_MATRIX.md`
- `docs/YUANTA_SPARKAPI_ARCHITECTURE.md`

Optional cron examples:

```cron
0 8 * * 1-5 cd /root/devin-investment-os && .venv/bin/python scripts/send_daily_report.py
*/30 * * * 1-5 cd /root/devin-investment-os && .venv/bin/python scripts/send_watchlist_alerts.py
```

## Data Files

- `data/portfolio.csv`
- `data/watchlist.csv`

These files contain holdings and watch zones only. Do not add account numbers or secrets.

## Security Notes

- Do not commit `.env`, passwords, SSH keys, Telegram tokens, or account numbers.
- Keep SSH port 22 protected and do not expose secrets in logs.
- Market data uses yfinance with fallback values so the app remains stable during data failures.
