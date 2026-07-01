import pandas as pd
import plotly.express as px
import streamlit as st

from utils.i18n import t, translate_action_label, translate_warning
from utils.portfolio_engine import (
    calculate_cash_needed_for_rebalance,
    calculate_position_values,
    calculate_total_value,
    load_portfolio,
    portfolio_health_score,
    save_portfolio,
)
from utils.ui import render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


st.set_page_config(page_title="Portfolio", page_icon="DI", layout="wide")
render_sidebar_language_switch()
render_refresh_button()
render_sidebar_provider_status()

st.title(t("portfolio"))
st.caption(t("portfolio_page_caption"))

portfolio = load_portfolio()
positions = calculate_position_values(portfolio)
health = portfolio_health_score(portfolio)
cash = st.number_input(t("cash"), min_value=0.0, value=0.0, step=100.0)
total_value = calculate_total_value(positions) + cash

cols = st.columns(3)
cols[0].metric(t("total_portfolio_value"), f"{total_value:,.2f}")
cols[1].metric(t("cash"), f"{cash:,.2f}")
cols[2].metric(t("portfolio_health"), f"{health['score']}/100")

st.subheader(t("current_allocation"))
if positions.empty:
    st.info(t("no_data"))
else:
    allocation = positions.groupby("category", dropna=False)["market_value"].sum().reset_index()
    target = positions.groupby("category", dropna=False)["target_weight"].sum().reset_index()
    chart_cols = st.columns(2)
    chart_cols[0].plotly_chart(px.pie(allocation, names="category", values="market_value", title=t("current_allocation")), use_container_width=True)
    chart_cols[1].plotly_chart(px.bar(target, x="category", y="target_weight", title=t("target_allocation")), use_container_width=True)

st.subheader(t("drift"))
if not positions.empty:
    drift = positions[["symbol", "category", "current_weight", "target_weight", "drift", "drift_label", "action_suggestion"]].copy()
    drift["action_suggestion"] = drift["action_suggestion"].map(translate_action_label)
    st.dataframe(drift, use_container_width=True, hide_index=True)

st.subheader(t("positions"))
if positions.empty:
    st.info(t("no_holdings"))
else:
    columns = ["symbol", "name", "category", "market", "currency", "quantity", "avg_cost", "latest_price", "market_value", "current_weight", "target_weight", "drift", "unrealized_pl", "action_suggestion", "freshness_status", "warning"]
    view = positions[[column for column in columns if column in positions]].copy()
    view["action_suggestion"] = view["action_suggestion"].map(translate_action_label)
    st.dataframe(view, use_container_width=True, hide_index=True)

st.subheader(t("suggested_actions"))
for warning in health["warnings"]:
    st.write(f"- {warning}")
for _, row in positions.head(8).iterrows():
    st.write(f"- {row['symbol']}: {translate_action_label(row['action_suggestion'])}")

st.subheader(t("target_allocation"))
st.dataframe(calculate_cash_needed_for_rebalance(portfolio), use_container_width=True, hide_index=True)

edited = st.data_editor(portfolio, use_container_width=True, hide_index=True, num_rows="dynamic")
if st.button(t("save_portfolio"), use_container_width=True):
    save_portfolio(edited)
    st.success(t("portfolio_saved"))

for warning in positions.get("warning", pd.Series(dtype=str)).dropna().astype(str).unique()[:5]:
    if warning:
        st.warning(translate_warning(warning))
