# Security

- Never commit `.env`.
- Never commit Telegram tokens, passwords, SSH keys, or broker credentials.
- Keep `.env` only on the server or local development machine.
- Telegram scripts skip gracefully if credentials are missing.
- SSH key login is used for deployment; protect the private key on the Windows machine.
- UFW allows SSH, HTTP, and Streamlit only.
- Do not add account numbers to CSV data files.
- Use `secrets/api_keys.local.env` only as a local plaintext staging file and upload it with `scripts/upload_secrets_to_vps.ps1`.
- Binance integration is read-only by design; trading, withdrawals, futures, and order endpoints are not implemented.
- API onboarding is read-only. Order placement, order modification, order cancellation, margin, futures, withdrawals, and automated orders are forbidden.
