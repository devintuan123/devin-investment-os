#!/usr/bin/env bash

echo "=== Host ==="
hostname
echo "=== Services ==="
systemctl status devin-investment-os --no-pager
systemctl status devin-investment-os-webhook --no-pager 2>/dev/null || true
systemctl status nginx --no-pager
echo "=== Ports ==="
ss -tulpn | grep -E ':22|:80|:8501|:8502' || true
echo "=== HTTP ==="
curl -I --max-time 10 http://127.0.0.1:8501 || true
curl -I --max-time 10 http://127.0.0.1:8502/health || true
curl -I --max-time 10 http://127.0.0.1 || true
