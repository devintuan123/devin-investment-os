import pandas as pd
import streamlit as st

from utils.data import load_watchlist, save_watchlist
from utils.market_data import get_prices


st.set_page_config(page_title="Watchlist", page_icon="DI", layout="wide")
st.title("Watchlist")
st.caption("Buy zones, trim zones, stop levels, priorities, and simple action signals.")


def to_float(value: object) -> float:
    try:
        if pd.isna(value) or value == "":
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def signal(row: pd.Series) -> str:
    price = to_float(row.get("current_price"))
    if not price:
        return "No price"
    if to_float(row.get("stop_level")) and price <= to_float(row.get("stop_level")):
        return "Risk Alert"
    if to_float(row.get("trim_zone")) and price >= to_float(row.get("trim_zone")):
        return "Trim"
    if to_float(row.get("buy_zone_low")) and to_float(row.get("buy_zone_high")) and to_float(row.get("buy_zone_low")) <= price <= to_float(row.get("buy_zone_high")):
        return "Buy Zone"
    return "Watch"


watchlist = load_watchlist()
if st.button("Refresh Prices", use_container_width=True):
    prices = get_prices(watchlist["ticker"].dropna().tolist()).set_index("ticker")
    for ticker in prices.index:
        watchlist.loc[watchlist["ticker"] == ticker, "current_price"] = prices.loc[ticker, "price"]

watchlist["signal"] = watchlist.apply(signal, axis=1)

filters = st.columns(2)
category = filters[0].selectbox("Category", ["All"] + sorted([str(x) for x in watchlist["category"].dropna().unique() if str(x)]))
signal_filter = filters[1].selectbox("Signal", ["All"] + sorted(watchlist["signal"].unique().tolist()))

view = watchlist.copy()
if category != "All":
    view = view[view["category"].astype(str) == category]
if signal_filter != "All":
    view = view[view["signal"] == signal_filter]
if "priority" in view:
    view = view.sort_values("priority", na_position="last")

edited = st.data_editor(view, use_container_width=True, hide_index=True, num_rows="dynamic")
if st.button("Save Watchlist", use_container_width=True):
    if "signal" in edited:
        edited = edited.drop(columns=["signal"])
    save_watchlist(edited)
    st.success("Watchlist saved.")
