import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "secrets" / "api_keys.local.env")

REQUIRED_KEYS = [
    "BINANCE_API_KEY",
    "BINANCE_API_SECRET",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "TRADINGVIEW_WEBHOOK_SECRET",
]
IBKR_KEYS = ["IBKR_ACCOUNT_ID", "IBKR_FLEX_TOKEN", "IBKR_FLEX_QUERY_ID"]
SAFETY_FLAGS = ["ENABLE_TRADING", "ENABLE_WITHDRAWALS", "ENABLE_FUTURES"]


def status(name: str) -> str:
    return "configured" if os.getenv(name) else "missing"


def flag_value(name: str) -> str:
    return str(os.getenv(name, "false")).strip().lower()


def main() -> None:
    for key in REQUIRED_KEYS:
        print(f"{key}: {status(key)}")

    ibkr_configured = any(os.getenv(key) for key in IBKR_KEYS)
    print(f"IBKR placeholders: {'configured' if ibkr_configured else 'missing'}")

    for flag in SAFETY_FLAGS:
        value = flag_value(flag)
        print(f"{flag}: {value}")
        if value == "true":
            print(f"WARNING: {flag} is true. Trading, withdrawals, and futures are not supported by this app.")


if __name__ == "__main__":
    main()
