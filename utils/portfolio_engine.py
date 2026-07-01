from __future__ import annotations

from pathlib import Path

import pandas as pd

from utils.market_data import safe_fetch_with_fallback


ROOT_DIR = Path(__file__).resolve().parents[1]
PORTFOLIO_PATH = ROOT_DIR / "data" / "portfolio.csv"
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


def load_portfolio() -> pd.DataFrame:
    if not PORTFOLIO_PATH.exists():
        PORTFOLIO_PATH.parent.mkdir(exist_ok=True)
        pd.DataFrame(columns=PORTFOLIO_COLUMNS).to_csv(PORTFOLIO_PATH, index=False)
    return normalize_portfolio(pd.read_csv(PORTFOLIO_PATH))


def save_portfolio(df: pd.DataFrame) -> None:
    clean = normalize_portfolio(df)
    clean[PORTFOLIO_COLUMNS].to_csv(PORTFOLIO_PATH, index=False)


def normalize_portfolio(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    legacy_map = {
        "ticker": "symbol",
        "asset_type": "category",
        "shares": "quantity",
        "average_cost": "avg_cost",
        "notes": "note",
    }
    for old, new in legacy_map.items():
        if old in df.columns and new not in df.columns:
            df[new] = df[old]
    for column in PORTFOLIO_COLUMNS:
        if column not in df.columns:
            df[column] = "" if column not in {"quantity", "avg_cost", "target_weight"} else 0
    df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0.0)
    df["avg_cost"] = pd.to_numeric(df["avg_cost"], errors="coerce").fillna(0.0)
    df["target_weight"] = pd.to_numeric(df["target_weight"], errors="coerce").fillna(0.0)
    return df[PORTFOLIO_COLUMNS]


