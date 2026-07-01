# TradingView Webhook

TradingView Premium webhooks are treated as an alert source only, not a general market data API.

Webhook endpoint:

```text
http://45.32.52.205/tradingview-webhook
```

TradingView only posts to ports `80` or `443`, so Nginx proxies this route to the local webhook receiver.

Example JSON body:

```json
{
  "secret": "your_webhook_secret",
  "ticker": "{{ticker}}",
  "price": "{{close}}",
  "timeframe": "{{interval}}",
  "message": "Alert message"
}
```

Security:

- `TRADINGVIEW_WEBHOOK_SECRET` is required in the JSON body.
- Unauthenticated alerts are rejected.
- The `secret` field is never written to the alert log.
- Alerts are logged to `data/tradingview_alerts.jsonl`.
- Alerts never execute trades.
