import pandas as pd
import streamlit as st

from utils.i18n import t
from utils.interactive_table import render_interactive_table
from utils.tradingview import load_alerts
from utils.ui import get_current_lang, render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


st.set_page_config(page_title="TradingView Alerts", page_icon="DI", layout="wide")
render_sidebar_language_switch()
render_refresh_button()
render_sidebar_provider_status()

st.title(t("tv_alerts"))
st.caption(t("alerts_caption"))
lang = get_current_lang()

alerts = load_alerts()
if not alerts:
    st.info(t("no_alerts"))
else:
    df = pd.DataFrame(alerts)
    visible = [column for column in ["received_at", "ticker", "alert", "timeframe", "price", "action"] if column in df]
    render_interactive_table(df[visible].sort_values("received_at", ascending=False), table_key="tradingview_alerts", lang=lang)
