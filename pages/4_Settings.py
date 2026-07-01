import os

import streamlit as st
from dotenv import load_dotenv

from utils.config import is_configured, safety_status
from utils.binance_provider import account_snapshot_placeholder
from utils.ibkr_provider import (
    client_portal_portfolio_placeholder,
    flex_web_service_placeholder,
    market_data_snapshot_placeholder,
)
from utils.telegram import send_telegram_message


st.set_page_config(page_title="Settings", page_icon="DI", layout="wide")
load_dotenv()

st.title("Settings")
st.caption("Environment-backed settings. Secret values are never displayed.")

st.subheader("API Configuration")
providers = {
    "IBKR": os.getenv("IBKR_ENABLED", "false").lower() == "true",
    "Yuanta": os.getenv("YUANTA_ENABLED", "false").lower() == "true",
    "Binance": is_configured("BINANCE_API_KEY", "BINANCE_API_SECRET"),
    "OKX": is_configured("OKX_API_KEY", "OKX_API_SECRET", "OKX_API_PASSPHRASE"),
    "Bitget": is_configured("BITGET_API_KEY", "BITGET_API_SECRET", "BITGET_API_PASSPHRASE"),
    "TradingView": is_configured("TRADINGVIEW_WEBHOOK_SECRET"),
    "Telegram": is_configured("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"),
    "FRED": is_configured("FRED_API_KEY"),
    "yfinance fallback": True,
}
provider_rows = [st.columns(3), st.columns(3), st.columns(3)]
for index, (provider, configured) in enumerate(providers.items()):
    provider_rows[index // 3][index % 3].metric(provider, "Configured" if configured else "Not configured")

st.subheader("Safety Status")
safety = safety_status()
safe_cols = st.columns(5)
safe_cols[0].checkbox("Trading disabled", value=safety["trading_disabled"], disabled=True)
safe_cols[1].checkbox("Withdrawals disabled", value=safety["withdrawals_disabled"], disabled=True)
safe_cols[2].checkbox("Futures disabled", value=safety["futures_disabled"], disabled=True)
safe_cols[3].checkbox("Margin disabled", value=safety["margin_disabled"], disabled=True)
safe_cols[4].checkbox("Auto-order disabled", value=safety["auto_order_disabled"], disabled=True)
for warning in safety["warnings"]:
    st.warning(warning)

st.subheader("Provider Strategy")
st.write("- Crypto: Binance read-only data > yfinance > fallback")
st.write("- US/ETF: IBKR future read-only > yfinance > fallback")
st.write("- Taiwan: Yuanta future/CSV > yfinance > fallback")
st.write("- Signals: TradingView webhook > internal rules")
st.write("- TradingView, Binance, IBKR, and Yuanta trading/order endpoints are not implemented.")
st.write("- OKX, Bitget, FRED, and yfinance are read-only or fallback data sources.")

with st.expander("Read-only provider placeholders"):
    st.json(
        {
            "binance": account_snapshot_placeholder(),
            "ibkr_flex": flex_web_service_placeholder(),
            "ibkr_client_portal": client_portal_portfolio_placeholder(),
            "ibkr_market_data": market_data_snapshot_placeholder(),
        }
    )

st.subheader("Telegram Test")
st.code("TELEGRAM_BOT_TOKEN=\nTELEGRAM_CHAT_ID=", language="bash")

message = st.text_area("Test message", value="Devin Investment OS test message.")
if st.button("Send Test Telegram Message", use_container_width=True):
    st.success("Sent.") if send_telegram_message(message) else st.warning("Skipped. Check .env configuration.")

st.subheader("Security Notes")
st.write("- Keep `.env` local to the server.")
st.write("- Do not commit Telegram tokens, passwords, SSH keys, or account numbers.")
st.write("- Data files are local CSV files and can be edited from the app.")
