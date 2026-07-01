import pandas as pd
import streamlit as st

from utils.data import load_watchlist, save_watchlist
from utils.market_data import get_prices
from utils.signals import distance_to_buy_zone, distance_to_trim_zone, watchlist_signal
from utils.watchlist_scoring import score_watchlist


st.set_page_config(page_title="Watchlist", page_icon="DI", layout="wide")
st.title("Watchlist")
st.caption("Buy zones, trim zones, stop levels, priorities, and simple action signals.")


watchlist = load_watchlist()
if st.button("Refresh Prices", use_container_width=True):
    prices = get_prices(watchlist["ticker"].dropna().tolist()).set_index("ticker")
    for ticker in prices.index:
        watchlist.loc[watchlist["ticker"] == ticker, "current_price"] = prices.loc[ticker, "price"]

watchlist["signal"] = watchlist.apply(watchlist_signal, axis=1)
watchlist["distance_to_buy_zone_pct"] = watchlist.apply(distance_to_buy_zone, axis=1)
watchlist["distance_to_trim_zone_pct"] = watchlist.apply(distance_to_trim_zone, axis=1)
watchlist["suggested_action"] = watchlist["signal"].map(
    {
        "Buy Zone": "Consider staged buy",
        "Trim": "Trim or stop chasing",
        "Risk Alert": "Review stop/risk control",
        "Watch": "Wait for planned zone",
        "No price": "Refresh price",
    }
).fillna("Watch")

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

st.subheader("Decision Scoring")
scores = pd.DataFrame(score_watchlist(watchlist["ticker"].dropna().astype(str).tolist()))
if scores.empty:
    st.info("No scoring data available.")
else:
    score_columns = [
        "ticker",
        "latest_price",
        "ma20",
        "ma60",
        "ma120",
        "distance_ma20_pct",
        "distance_ma60_pct",
        "drawdown_52w_pct",
        "trend_score",
        "pullback_score",
        "risk_label",
        "action_label",
    ]
    st.dataframe(scores[score_columns], use_container_width=True, hide_index=True)
