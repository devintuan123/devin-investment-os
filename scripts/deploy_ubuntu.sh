#!/usr/bin/env bash
set -euo pipefail

sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl nano

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example. Edit it before enabling Telegram alerts."
else
  echo ".env already exists. Leaving it unchanged."
fi

echo "Run the app with:"
echo "streamlit run app.py --server.port 8501 --server.address 0.0.0.0"
