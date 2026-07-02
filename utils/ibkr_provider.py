from __future__ import annotations

from datetime import datetime

import pandas as pd


def import_holdings_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8")
    df["_updated"] = datetime.utcnow().isoformat() + "Z"
    df["_source"] = "ibkr_csv_read_only"
    return df


def flex_web_service_placeholder() -> dict:
    return {
        "enabled": False,
        "source": "ibkr_flex_read_only_placeholder",
        "requires": ["IBKR_ACCOUNT_ID", "IBKR_FLEX_TOKEN", "IBKR_FLEX_QUERY_ID"],
        "_updated": None,
    }


def client_portal_portfolio_placeholder() -> dict:
    return {
        "enabled": False,
        "source": "ibkr_client_portal_read_only_placeholder",
        "requires": ["authenticated session", "read-only portfolio permissions"],
        "_updated": None,
    }


def market_data_snapshot_placeholder() -> dict:
    return {
        "enabled": False,
        "source": "ibkr_market_data_snapshot_future",
        "requires": ["market data subscriptions", "session management"],
        "_updated": None,
    }


def place_order(*args, **kwargs) -> None:
    raise NotImplementedError("IBKR order endpoints are not implemented.")
