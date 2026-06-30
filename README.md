# Devin Investment OS

Devin Investment OS is a simple Streamlit investment dashboard with local CSV storage, macro score placeholders, portfolio editing, watchlist signals, Telegram alerts, and Ubuntu deployment scripts.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Then edit `.env`:

```bash
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Do not commit `.env`.

## Server Setup

```bash
git clone <your-repo-url>
cd devin-investment-os
bash scripts/deploy_ubuntu.sh
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## Systemd Setup

For a root deployment:

```bash
bash scripts/install_service_root.sh
```

For an `ubuntu` user deployment:

```bash
bash scripts/install_service_ubuntu.sh
```

Then manage the service:

```bash
sudo systemctl status devin-investment-os
sudo systemctl restart devin-investment-os
sudo journalctl -u devin-investment-os -f
```

## Data Files

- `data/portfolio.csv`
- `data/watchlist.csv`

The app reads and writes these files locally.
