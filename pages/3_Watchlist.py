import pandas as pd
import streamlit as st

from utils.data import load_watchlist, save_watchlist


st.set_page_config(page_title="Watchlist", page_icon="👀", layout="wide")

st.title("Watchlist")
st.caption("Track buy, sell, and risk zones with optional current prices.")

watchlist = load_watchlist()


def signal_for_row(row: pd.Series) -> str:
    if "current_price" not in row or pd.isna(row.get("current_price")) or row.get("current_price") == "":
        return "No price"

    current_price = _to_float(row.get("current_price"))
    buy_low = _to_float(row.get("buy_zone_low"))
    buy_high = _to_float(row.get("buy_zone_high"))
    sell_zone = _to_float(row.get("sell_zone"))
    stop_level = _to_float(row.get("stop_level"))

    if stop_level and current_price <= stop_level:
        return "Risk Alert"
    if sell_zone and current_price >= sell_zone:
        return "Sell / Trim Zone"
    if buy_low and buy_high and buy_low <= current_price <= buy_high:
        return "Buy Zone"
    return "Watching"


def _to_float(value: object) -> float:
    try:
        if pd.isna(value) or value == "":
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


watchlist["signal"] = watchlist.apply(signal_for_row, axis=1)
edited = st.data_editor(watchlist, use_container_width=True, hide_index=True, num_rows="dynamic")

if st.button("Save Watchlist", use_container_width=True):
    if "signal" in edited.columns:
        edited = edited.drop(columns=["signal"])
    save_watchlist(edited)
    st.success("Watchlist saved to data/watchlist.csv.")
