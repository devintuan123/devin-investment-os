import pandas as pd
import streamlit as st

from utils.tradingview import load_alerts


st.set_page_config(page_title="TradingView Alerts", page_icon="DI", layout="wide")
st.title("TradingView Alerts")
st.caption("Webhook alerts are logged only. No trades are executed.")

alerts = load_alerts()
if not alerts:
    st.info("No TradingView alerts received yet.")
else:
    df = pd.DataFrame(alerts)
    visible = [column for column in ["received_at", "ticker", "alert", "timeframe", "price", "action"] if column in df]
    st.dataframe(df[visible].sort_values("received_at", ascending=False), use_container_width=True, hide_index=True)
