# API Keys Setup

This workflow lets you edit one local file on Windows and upload it to the VPS as the app runtime `.env`.

## Windows Workflow

1. Copy the template:

```powershell
Copy-Item secrets/api_keys.template.env secrets/api_keys.local.env
```

2. Open it with Notepad:

```powershell
notepad secrets/api_keys.local.env
```

3. Fill in API keys locally.

4. Upload to the VPS:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/upload_secrets_to_vps.ps1
```

5. The upload script automatically secures `/root/devin-investment-os/.env` with `chmod 600` and restarts Streamlit.

6. Verify:

- http://45.32.52.205
- Open the Settings page and check configured status.

## Security Notes

- Use Binance read-only API keys.
- Disable Binance trading.
- Disable Binance withdrawals.
- Disable Binance futures and margin.
- Set Binance IP whitelist to `45.32.52.205` if possible.
- Never commit secrets.
- Rotate any API key immediately if exposed.
