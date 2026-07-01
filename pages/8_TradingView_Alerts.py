import pandas as pd
import streamlit as st

from utils.i18n import t
from utils.table_i18n import translate_dataframe
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
    st.dataframe(translate_dataframe(df[visible].sort_values("received_at", ascending=False), lang), use_container_width=True, hide_index=True)
