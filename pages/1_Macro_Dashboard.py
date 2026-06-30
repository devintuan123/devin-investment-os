import pandas as pd
import streamlit as st

from utils.market_data import get_price_change
from utils.scoring import calculate_market_score


st.set_page_config(page_title="Macro Dashboard", page_icon="DI", layout="wide")
st.title("Macro Dashboard")
st.caption("Macro regime framework with live/fallback market inputs.")

inputs = {"liquidity": 68, "sentiment": 62, "breadth": 58, "ai_tech": 74, "defensive": 52}
score = calculate_market_score(inputs)

col1, col2 = st.columns(2)
col1.metric("Market Score", f"{score['score']}/100")
col2.metric("Regime", score["regime"])

sections = {
    "Liquidity": ["US10Y", "Real Yield", "DXY", "FedWatch"],
    "Sentiment": ["VIX", "Put/Call Ratio", "Fear & Greed"],
    "Breadth": ["Advance/Decline", "New High/New Low", "% above 200MA"],
    "AI / Tech": ["SOX", "NVDA", "TSMC ADR", "GEV"],
    "Defensive / Hedge": ["Gold", "BTC", "SGLD"],
}
symbols = {"DXY": "DX-Y.NYB", "VIX": "^VIX", "NVDA": "NVDA", "TSMC ADR": "TSM", "GEV": "GEV", "Gold": "GC=F", "BTC": "BTC-USD", "SGLD": "SGLD.L"}

for section, indicators in sections.items():
    st.subheader(section)
    rows = []
    for indicator in indicators:
        ticker = symbols.get(indicator)
        rows.append(
            {
                "Indicator": indicator,
                "Ticker": ticker or "Mock",
                "Change %": get_price_change(ticker) if ticker else 0.0,
                "Status": "Watch" if indicator in {"VIX", "DXY"} else "Hold",
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