def fetch_portfolio_prices(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for symbol in normalize_portfolio(df)["symbol"]:
        if not symbol:
            continue
        quote = safe_fetch_with_fallback(symbol)
        rows.append(
            {
                "symbol": symbol,
                "latest_price": quote.get("price", 0.0),
                "provider": quote.get("provider_label") or quote.get("source"),
                "fetch_timestamp": quote.get("fetch_timestamp"),
                "quote_timestamp": quote.get("quote_timestamp"),
                "freshness_status": quote.get("freshness_status"),
                "confidence": quote.get("confidence"),
                "warning": quote.get("provider_warning") or quote.get("warning"),
            }
        )
    return pd.DataFrame(rows)


def calculate_position_values(df: pd.DataFrame) -> pd.DataFrame:
    portfolio = normalize_portfolio(df)
    prices = fetch_portfolio_prices(portfolio)
    if prices.empty:
        portfolio["latest_price"] = 0.0
    else:
        portfolio = portfolio.merge(prices, on="symbol", how="left")
    portfolio["latest_price"] = pd.to_numeric(portfolio["latest_price"], errors="coerce").fillna(0.0)
    portfolio["market_value"] = portfolio["quantity"] * portfolio["latest_price"]
    portfolio["cost_basis"] = portfolio["quantity"] * portfolio["avg_cost"]
    portfolio["unrealized_pl"] = portfolio["market_value"] - portfolio["cost_basis"]
    cost_basis = pd.to_numeric(portfolio["cost_basis"], errors="coerce")
    portfolio["unrealized_pl_pct"] = (portfolio["unrealized_pl"] / cost_basis.where(cost_basis != 0) * 100).fillna(0.0)
    total_value = calculate_total_value(portfolio)
    portfolio["current_weight"] = (
        portfolio["market_value"] / total_value * 100 if total_value else 0.0
    )
    portfolio["drift"] = portfolio["current_weight"] - portfolio["target_weight"]
    portfolio["drift_label"] = portfolio["drift"].apply(classify_drift)
    portfolio["action_suggestion"] = portfolio.apply(_action_suggestion, axis=1)
    return portfolio


def calculate_total_value(df: pd.DataFrame) -> float:
    if "market_value" not in df:
        df = calculate_position_values(df)
    return float(pd.to_numeric(df.get("market_value"), errors="coerce").fillna(0.0).sum())


def calculate_current_weights(df: pd.DataFrame) -> pd.DataFrame:
    positions = calculate_position_values(df)
    return positions[["symbol", "category", "market_value", "current_weight", "target_weight"]]


def calculate_target_drift(df: pd.DataFrame) -> pd.DataFrame:
    positions = calculate_position_values(df)
    return positions[["symbol", "category", "current_weight", "target_weight", "drift", "drift_label"]]


def classify_drift(value: float) -> str:
    if pd.isna(value):
        return "No target"
    if value <= -2:
        return "Underweight"
    if value >= 2:
        return "Overweight"
    return "On Target"


def allocation_by_category(df: pd.DataFrame) -> pd.DataFrame:
    positions = calculate_position_values(df)
    return _allocation_by(positions, "category")


def allocation_by_market(df: pd.DataFrame) -> pd.DataFrame:
    positions = calculate_position_values(df)
    return _allocation_by(positions, "market")


def allocation_by_currency(df: pd.DataFrame) -> pd.DataFrame:
    positions = calculate_position_values(df)
    return _allocation_by(positions, "currency")


def target_allocation_comparison(df: pd.DataFrame) -> pd.DataFrame:
    positions = calculate_position_values(df)
    return positions[["symbol", "category", "market_value", "current_weight", "target_weight", "drift", "drift_label", "action_suggestion"]]


def cash_deployment_suggestion(df: pd.DataFrame) -> str:
    positions = calculate_position_values(df)
    if positions.empty:
        return "Watch only"
    if float(positions["drift"].min()) <= -5:
        return "Add gradually"
    return "Hold"


def exposure_warnings(df: pd.DataFrame) -> list[str]:
    positions = calculate_position_values(df)
    warnings = ["Manual portfolio records may differ from broker records."]
    if positions.empty:
        return warnings
    single_stock = positions[(positions["category"].astype(str).str.lower() == "stock") & (positions["current_weight"] > 15)]
    for _, row in single_stock.iterrows():
        warnings.append(f"{row['symbol']} single-stock exposure is elevated.")
    satellite = positions[(positions["category"].astype(str).str.contains("Crypto|Stock", case=False, na=False)) & (positions["current_weight"] > 20)]
    for _, row in satellite.iterrows():
        warnings.append(f"{row['symbol']} high-volatility satellite exposure should be monitored.")
    return warnings


def calculate_cash_needed_for_rebalance(df: pd.DataFrame) -> pd.DataFrame:
    positions = calculate_position_values(df)
    total_value = calculate_total_value(positions)
    positions["target_value"] = total_value * positions["target_weight"] / 100
    positions["cash_needed"] = positions["target_value"] - positions["market_value"]
    return positions[["symbol", "target_value", "market_value", "cash_needed"]]


def portfolio_health_score(df: pd.DataFrame) -> dict:
    positions = calculate_position_values(df)
    if positions.empty:
        return {"score": 0, "summary": "No data", "warnings": ["No portfolio data."]}
    missing = int((positions["latest_price"] <= 0).sum())
    average_abs_drift = float(positions["drift"].abs().mean())
    score = max(0, min(100, round(90 - average_abs_drift * 2 - missing * 10)))
    warnings = []
    if missing:
        warnings.append("Some positions have missing price data.")
    if average_abs_drift > 5:
        warnings.append("Portfolio drift is elevated.")
    if not warnings:
        warnings.append("Portfolio drift is manageable.")
    return {"score": score, "summary": f"Average drift {average_abs_drift:.1f}%", "warnings": warnings}


def _action_suggestion(row: pd.Series) -> str:
    if float(row.get("latest_price", 0) or 0) <= 0:
        return "Missing data"
    if float(row.get("quantity", 0) or 0) == 0:
        return "Watch only"
    if float(row.get("target_weight", 0) or 0) == 0:
        return "Need target weight"
    drift = float(row.get("drift", 0) or 0)
    if drift <= -2:
        return "Add gradually"
    if drift >= 3:
        return "Trim later"
    return "Hold"


def _allocation_by(positions: pd.DataFrame, column: str) -> pd.DataFrame:
    if positions.empty or column not in positions:
        return pd.DataFrame(columns=[column, "market_value", "current_weight"])
    total = calculate_total_value(positions)
    result = positions.groupby(column, dropna=False)["market_value"].sum().reset_index()
    result["current_weight"] = result["market_value"] / total * 100 if total else 0.0
    return result
