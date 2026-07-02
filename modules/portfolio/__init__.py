from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from modules.shared.tables import render_interactive_table
from utils.i18n import t, translate_action_label, translate_warning
from utils.portfolio_engine import (
    allocation_by_category,
    allocation_by_currency,
    allocation_by_market,
    calculate_cash_needed_for_rebalance,
    calculate_position_values,
    calculate_total_value,
    exposure_warnings,
    portfolio_health_score,
    target_allocation_comparison,
)
from utils.portfolio_store import (
    add_holding,
    clear_portfolio,
    close_holding,
    load_portfolio,
    load_transactions,
    reduce_holding,
    save_portfolio,
)
from utils.table_i18n import translated_column_config


def render(lang: str) -> None:
    st.title(t("portfolio"))
    st.caption(t("portfolio_page_caption"))
    st.warning(t("manual_portfolio_warning"))

    portfolio = load_portfolio()
    positions = calculate_position_values(portfolio)
    health = portfolio_health_score(portfolio)
    cash = st.number_input(t("cash"), min_value=0.0, value=0.0, step=100.0)
    total_value = calculate_total_value(positions) + cash

    cols = st.columns(3)
    cols[0].metric(t("total_portfolio_value"), f"{total_value:,.2f}")
    cols[1].metric(t("cash"), f"{cash:,.2f}")
    cols[2].metric(t("portfolio_health"), f"{health['score']}/100")

    tabs = st.tabs(
        [
            t("overview"),
            t("add_holding"),
            f"{t('reduce_position')} / {t('close_position')}",
            t("target_allocation_tab"),
            t("transaction_ledger"),
            t("danger_zone"),
        ]
    )

    with tabs[0]:
        _render_overview(portfolio, positions, health, lang)
    with tabs[1]:
        _render_add_holding(lang)
    with tabs[2]:
        _render_reduce_close(portfolio)
    with tabs[3]:
        _render_target_allocation(portfolio, lang)
    with tabs[4]:
        render_interactive_table(load_transactions(), table_key="portfolio_transactions", lang=lang)
    with tabs[5]:
        _render_danger_zone()


def _render_overview(portfolio: pd.DataFrame, positions: pd.DataFrame, health: dict, lang: str) -> None:
    st.subheader(t("current_allocation"))
    if positions.empty:
        st.info(t("no_holdings"))
    else:
        allocation = allocation_by_category(portfolio)
        market_allocation = allocation_by_market(portfolio)
        currency_allocation = allocation_by_currency(portfolio)
        chart_cols = st.columns(3)
        chart_cols[0].plotly_chart(px.pie(allocation, names="category", values="market_value", title=t("category")), use_container_width=True)
        chart_cols[1].plotly_chart(px.bar(market_allocation, x="market", y="current_weight", title=t("market")), use_container_width=True)
        chart_cols[2].plotly_chart(px.bar(currency_allocation, x="currency", y="current_weight", title=t("currency")), use_container_width=True)

        columns = ["symbol", "name", "category", "market", "currency", "quantity", "avg_cost", "latest_price", "market_value", "current_weight", "target_weight", "drift", "unrealized_pl", "action_suggestion", "freshness_status", "warning"]
        view = positions[[column for column in columns if column in positions]].copy()
        render_interactive_table(view, table_key="portfolio_positions", lang=lang)

    st.subheader(t("suggested_actions"))
    for warning in [*health["warnings"], *exposure_warnings(portfolio)]:
        st.warning(translate_warning(warning))
    if not positions.empty:
        for _, row in positions.head(8).iterrows():
            st.write(f"- {row['symbol']}: {translate_action_label(row['action_suggestion'])}")


def _render_add_holding(lang: str) -> None:
    with st.form("add_holding_form"):
        symbol = st.text_input(t("symbol"))
        quantity = st.number_input(t("quantity"), min_value=0.0, step=1.0)
        price = st.number_input(t("price"), min_value=0.0, step=1.0)
        currency = st.text_input(t("currency"), value="USD")
        category = st.selectbox(t("category"), ["ETF", "Stock", "Crypto", "Gold", "Cash"])
        account = st.text_input(t("account"))
        note = st.text_input(t("note"))
        submitted = st.form_submit_button(t("add_holding"))
    if submitted:
        try:
            add_holding(symbol, quantity, price, currency=currency, category=category, account=account, note=note)
            st.success(t("holding_added"))
            st.rerun()
        except ValueError as error:
            st.error(str(error))


def _render_reduce_close(portfolio: pd.DataFrame) -> None:
    symbols = portfolio["symbol"].dropna().astype(str).tolist() if "symbol" in portfolio else []
    if not symbols:
        st.info(t("no_holdings"))
        return
    symbol = st.selectbox(t("symbol"), symbols)
    quantity = st.number_input(t("quantity"), min_value=0.0, step=1.0)
    price = st.number_input(t("sell_price"), min_value=0.0, step=1.0)
    fees = st.number_input(t("fees"), min_value=0.0, step=1.0)
    note = st.text_input(t("note"), key="reduce_close_note")
    action_cols = st.columns(2)
    if action_cols[0].button(t("reduce_position"), use_container_width=True):
        try:
            reduce_holding(symbol, quantity, price, fees=fees, note=note)
            st.success(t("position_reduced"))
            st.rerun()
        except ValueError as error:
            st.error(str(error))
    if action_cols[1].button(t("close_position"), use_container_width=True):
        try:
            close_holding(symbol, price, fees=fees, note=note)
            st.success(t("position_closed"))
            st.rerun()
        except ValueError as error:
            st.error(str(error))


def _render_target_allocation(portfolio: pd.DataFrame, lang: str) -> None:
    st.subheader(t("target_allocation"))
    comparison = target_allocation_comparison(portfolio)
    render_interactive_table(comparison, table_key="portfolio_target_comparison", lang=lang)
    st.subheader(t("cash_deployment"))
    render_interactive_table(calculate_cash_needed_for_rebalance(portfolio), table_key="portfolio_cash_needed", lang=lang)
    st.subheader(t("positions"))
    # TABLE_ALLOWLIST_REASON: editable local CSV portfolio management form, not a display table.
    edited = st.data_editor(portfolio, use_container_width=True, hide_index=True, num_rows="dynamic", column_config=translated_column_config(portfolio, lang))
    if st.button(t("save_portfolio"), use_container_width=True):
        save_portfolio(edited)
        st.success(t("portfolio_saved"))
        st.rerun()


def _render_danger_zone() -> None:
    st.subheader(t("clear_holdings"))
    st.warning(t("manual_portfolio_warning"))
    confirmed = st.checkbox(t("confirm_clear_holdings"))
    if st.button(t("clear_holdings"), disabled=not confirmed, use_container_width=True):
        if clear_portfolio(confirm=confirmed):
            st.success(t("holdings_cleared"))
            st.rerun()
