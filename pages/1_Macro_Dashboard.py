import pandas as pd
import streamlit as st

from utils.indicators import market_indicators
from utils.scoring import calculate_market_score


st.set_page_config(page_title="Macro Dashboard", page_icon="DI", layout="wide")
st.title("Macro Dashboard")
st.caption("Macro regime framework with live/fallback market inputs.")

inputs = {"liquidity": 68, "sentiment": 62, "breadth": 58, "ai_tech": 74, "defensive": 52}
score = calculate_market_score(inputs)

col1, col2 = st.columns(2)
col1.metric("Market Score", f"{score['score']}/100")
col2.metric("Regime", score["regime"])

indicators = market_indicators()
for section, payload in indicators.items():
    st.subheader(section)
    c1, c2 = st.columns(2)
    c1.metric("Score", f"{payload['score']}/100")
    c2.metric("Status", payload["status"])
    st.write(payload["explanation"])
    st.write(f"What changed: {payload['what_changed']}")
    rows = pd.DataFrame(payload["data"])
    st.dataframe(rows[["ticker", "price", "return_5d", "return_1m", "distance_ma_50d", "drawdown_52w"]], use_container_width=True, hide_index=True)
