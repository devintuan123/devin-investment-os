from __future__ import annotations

import pandas as pd

from utils.data import load_portfolio, load_watchlist
from utils.portfolio_risk import portfolio_summary
from utils.signals import watchlist_signal


def generate_watchlist_alerts(watchlist: pd.DataFrame | None = None) -> list[str]:
    data = load_watchlist() if watchlist is None else watchlist.copy()
    if data.empty:
        return []
    data["signal"] = data.apply(watchlist_signal, axis=1)
    alerts = []
    for _, row in data[data["signal"].isin(["Buy Zone", "Trim", "Risk Alert"])].iterrows():
        alerts.append(f"{row['ticker']}: {row['signal']} at {row.get('current_price', 'N/A')}")
    return alerts


def generate_risk_alerts(portfolio: pd.DataFrame | None = None) -> list[str]:
    data = load_portfolio() if portfolio is None else portfolio.copy()
    if data.empty:
        return []
    summary = portfolio_summary(data)
    alerts = []
    if summary["risk_score"] >= 70:
        alerts.append(f"Portfolio Risk Score elevated: {summary['risk_score']}/100")
    if summary["high_beta_exposure"] > 25:
        alerts.append(f"High-beta exposure elevated: {summary['high_beta_exposure']}%")
    if summary["single_name_concentration"] > 30:
        alerts.append(f"Single-name concentration elevated: {summary['single_name_concentration']}%")
    return alerts


def generate_portfolio_alerts(portfolio: pd.DataFrame | None = None) -> list[str]:
    data = load_portfolio() if portfolio is None else portfolio.copy()
    if data.empty:
        return []
    summary = portfolio_summary(data)
    return summary["suggestions"]


def deduplicate_alerts(alerts: list[str]) -> list[str]:
    return list(dict.fromkeys(alert for alert in alerts if alert))
