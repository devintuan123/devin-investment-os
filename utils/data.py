from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
PORTFOLIO_PATH = DATA_DIR / "portfolio.csv"
WATCHLIST_PATH = DATA_DIR / "watchlist.csv"

PORTFOLIO_COLUMNS = ["ticker", "name", "shares", "average_cost", "currency", "asset_type", "notes"]
WATCHLIST_COLUMNS = ["ticker", "name", "buy_zone_low", "buy_zone_high", "sell_zone", "stop_level", "notes"]


def load_portfolio() -> pd.DataFrame:
    return _load_csv(PORTFOLIO_PATH, PORTFOLIO_COLUMNS)


def load_watchlist() -> pd.DataFrame:
    return _load_csv(WATCHLIST_PATH, WATCHLIST_COLUMNS)


def save_portfolio(df: pd.DataFrame) -> None:
    _save_csv(df, PORTFOLIO_PATH, PORTFOLIO_COLUMNS)


def save_watchlist(df: pd.DataFrame) -> None:
    _save_csv(df, WATCHLIST_PATH, WATCHLIST_COLUMNS)


def _load_csv(path: Path, columns: list[str]) -> pd.DataFrame:
    DATA_DIR.mkdir(exist_ok=True)
    if not path.exists():
        pd.DataFrame(columns=columns).to_csv(path, index=False)
    df = pd.read_csv(path)
    for column in columns:
        if column not in df.columns:
            df[column] = ""
    return df


def _save_csv(df: pd.DataFrame, path: Path, columns: list[str]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    clean = df.copy()
    for column in columns:
        if column not in clean.columns:
            clean[column] = ""
    clean.to_csv(path, index=False)
