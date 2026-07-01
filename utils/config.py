import os

from dotenv import load_dotenv


load_dotenv()

ENABLE_TRADING = False
ENABLE_WITHDRAWALS = False
ENABLE_FUTURES = False
ENABLE_MARGIN = False
ENABLE_AUTO_ORDER = False


def is_configured(*keys: str) -> bool:
    return all(bool(os.getenv(key)) for key in keys)


def safety_status() -> dict:
    env_flags = {
        "ENABLE_TRADING": os.getenv("ENABLE_TRADING", "false").strip().lower(),
        "ENABLE_WITHDRAWALS": os.getenv("ENABLE_WITHDRAWALS", "false").strip().lower(),
        "ENABLE_FUTURES": os.getenv("ENABLE_FUTURES", "false").strip().lower(),
        "ENABLE_MARGIN": os.getenv("ENABLE_MARGIN", "false").strip().lower(),
        "ENABLE_AUTO_ORDER": os.getenv("ENABLE_AUTO_ORDER", "false").strip().lower(),
    }
    return {
        "trading_disabled": True,
        "withdrawals_disabled": True,
        "futures_disabled": True,
        "margin_disabled": True,
        "auto_order_disabled": True,
        "warnings": [
            f"{name} is true in .env, but this app still does not implement that capability."
            for name, value in env_flags.items()
            if value == "true"
        ],
    }
