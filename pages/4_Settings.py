import os

import streamlit as st
from dotenv import load_dotenv

from utils.telegram import send_telegram_message


st.set_page_config(page_title="Settings", page_icon="DI", layout="wide")
load_dotenv()

st.title("Settings")
st.caption("Environment-backed settings. Secret values are never displayed.")

st.subheader("Telegram")
st.code("TELEGRAM_BOT_TOKEN=\nTELEGRAM_CHAT_ID=", language="bash")

col1, col2 = st.columns(2)
col1.checkbox("Bot token detected", value=bool(os.getenv("TELEGRAM_BOT_TOKEN")), disabled=True)
col2.checkbox("Chat ID detected", value=bool(os.getenv("TELEGRAM_CHAT_ID")), disabled=True)

message = st.text_area("Test message", value="Devin Investment OS test message.")
if st.button("Send Test Telegram Message", use_container_width=True):
    st.success("Sent.") if send_telegram_message(message) else st.warning("Skipped. Check .env configuration.")

st.subheader("Security Notes")
st.write("- Keep `.env` local to the server.")
st.write("- Do not commit Telegram tokens, passwords, SSH keys, or account numbers.")
st.write("- Data files are local CSV files and can be edited from the app.")
