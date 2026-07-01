import pandas as pd
import streamlit as st

from utils.market_regime import calculate_market_regime
from utils.provider_status import future_disabled_provider_rows


st.set_page_config(page_title="Data Quality", page_icon="DI", layout="wide")
st.title("Data Quality")
st.caption("Read-only provider freshness, confidence, and warnings.")

regime = calculate_market_regime()

st.subheader("Active Provider Quality")
quality_df = pd.DataFrame(regime["provider_quality"])
st.dataframe(quality_df, use_container_width=True, hide_index=True)

st.subheader("Source Hierarchy")
st.write("- Crypto: Binance read-only > yfinance > fallback")
st.write("- Stocks / ETFs / Taiwan / gold: yfinance delayed / best-effort > fallback")
st.write("- Macro: FRED daily / lagged")
st.write("- Notifications: Telegram outbound only")

st.subheader("Market Data Confidence")
cols = st.columns(4)
cols[0].metric("Overall Confidence", regime["confidence_level"])
cols[1].metric("Confidence Score", f"{regime['confidence_score']}/100")
cols[2].metric("Market Score", f"{regime['market_score']}/100")
cols[3].metric("Regime", regime["market_regime"])

st.subheader("Warnings")
for warning in regime["warnings"]:
    st.warning(warning)

with st.expander("Future / disabled providers", expanded=False):
    st.dataframe(pd.DataFrame(future_disabled_provider_rows()), use_container_width=True, hide_index=True)
    st.write("These providers remain disabled unless explicitly requested.")
