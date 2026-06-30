import pandas as pd
import streamlit as st

from utils.data import load_portfolio, save_portfolio


st.set_page_config(page_title="Portfolio", page_icon="💼", layout="wide")

st.title("Portfolio")
st.caption("Edit local holdings and save them back to CSV.")

portfolio = load_portfolio()

if "current_price" in portfolio.columns:
    portfolio["market_value"] = pd.to_numeric(portfolio["shares"], errors="coerce").fillna(0) * pd.to_numeric(
        portfolio["current_price"], errors="coerce"
    ).fillna(0)
    portfolio["unrealized_pl"] = (
        pd.to_numeric(portfolio["current_price"], errors="coerce").fillna(0)
        - pd.to_numeric(portfolio["average_cost"], errors="coerce").fillna(0)
    ) * pd.to_numeric(portfolio["shares"], errors="coerce").fillna(0)

edited = st.data_editor(portfolio, use_container_width=True, hide_index=True, num_rows="dynamic")

if st.button("Save Portfolio", use_container_width=True):
    save_portfolio(edited)
    st.success("Portfolio saved to data/portfolio.csv.")

if "market_value" in edited.columns:
    st.subheader("Summary")
    col1, col2 = st.columns(2)
    col1.metric("Market Value", f"${pd.to_numeric(edited['market_value'], errors='coerce').fillna(0).sum():,.2f}")
    col2.metric("Unrealized P/L", f"${pd.to_numeric(edited['unrealized_pl'], errors='coerce').fillna(0).sum():,.2f}")
