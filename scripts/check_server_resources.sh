#!/usr/bin/env bash
set -euo pipefail

echo "=== uptime ==="
uptime

echo ""
echo "=== memory ==="
free -h

echo ""
echo "=== disk ==="
df -h /

echo ""
echo "=== cpu load ==="
top -bn1 | head -n 5

echo ""
echo "=== streamlit process ==="
pgrep -af streamlit || true

echo ""
echo "=== service status ==="
systemctl status devin-investment-os --no-pager || true

echo ""
echo "=== port 8501 ==="
ss -tulpn | grep 8501 || true
