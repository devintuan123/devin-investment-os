from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
BACKUP_DIR = DATA_DIR / "backups"
PORTFOLIO_PATH = DATA_DIR / "portfolio.csv"
TRANSACTIONS_PATH = DATA_DIR / "transactions.csv"
SETTINGS_PATH = DATA_DIR / "portfolio_settings.yaml"

PORTFOLIO_COLUMNS = [
    "symbol",
    "name",
    "category",
    "market",
    "currency",
    "quantity",
    "avg_cost",
    "target_weight",
    "account",
    "note",
    "updated_at",
]
TRANSACTION_COLUMNS = [
    "timestamp",
    "action_type",
    "symbol",
    "quantity",
    "price",
    "currency",
    "fees",
    "realized_pl",
    "note",
]


def load_portfolio() -> pd.DataFrame:
    DATA_DIR.mkdir(exist_ok=True)
    if not PORTFOLIO_PATH.exists():
        pd.DataFrame(columns=PORTFOLIO_COLUMNS).to_csv(PORTFOLIO_PATH, index=False)
    return _normalize_portfolio(pd.read_csv(PORTFOLIO_PATH))


def save_portfolio(df: pd.DataFrame) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    clean = _normalize_portfolio(df)
    clean[PORTFOLIO_COLUMNS].to_csv(PORTFOLIO_PATH, index=False)


def backup_portfolio() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = _now().replace(":", "").replace("-", "")
    backup_path = BACKUP_DIR / f"portfolio_{timestamp}.csv"
    if PORTFOLIO_PATH.exists():
        backup_path.write_bytes(PORTFOLIO_PATH.read_bytes())
    else:
        pd.DataFrame(columns=PORTFOLIO_COLUMNS).to_csv(backup_path, index=False)
    return backup_path


def clear_portfolio(confirm: bool) -> bool:
    if not confirm:
        return False
    backup_portfolio()
    pd.DataFrame(columns=PORTFOLIO_COLUMNS).to_csv(PORTFOLIO_PATH, index=False)
    record_transaction("CLEAR_ALL", "", 0, 0, "", 0, 0, "Manual clear all holdings")
    return True


