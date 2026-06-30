import os

import streamlit as st
from dotenv import load_dotenv

from utils.telegram import send_telegram_message


st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

load_dotenv()

st.title("Settings")
st.caption("Configure Telegram through environment variables. Secrets are never displayed.")

st.subheader(".env Setup")
st.code(
    "TELEGRAM_BOT_TOKEN=your_bot_token\nTELEGRAM_CHAT_ID=your_chat_id",
    language="bash",
)

col1, col2 = st.columns(2)
col1.checkbox("TELEGRAM_BOT_TOKEN detected", value=bool(os.getenv("TELEGRAM_BOT_TOKEN")), disabled=True)
col2.checkbox("TELEGRAM_CHAT_ID detected", value=bool(os.getenv("TELEGRAM_CHAT_ID")), disabled=True)

message = st.text_area("Test Message", value="Devin Investment OS test message.")
if st.button("Send Test Telegram Message", use_container_width=True):
    if send_telegram_message(message):
        st.success("Telegram message sent.")
    else:
        st.error("Telegram message was not sent. Check .env values.")
