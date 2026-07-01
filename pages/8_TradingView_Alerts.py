import pandas as pd
import streamlit as st

from utils.i18n import t
from utils.tradingview import load_alerts
from utils.ui import render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


st.set_page_config(page_title="TradingView Alerts", page_icon="DI", layout="wide")
render_sidebar_language_switch()
render_refresh_button()
render_sidebar_provider_status()

st.title(t("tv_alerts"))
st.caption(t("alerts_caption"))

alerts = load_alerts()
if not alerts:
    st.info(t("no_alerts"))
else:
    df = pd.DataFrame(alerts)
    visible = [column for column in ["received_at", "ticker", "alert", "timeframe", "price", "action"] if column in df]
    st.dataframe(df[visible].sort_values("received_at", ascending=False), use_container_width=True, hide_index=True)
