import pandas as pd
import streamlit as st

from utils.data import load_watchlist, save_watchlist
from utils.i18n import (
    get_lang,
    render_language_sidebar,
    render_refresh_button,
    t,
    translate_action_label,
    translate_risk_label,
)
from utils.market_data import get_prices
from utils.signals import distance_to_buy_zone, distance_to_trim_zone, watchlist_signal
from utils.watchlist_scoring import score_watchlist


st.set_page_config(page_title="Watchlist", page_icon="DI", layout="wide")
render_language_sidebar()
render_refresh_button()
st.title(t("watchlist"))
st.caption(
    "Buy zones, trim zones, stop levels, priorities, and simple action signals."
    if get_lang() == "en"
    else "買進區、減碼區、停損位、優先順序與簡易行動訊號。"
)


watchlist = load_watchlist()
if st.button(t("refresh_data"), use_container_width=True):
    st.cache_data.clear()
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
category = filters[0].selectbox(t("category"), [t("all")] + sorted([str(x) for x in watchlist["category"].dropna().unique() if str(x)]))
signal_filter = filters[1].selectbox(t("signal"), [t("all")] + sorted(watchlist["signal"].unique().tolist()))

view = watchlist.copy()
if category != t("all"):
    view = view[view["category"].astype(str) == category]
if signal_filter != t("all"):
    view = view[view["signal"] == signal_filter]
if "priority" in view:
    view = view.sort_values("priority", na_position="last")

edited = st.data_editor(view, use_container_width=True, hide_index=True, num_rows="dynamic")
if st.button(t("save_watchlist"), use_container_width=True):
    if "signal" in edited:
        edited = edited.drop(columns=["signal"])
    save_watchlist(edited)
    st.success(t("watchlist_saved"))

st.subheader(t("decision_scoring"))
scores = pd.DataFrame(score_watchlist(watchlist["ticker"].dropna().astype(str).tolist()))
if scores.empty:
    st.info(t("no_watchlist"))
else:
    tw_scores = scores[scores["ticker"].astype(str).str.endswith(".TW")]
    if not tw_scores.empty:
        st.warning(t("delayed_verify_broker_quote"))
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
        "freshness_status",
        "confidence",
    ]
    display_scores = scores[score_columns].copy()
    display_scores["action_label"] = display_scores["action_label"].map(translate_action_label)
    display_scores["risk_label"] = display_scores["risk_label"].map(translate_risk_label)
    if get_lang() == "zh":
        display_scores = display_scores.rename(
            columns={
                "ticker": t("ticker"),
                "latest_price": t("latest_price"),
                "ma20": t("ma20"),
                "ma60": t("ma60"),
                "ma120": t("ma120"),
                "drawdown_52w_pct": t("drawdown_52w_pct"),
                "trend_score": t("trend_score"),
                "pullback_score": t("pullback_score"),
                "risk_label": t("risk_label"),
                "action_label": t("action_label"),
                "freshness_status": t("freshness_status"),
                "confidence": t("confidence"),
            }
        )
    st.dataframe(display_scores, use_container_width=True, hide_index=True)
