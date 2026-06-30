import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data import load_portfolio, save_portfolio
from utils.market_data import get_prices
from utils.portfolio_risk import holding_action, portfolio_summary


st.set_page_config(page_title="Portfolio", page_icon="DI", layout="wide")
st.title("Portfolio")
st.caption("Editable holdings, valuation, allocation, and high-beta exposure.")


def enrich_portfolio(df: pd.DataFrame, refresh_prices: bool = False) -> pd.DataFrame:
    df = df.copy()
    if refresh_prices:
        prices = get_prices(df["ticker"].dropna().tolist()).set_index("ticker")
        for ticker in prices.index:
            df.loc[df["ticker"] == ticker, "current_price"] = prices.loc[ticker, "price"]

    shares = pd.to_numeric(df.get("shares"), errors="coerce").fillna(0)
    average_cost = pd.to_numeric(df.get("average_cost"), errors="coerce").fillna(0)
    current_price = pd.to_numeric(df.get("current_price"), errors="coerce").fillna(0)
    df["market_value"] = shares * current_price
    df["unrealized_pnl"] = (current_price - average_cost) * shares
    cost_basis = shares * average_cost
    df["unrealized_pnl_pct"] = (df["unrealized_pnl"] / cost_basis.replace(0, pd.NA) * 100).fillna(0)
    df["action_signal"] = df.apply(holding_action, axis=1)
    return df


portfolio = load_portfolio()
refresh = st.button("Refresh Prices", use_container_width=True)
portfolio = enrich_portfolio(portfolio, refresh)

col1, col2, col3 = st.columns(3)
col1.metric("Total Market Value", f"{portfolio['market_value'].sum():,.2f}")
col2.metric("Unrealized P/L", f"{portfolio['unrealized_pnl'].sum():,.2f}")
risk = portfolio_summary(portfolio)
col3.metric("Portfolio Risk", f"{risk['risk_score']}/100")

metric_cols = st.columns(4)
metric_cols[0].metric("High-Beta Exposure", f"{risk['high_beta_exposure']:.1f}%")
metric_cols[1].metric("Hedge Exposure", f"{risk['hedge_allocation']:.1f}%")
metric_cols[2].metric("Core Allocation", f"{risk['core_allocation']:.1f}%")
metric_cols[3].metric("Single Name Max", f"{risk['single_name_concentration']:.1f}%")

st.subheader("Suggested Risk Actions")
for item in risk["suggestions"]:
    st.write(f"- {item}")

edited = st.data_editor(portfolio, use_container_width=True, hide_index=True, num_rows="dynamic")
if st.button("Save Portfolio", use_container_width=True):
    save_portfolio(edited)
    st.success("Portfolio saved.")

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    allocation = portfolio.groupby("asset_type", dropna=False)["market_value"].sum().reset_index()
    st.plotly_chart(px.pie(allocation, names="asset_type", values="market_value", title="Allocation by Asset Type"), use_container_width=True)
with chart_col2:
    currency = portfolio.groupby("currency", dropna=False)["market_value"].sum().reset_index()
    st.plotly_chart(px.pie(currency, names="currency", values="market_value", title="Allocation by Currency"), use_container_width=True)
