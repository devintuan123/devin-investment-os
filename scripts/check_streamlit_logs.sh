#!/usr/bin/env bash
set -euo pipefail

LOG_LINES="${1:-300}"
echo "=== devin-investment-os logs ==="
journalctl -u devin-investment-os -n "$LOG_LINES" --no-pager > /tmp/devin-investment-os-streamlit.log || true
cat /tmp/devin-investment-os-streamlit.log

if grep -E "Traceback|UnicodeDecodeError|UnicodeEncodeError|StreamlitInvalidHeightError|Duplicate column names|ValueError|嚙|�|癟|疆|矇|疇|瓊|癡|璽" /tmp/devin-investment-os-streamlit.log; then
  echo "Streamlit log check failed."
  exit 1
fi

echo "Streamlit log check passed."
