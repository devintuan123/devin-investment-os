# Codex Operating Manual

## Official local path

Always work from:
`E:\Google Drive\Python\devin-investment-os`

Never work from old temporary Codex folders.

## GitHub repository

Repository:
`https://github.com/devintuan123/devin-investment-os.git`

Primary branch:
`main`

## VPS

VPS IP:
`45.32.52.205`

SSH target:
`root@45.32.52.205`

Public URLs:
- `http://45.32.52.205`
- `http://45.32.52.205:8501`

## Active providers

- yfinance / Yahoo Finance: stocks, ETFs, Taiwan tickers, gold, and fallback market data.
- Binance: read-only crypto data and read-only account snapshot checks.
- FRED: read-only macro data.
- Telegram: outbound notifications and test alerts.

## Disabled providers

Do not activate these unless the user explicitly asks:
- IBKR
- Yuanta
- OKX
- Bitget
- TradingView webhook
- tokenized equity provider

## Secrets workflow

Local template:
`secrets/api_keys.template.env`

Local secrets file:
`secrets/api_keys.local.env`

Server destination:
`root@45.32.52.205:/root/devin-investment-os/.env`

Upload command:
`powershell -ExecutionPolicy Bypass -File scripts\upload_secrets_to_vps.ps1`

Rules:
- Never print secrets.
- Never display API keys.
- Never commit `.env`.
- Never commit `secrets/api_keys.local.env`.
- Never commit `.streamlit/secrets.toml`.
- Validate only configured / missing status when needed.

## Safety flags

These must stay false:
- `ENABLE_TRADING=false`
- `ENABLE_WITHDRAWALS=false`
- `ENABLE_FUTURES=false`
- `ENABLE_MARGIN=false`
- `ENABLE_AUTO_ORDER=false`

The project is read-only. Do not implement trading, order placement, order cancel/modify, withdrawals, futures, margin, or auto-execution logic.

## Deployment checklist

Before changing:
1. Confirm working directory is `E:\Google Drive\Python\devin-investment-os`.
2. Run `git status`.
3. Confirm no unexpected local changes.

After changing:
1. Run `python -m compileall -q .`.
2. Run relevant safe tests.
3. Confirm secrets are ignored by Git.
4. Confirm no secret files are staged.
5. Commit only safe code/docs changes.
6. Push to GitHub.
7. Deploy only if app/server behavior changed.
8. Health check `http://45.32.52.205` after deploy.

## Final report template

Every final report must include only:
1. Task completed or not
2. Files changed
3. Tests passed or failed
4. Secrets safe or not
5. Deploy status
6. Public URL
7. Commit hash
8. Blockers
