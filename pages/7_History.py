import pandas as pd
import plotly.express as px
import streamlit as st

from utils.i18n import t
from utils.snapshots import load_snapshots
from utils.ui import render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


st.set_page_config(page_title="History", page_icon="DI", layout="wide")
render_sidebar_language_switch()
render_refresh_button()
render_sidebar_provider_status()

st.title(t("history"))
st.caption(t("history_caption"))

snapshots = load_snapshots()
if not snapshots:
    st.info(t("no_snapshots"))
else:
    rows = [{"timestamp": item.get("timestamp"), "market_score": item.get("market_score"), "regime": item.get("regime"), "alerts": len(item.get("alerts", []))} for item in snapshots]
    df = pd.DataFrame(rows)
    st.plotly_chart(px.line(df, x="timestamp", y="market_score", title=t("market_score")), use_container_width=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.subheader(t("latest_alerts"))
    for alert in snapshots[-1].get("alerts", []):
        st.write(f"- {alert}")
