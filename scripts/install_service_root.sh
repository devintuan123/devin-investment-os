#!/usr/bin/env bash
set -euo pipefail

SERVICE_FILE="/etc/systemd/system/devin-investment-os.service"

sudo tee "$SERVICE_FILE" > /dev/null <<'SERVICE'
[Unit]
Description=Devin Investment OS Streamlit App
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/devin-investment-os
EnvironmentFile=-/root/devin-investment-os/.env
ExecStart=/root/devin-investment-os/.venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl enable devin-investment-os
sudo systemctl restart devin-investment-os
sudo systemctl status devin-investment-os --no-pager

sudo tee /etc/systemd/system/devin-investment-os-webhook.service > /dev/null <<'SERVICE'
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

sudo systemctl daemon-reload
sudo systemctl enable devin-investment-os-webhook
sudo systemctl restart devin-investment-os-webhook
sudo systemctl status devin-investment-os-webhook --no-pager
