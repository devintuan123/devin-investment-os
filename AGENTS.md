# Devin Investment OS - Codex Standing Rules

## Official working directory

Always work only in:
`E:\Google Drive\Python\devin-investment-os`

Never work from old temporary Codex folders.

## Project purpose

Devin Investment OS is a read-only investment dashboard and decision-support system.
It provides market data, macro data, portfolio analysis, scoring, alerts, and Telegram notifications.
It must not become an automated trading system.

## Active provider stack

Active:
- yfinance / Yahoo Finance
- Binance read-only
- FRED macro data
- Telegram notifications

Future / disabled:
- IBKR
- Yuanta
- OKX
- Bitget
- TradingView webhook
- tokenized equity provider

Do not activate future providers unless the user explicitly asks.

## Safety rules

Never:
- print secrets
- display API keys
- commit secrets
- commit `.env`
- commit `secrets/api_keys.local.env`
- commit `.streamlit/secrets.toml`
- implement trading
- implement order placement
- implement order cancel/modify
- implement withdrawals
- implement futures
- implement margin
- implement auto-order or execution logic

Always:
- keep `ENABLE_TRADING=false`
- keep `ENABLE_WITHDRAWALS=false`
- keep `ENABLE_FUTURES=false`
- keep `ENABLE_MARGIN=false`
- keep `ENABLE_AUTO_ORDER=false`
- treat all external providers as read-only
- mark yfinance data as delayed / best-effort
- require broker quote verification before real trading decisions

## Secrets workflow

Local secrets file:
`secrets/api_keys.local.env`

Template:
`secrets/api_keys.template.env`

VPS destination:
`root@45.32.52.205:/root/devin-investment-os/.env`

Upload command:
`powershell -ExecutionPolicy Bypass -File scripts\upload_secrets_to_vps.ps1`

Never print or commit secret contents.

## Required checks for every task

Before changing:
- `git status`
- confirm working path

After changing:
- read `docs/REVIEW_CHECKLIST.md`
- apply relevant `docs/ROLES/*.md`
- check `docs/DEFINITION_OF_DONE.md`
- `python -m compileall -q .`
- run relevant tests
- run `python scripts/run_quality_gate.py` for non-trivial changes when available
- validate secrets only if needed without printing values
- ensure git does not include secrets
- commit safe code/docs changes only
- push to GitHub
- deploy if app/server behavior changed
- health check public URL

## Role-based review process

Before the final response for every non-trivial task, Codex must:
- read `docs/REVIEW_CHECKLIST.md`
- apply the relevant role documents in `docs/ROLES/`
- check `docs/DEFINITION_OF_DONE.md`
- run the correct audits/tests for the changed scope
- provide a role-based final report unless the user requests a stricter final format

Required review order:
1. Project Manager
2. Developer
3. Localization Specialist
4. UI/UX Designer
5. Investment Analyst
6. QA Tester
7. Security Officer

Codex must not report a task as completed unless every required role passes or a blocker is clearly reported.

If the user says "do not let Codex idle" or asks for continuous build, Codex should continue to the next planned phase only within the approved roadmap and safety boundaries.

## VPS

Public URL:
`http://45.32.52.205`
`http://45.32.52.205:8501`

Health check after deploy.

## Final report format

Every final report must include only:
1. Task completed or not
2. Files changed
3. Tests passed or failed
4. Secrets safe or not
5. Deploy status
6. Public URL
7. Commit hash
8. Blockers
