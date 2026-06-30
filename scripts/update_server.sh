#!/usr/bin/env bash
set -e

APP_DIR="/root/devin-investment-os"
cd "$APP_DIR"
git fetch origin
git reset --hard origin/main
source .venv/bin/activate
pip install -r requirements.txt
systemctl restart devin-investment-os
sleep 5
systemctl status devin-investment-os --no-pager
curl -I --max-time 10 http://127.0.0.1:8501