def add_holding(symbol, quantity, price, currency="USD", category="Stock", account="", note="", name="", market="") -> pd.DataFrame:
    symbol = normalize_symbol(symbol)
    quantity = float(quantity or 0)
    price = float(price or 0)
    if not symbol or quantity <= 0 or price < 0:
        raise ValueError("Invalid holding input.")
    portfolio = load_portfolio()
    now = _now()
    mask = portfolio["symbol"] == symbol
    if mask.any():
        index = portfolio.index[mask][0]
        old_quantity = float(portfolio.loc[index, "quantity"])
        old_cost = float(portfolio.loc[index, "avg_cost"])
        new_quantity = old_quantity + quantity
        portfolio.loc[index, "quantity"] = new_quantity
        portfolio.loc[index, "avg_cost"] = ((old_quantity * old_cost) + (quantity * price)) / new_quantity if new_quantity else 0
        portfolio.loc[index, "currency"] = currency
        portfolio.loc[index, "category"] = category
        portfolio.loc[index, "account"] = account
        portfolio.loc[index, "note"] = note
        portfolio.loc[index, "updated_at"] = now
    else:
        portfolio = pd.concat(
            [
                portfolio,
                pd.DataFrame(
                    [
                        {
                            "symbol": symbol,
                            "name": name or symbol,
                            "category": category,
                            "market": market or _infer_market(symbol),
                            "currency": currency,
                            "quantity": quantity,
                            "avg_cost": price,
                            "target_weight": 0,
                            "account": account,
                            "note": note,
                            "updated_at": now,
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )
    save_portfolio(portfolio)
    record_transaction("BUY_MANUAL", symbol, quantity, price, currency, 0, 0, note)
    return load_portfolio()


def reduce_holding(symbol, quantity, price, fees=0, note="") -> pd.DataFrame:
    symbol = normalize_symbol(symbol)
    quantity = float(quantity or 0)
    price = float(price or 0)
    fees = float(fees or 0)
    portfolio = load_portfolio()
    mask = portfolio["symbol"] == symbol
    if not mask.any() or quantity <= 0:
        raise ValueError("Position not found or invalid quantity.")
    index = portfolio.index[mask][0]
    old_quantity = float(portfolio.loc[index, "quantity"])
    if quantity > old_quantity:
        raise ValueError("Cannot reduce below zero.")
    avg_cost = float(portfolio.loc[index, "avg_cost"])
    currency = str(portfolio.loc[index, "currency"])
    realized_pl = calculate_realized_pl(quantity, avg_cost, price, fees)
    portfolio.loc[index, "quantity"] = old_quantity - quantity
    portfolio.loc[index, "updated_at"] = _now()
    portfolio = portfolio[portfolio["quantity"] > 0].copy()
    save_portfolio(portfolio)
    record_transaction("SELL_REDUCE", symbol, quantity, price, currency, fees, realized_pl, note)
    return load_portfolio()


def close_holding(symbol, price, fees=0, note="") -> pd.DataFrame:
    symbol = normalize_symbol(symbol)
    portfolio = load_portfolio()
    mask = portfolio["symbol"] == symbol
    if not mask.any():
        raise ValueError("Position not found.")
    quantity = float(portfolio.loc[mask, "quantity"].iloc[0])
    return reduce_holding(symbol, quantity, price, fees, note or "Manual close position")


def delete_holding(symbol) -> pd.DataFrame:
    backup_portfolio()
    symbol = normalize_symbol(symbol)
    portfolio = load_portfolio()
    portfolio = portfolio[portfolio["symbol"] != symbol].copy()
    save_portfolio(portfolio)
    record_transaction("ADJUSTMENT", symbol, 0, 0, "", 0, 0, "Manual delete holding")
    return load_portfolio()


def record_transaction(action_type, symbol, quantity, price, currency="", fees=0, realized_pl=0, note="") -> None:
    ledger = load_transactions()
    row = {
        "timestamp": _now(),
        "action_type": action_type,
        "symbol": normalize_symbol(symbol),
        "quantity": float(quantity or 0),
        "price": float(price or 0),
        "currency": currency,
        "fees": float(fees or 0),
        "realized_pl": float(realized_pl or 0),
        "note": note,
    }
    ledger = pd.concat([ledger, pd.DataFrame([row])], ignore_index=True)
    ledger[TRANSACTION_COLUMNS].to_csv(TRANSACTIONS_PATH, index=False)


def load_transactions() -> pd.DataFrame:
    DATA_DIR.mkdir(exist_ok=True)
    if not TRANSACTIONS_PATH.exists():
        pd.DataFrame(columns=TRANSACTION_COLUMNS).to_csv(TRANSACTIONS_PATH, index=False)
    ledger = pd.read_csv(TRANSACTIONS_PATH)
    for column in TRANSACTION_COLUMNS:
        if column not in ledger.columns:
            ledger[column] = "" if column in {"timestamp", "action_type", "symbol", "currency", "note"} else 0
    return ledger[TRANSACTION_COLUMNS]


def calculate_realized_pl(quantity, avg_cost, price, fees=0) -> float:
    return float(quantity or 0) * (float(price or 0) - float(avg_cost or 0)) - float(fees or 0)


def validate_portfolio_row(row: dict) -> list[str]:
    errors = []
    if not normalize_symbol(row.get("symbol", "")):
        errors.append("Missing symbol.")
    if float(row.get("quantity", 0) or 0) < 0:
        errors.append("Quantity cannot be negative.")
    if float(row.get("avg_cost", 0) or 0) < 0:
        errors.append("Average cost cannot be negative.")
    return errors


def normalize_symbol(symbol) -> str:
    return str(symbol or "").strip().upper()


def _normalize_portfolio(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    legacy = {"ticker": "symbol", "shares": "quantity", "average_cost": "avg_cost", "asset_type": "category", "notes": "note"}
    for old, new in legacy.items():
        if old in df.columns and new not in df.columns:
            df[new] = df[old]
    for column in PORTFOLIO_COLUMNS:
        if column not in df.columns:
            df[column] = "" if column not in {"quantity", "avg_cost", "target_weight"} else 0
    df["symbol"] = df["symbol"].map(normalize_symbol)
    for column in ["quantity", "avg_cost", "target_weight"]:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0.0)
    df["updated_at"] = df["updated_at"].fillna("").astype(str)
    return df[PORTFOLIO_COLUMNS]


def _infer_market(symbol: str) -> str:
    if symbol.endswith(".TW"):
        return "Taiwan"
    if symbol.endswith(".L"):
        return "LSE"
    if symbol.endswith("-USD") or symbol.endswith("USDT"):
        return "Crypto"
    return "US"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
