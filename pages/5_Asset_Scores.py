import pandas as pd
import streamlit as st


st.set_page_config(page_title="Asset Scores", page_icon="DI", layout="wide")
st.title("Asset Scores")
st.caption("Asset class scorecard for daily allocation decisions.")

rows = [
    ("US Market", 62, "Bullish Neutral", "SPY, QQQ, DIA", "Hold"),
    ("Taiwan Market", 58, "Neutral", "0050.TW, 2330.TW, 2454.TW", "Watch"),
    ("AI / Semis", 72, "Constructive", "NVDA, TSM, MRVL, GEV", "Buy Zone"),
    ("Gold", 55, "Neutral", "GC=F, SGLD.L", "Hold"),
    ("BTC", 48, "Neutral", "BTC-USD", "Watch"),
    ("Core ETF", 66, "Constructive", "VWRA.L, CNX1.L, IEMA.L", "Buy Zone"),
    ("High Beta Stocks", 44, "Mixed", "PLTR, MRVL", "Avoid"),
]

df = pd.DataFrame(rows, columns=["Asset", "Score", "Status", "Key Indicators", "Suggested Action"])

cols = st.columns(4)
cols[0].metric("Best Score", df.loc[df["Score"].idxmax(), "Asset"])
cols[1].metric("Risk Watch", "High Beta Stocks")
cols[2].metric("Core Bias", "Hold")
cols[3].metric("Action", "Buy Zone only")

st.dataframe(df, use_container_width=True, hide_index=True)
