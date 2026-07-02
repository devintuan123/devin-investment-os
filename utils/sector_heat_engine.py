from __future__ import annotations

from pathlib import Path

import pandas as pd

from utils.cache import cache_sector_heat
from utils.market_data import get_batch_history, get_history


ROOT_DIR = Path(__file__).resolve().parents[1]
THEME_UNIVERSE_PATH = ROOT_DIR / "data" / "theme_universe.csv"


def load_theme_universe() -> pd.DataFrame:
    if not THEME_UNIVERSE_PATH.exists():
        return pd.DataFrame(columns=["theme", "theme_zh", "market", "symbol", "name", "category", "proxy_type", "note"])
    return pd.read_csv(THEME_UNIVERSE_PATH, encoding="utf-8")


def quick_theme_universe(universe: pd.DataFrame | None = None, max_per_theme: int = 3, max_total: int = 60) -> pd.DataFrame:
    universe = load_theme_universe() if universe is None else universe.copy()
    if universe.empty:
        return universe
    return universe.groupby(["market", "theme"], dropna=False).head(max_per_theme).head(max_total).reset_index(drop=True)


def fetch_theme_prices(universe: pd.DataFrame | None = None, full_scan: bool = False) -> pd.DataFrame:
    universe = load_theme_universe() if universe is None else universe.copy()
    if not full_scan:
        universe = quick_theme_universe(universe)
    histories = get_batch_history(universe["symbol"].astype(str).tolist(), period="6mo") if not universe.empty else {}
    rows = []
    for _, item in universe.iterrows():
        symbol = str(item["symbol"])
        history, warning = histories.get(symbol) or get_history(symbol, period="6mo")
        rows.append({**item.to_dict(), **calculate_symbol_momentum(symbol, history), "warning": warning})
    return pd.DataFrame(rows)


def calculate_symbol_momentum(symbol: str, history: pd.DataFrame) -> dict:
    close = history["Close"].dropna() if "Close" in history else pd.Series(dtype=float)
    latest = float(close.iloc[-1]) if not close.empty else 0.0
    ma20 = _moving_average(close, 20)
    ma60 = _moving_average(close, 60)
    return {
        "latest_price": latest,
        "return_1d": _return(close, 1),
        "return_5d": _return(close, 5),
        "return_20d": _return(close, 20),
        "distance_ma20": _distance(latest, ma20),
        "distance_ma60": _distance(latest, ma60),
        "volume_trend": 0.0,
        "positive_5d": _return(close, 5) > 0,
        "positive_20d": _return(close, 20) > 0,
    }


def calculate_theme_heat_score(rows: pd.DataFrame | None = None, full_scan: bool = False) -> pd.DataFrame:
    symbol_rows = _cached_symbol_rows(full_scan) if rows is None else rows.copy()
    return _calculate_theme_heat_score_from_rows(symbol_rows)


@cache_sector_heat
def _cached_symbol_rows(full_scan: bool = False) -> pd.DataFrame:
    return fetch_theme_prices(full_scan=full_scan)


def _calculate_theme_heat_score_from_rows(symbol_rows: pd.DataFrame) -> pd.DataFrame:
    if symbol_rows.empty:
        return pd.DataFrame()
    grouped = []
    for (market, theme, theme_zh), group in symbol_rows.groupby(["market", "theme", "theme_zh"], dropna=False):
        return_5d = float(group["return_5d"].mean())
        return_20d = float(group["return_20d"].mean())
        breadth_5d = float(group["positive_5d"].mean() * 100)
        breadth_20d = float(group["positive_20d"].mean() * 100)
        ma_strength = float(group["distance_ma20"].mean())
        heat_score = max(0, min(100, round(50 + return_5d * 4 + return_20d * 1.5 + ma_strength + (breadth_5d - 50) * 0.3)))
        rotation_score = max(0, min(100, round(50 + return_5d * 5 + (breadth_5d - breadth_20d) * 0.4)))
        grouped.append(
            {
                "market": market,
                "theme": theme,
                "theme_zh": theme_zh,
                "heat_score": heat_score,
                "rotation_score": rotation_score,
                "heat_label": classify_theme_heat(heat_score),
                "rotation_label": classify_rotation_score(rotation_score),
                "return_5d": return_5d,
                "return_20d": return_20d,
                "breadth": breadth_5d,
                "symbol_count": len(group),
                "warning": "Proxy-based heat only, not exact fund flows or trading advice.",
            }
        )
    result = pd.DataFrame(grouped).sort_values(["heat_score", "rotation_score"], ascending=False)
    result["last_updated"] = pd.Timestamp.utcnow().isoformat()
    return result


def calculate_rotation_score(rows: pd.DataFrame | None = None, full_scan: bool = False) -> pd.DataFrame:
    return calculate_theme_heat_score(rows, full_scan=full_scan)


def classify_theme_heat(score: float) -> str:
    if score >= 75:
        return "Hot / Extended"
    if score >= 60:
        return "Heating Up"
    if score <= 40:
        return "Cooling"
    return "Neutral"


def classify_rotation_score(score: float) -> str:
    if score >= 60:
        return "Rotation In"
    if score <= 40:
        return "Rotation Out"
    return "Neutral"


def get_top_hot_themes(limit: int = 3, full_scan: bool = False) -> pd.DataFrame:
    return calculate_theme_heat_score(full_scan=full_scan).head(limit)


def get_cooling_themes(limit: int = 3, full_scan: bool = False) -> pd.DataFrame:
    scores = calculate_theme_heat_score(full_scan=full_scan)
    return scores[scores["heat_label"] == "Cooling"].head(limit)


def get_candidate_symbols_by_theme(limit: int = 20, full_scan: bool = False) -> pd.DataFrame:
    rows = fetch_theme_prices(full_scan=full_scan)
    if rows.empty:
        return rows
    rows["candidate_label"] = rows.apply(lambda row: "Watchlist Candidate" if row["return_5d"] > 0 and row["distance_ma20"] > 0 else "Avoid chasing", axis=1)
    return rows.sort_values(["return_5d", "return_20d"], ascending=False).head(limit)


def _return(close: pd.Series, periods: int) -> float:
    if len(close) <= periods:
        return 0.0
    previous = float(close.iloc[-periods - 1])
    latest = float(close.iloc[-1])
    return ((latest - previous) / previous * 100) if previous else 0.0


def _moving_average(close: pd.Series, window: int) -> float:
    if close.empty:
        return 0.0
    return float(close.tail(min(window, len(close))).mean())


def _distance(latest: float, average: float) -> float:
    return ((latest - average) / average * 100) if average else 0.0
