import pandas as pd
import streamlit as st

from utils.providers.tokenized_equity_provider import tokenized_equity_health_check


st.set_page_config(page_title="Asset Scores", page_icon="DI", layout="wide")
st.title("Asset Scores")
st.caption("Asset class scorecard for daily allocation decisions.")

tokenized_health = tokenized_equity_health_check()
tokenized_note = (
    f"Tokenized/Synthetic Reference available: {', '.join(tokenized_health['supported_symbols'])}"
    if tokenized_health["supported_symbols"]
    else "No Binance tokenized equity symbols detected"
)

rows = [
    ("US Market", 62, "Bullish Neutral", "Uptrend", "Medium", "Hold", f"SPY, QQQ, DIA | Supplement: {tokenized_note}"),
    ("Taiwan Market", 58, "Neutral", "Repairing", "Medium", "Watch", "0050.TW, 2330.TW, 2454.TW"),
    ("AI / Semis", 72, "Constructive", "Strong", "High", "Buy Zone", f"NVDA, TSM, MRVL | Supplement: {tokenized_note}"),
    ("AI Power Infrastructure", 76, "Constructive", "Strong", "High", "Buy pullbacks", "GEV"),
    ("Gold", 55, "Neutral", "Stable", "Low", "Hold", "GC=F, SGLD.L"),
    ("BTC", 48, "Neutral", "Volatile", "High", "Watch", "BTC-USD"),
    ("Core ETFs", 66, "Constructive", "Stable", "Low", "Buy Zone", "VWRA.L, CNX1.L, IEMA.L"),
    ("High Beta Stocks", 44, "Mixed", "Unstable", "High", "Avoid", "PLTR, MRVL"),
    ("Healthcare", 52, "Neutral", "Stable", "Low", "Hold", "WHEA.L"),
]

df = pd.DataFrame(rows, columns=["Asset", "Score", "Status", "Trend", "Risk", "Action", "Related Tickers"])

cols = st.columns(4)
cols[0].metric("Best Score", df.loc[df["Score"].idxmax(), "Asset"])
cols[1].metric("Risk Watch", "High Beta Stocks")
cols[2].metric("Core Bias", "Hold")
cols[3].metric("Action", "Buy Zone only")

st.dataframe(df, use_container_width=True, hide_index=True)

st.warning("Tokenized/Synthetic Reference data is supplementary sentiment only. Verify with broker quote before trading.")
