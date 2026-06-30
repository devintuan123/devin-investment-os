import os

import streamlit as st
from dotenv import load_dotenv

from utils.config import is_configured, safety_status
from utils.telegram import send_telegram_message


st.set_page_config(page_title="Settings", page_icon="DI", layout="wide")
load_dotenv()

st.title("Settings")
st.caption("Environment-backed settings. Secret values are never displayed.")

st.subheader("API Configuration")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Binance", "Configured" if is_configured("BINANCE_API_KEY", "BINANCE_API_SECRET") else "Not configured")
col2.metric("Telegram", "Configured" if is_configured("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID") else "Not configured")
col3.metric("TradingView", "Configured" if is_configured("TRADINGVIEW_WEBHOOK_SECRET") else "Not configured")
col4.metric("IBKR", "Placeholder" if os.getenv("IBKR_ENABLED", "false").lower() == "true" else "Not configured")

st.subheader("Safety Status")
safety = safety_status()
safe_cols = st.columns(3)
safe_cols[0].checkbox("Trading disabled", value=safety["trading_disabled"], disabled=True)
safe_cols[1].checkbox("Withdrawals disabled", value=safety["withdrawals_disabled"], disabled=True)
safe_cols[2].checkbox("Futures disabled", value=safety["futures_disabled"], disabled=True)
for warning in safety["warnings"]:
    st.warning(warning)

st.subheader("Telegram Test")
st.code("TELEGRAM_BOT_TOKEN=\nTELEGRAM_CHAT_ID=", language="bash")

message = st.text_area("Test message", value="Devin Investment OS test message.")
if st.button("Send Test Telegram Message", use_container_width=True):
    st.success("Sent.") if send_telegram_message(message) else st.warning("Skipped. Check .env configuration.")

st.subheader("Security Notes")
st.write("- Keep `.env` local to the server.")
st.write("- Do not commit Telegram tokens, passwords, SSH keys, or account numbers.")
st.write("- Data files are local CSV files and can be edited from the app.")
