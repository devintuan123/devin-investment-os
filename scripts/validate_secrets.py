import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "secrets" / "api_keys.local.env")

PROVIDER_KEYS = {
    "IBKR": [
        "IBKR_ENABLED",
        "IBKR_API_MODE",
        "IBKR_ACCOUNT_ID",
        "IBKR_GATEWAY_URL",
        "IBKR_FLEX_TOKEN",
        "IBKR_FLEX_QUERY_ID",
    ],
    "Yuanta": [
        "YUANTA_ENABLED",
        "YUANTA_MODE",
        "YUANTA_ACCOUNT",
        "YUANTA_LOGIN_ID",
        "YUANTA_LOGIN_PASSWORD",
        "YUANTA_CERT_PATH",
        "YUANTA_CERT_PASSWORD",
        "YUANTA_DLL_DIR",
        "YUANTA_QUOTE_JSON_PATH",
        "YUANTA_POSITION_JSON_PATH",
    ],
    "Binance": ["BINANCE_ENABLED", "BINANCE_API_KEY", "BINANCE_API_SECRET", "BINANCE_BASE_URL"],
    "OKX": ["OKX_ENABLED", "OKX_API_KEY", "OKX_API_SECRET", "OKX_API_PASSPHRASE", "OKX_BASE_URL"],
    "Bitget": ["BITGET_ENABLED", "BITGET_API_KEY", "BITGET_API_SECRET", "BITGET_API_PASSPHRASE", "BITGET_BASE_URL"],
    "TradingView": ["TRADINGVIEW_ENABLED", "TRADINGVIEW_WEBHOOK_SECRET"],
    "Telegram": ["TELEGRAM_ENABLED", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"],
    "FRED": ["FRED_ENABLED", "FRED_API_KEY"],
}
SAFETY_FLAGS = ["ENABLE_TRADING", "ENABLE_WITHDRAWALS", "ENABLE_FUTURES", "ENABLE_MARGIN", "ENABLE_AUTO_ORDER"]


def status(name: str) -> str:
    return "configured" if os.getenv(name) else "missing"


def flag_value(name: str) -> str:
    return str(os.getenv(name, "false")).strip().lower()


def main() -> None:
    for provider, keys in PROVIDER_KEYS.items():
        configured = sum(1 for key in keys if os.getenv(key))
        print(f"{provider}: {'configured' if configured else 'missing'}")
        for key in keys:
            print(f"  {key}: {status(key)}")

    print("yfinance fallback: available (no credentials)")

    for flag in SAFETY_FLAGS:
        value = flag_value(flag)
        print(f"{flag}: {value}")
        if value == "true":
            print(f"WARNING: {flag} is true. Trading, withdrawals, futures, margin, and auto-order are not supported by this app.")


if __name__ == "__main__":
    main()
