from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
PORTFOLIO_PATH = DATA_DIR / "portfolio.csv"
WATCHLIST_PATH = DATA_DIR / "watchlist.csv"

PORTFOLIO_COLUMNS = [
    "ticker",
    "name",
    "shares",
    "average_cost",
    "current_price",
    "currency",
    "market_value",
    "unrealized_pnl",
    "unrealized_pnl_pct",
    "asset_type",
    "action_signal",
    "notes",
]
WATCHLIST_COLUMNS = [
    "ticker",
    "name",
    "current_price",
    "buy_zone_low",
    "buy_zone_high",
    "trim_zone",
    "stop_level",
    "priority",
    "category",
    "notes",
]


def load_portfolio() -> pd.DataFrame:
    df = _load_csv(PORTFOLIO_PATH, PORTFOLIO_COLUMNS)
    aliases = {
        "symbol": "ticker",
        "quantity": "shares",
        "avg_cost": "average_cost",
        "category": "asset_type",
        "note": "notes",
    }
    for source, target in aliases.items():
        if source in df.columns and (target not in df.columns or df[target].astype(str).eq("").all()):
            df[target] = df[source]
    return df


def load_watchlist() -> pd.DataFrame:
    return _load_csv(WATCHLIST_PATH, WATCHLIST_COLUMNS)


def save_portfolio(df: pd.DataFrame) -> None:
    _save_csv(df, PORTFOLIO_PATH)


def save_watchlist(df: pd.DataFrame) -> None:
    _save_csv(df, WATCHLIST_PATH)


def _load_csv(path: Path, columns: list[str]) -> pd.DataFrame:
    DATA_DIR.mkdir(exist_ok=True)
    if not path.exists():
        pd.DataFrame(columns=columns).to_csv(path, index=False)
    df = pd.read_csv(path)
    for column in columns:
        if column not in df.columns:
            df[column] = ""
    return df


def _save_csv(df: pd.DataFrame, path: Path) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(path, index=False)
