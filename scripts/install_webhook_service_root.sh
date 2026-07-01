#!/usr/bin/env bash
set -euo pipefail

cat > /etc/systemd/system/devin-investment-os-webhook.service <<'SERVICE'
[Unit]
Description=Devin Investment OS TradingView Webhook Receiver
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/devin-investment-os
EnvironmentFile=-/root/devin-investment-os/.env
ExecStart=/root/devin-investment-os/.venv/bin/uvicorn webhook_receiver:app --host 127.0.0.1 --port 8502
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable devin-investment-os-webhook
systemctl restart devin-investment-os-webhook
systemctl status devin-investment-os-webhook --no-pager
