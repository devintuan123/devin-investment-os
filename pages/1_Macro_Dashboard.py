import pandas as pd
import streamlit as st

from utils.scoring import calculate_market_score


st.set_page_config(page_title="Macro Dashboard", page_icon="🌐", layout="wide")

st.title("Macro Dashboard")
st.caption("Mock macro framework structured for future real data integration.")

sections = {
    "Liquidity": {
        "US10Y": 64,
        "Real Yield": 56,
        "DXY": 60,
        "FedWatch": 66,
    },
    "Sentiment": {
        "VIX": 62,
        "Put/Call Ratio": 58,
        "Fear & Greed": 65,
    },
    "Breadth": {
        "Advance/Decline": 55,
        "New High/New Low": 52,
        "% above 200MA": 60,
    },
    "AI/Tech": {
        "SOX": 72,
        "NVDA": 78,
        "TSMC ADR": 70,
        "GEV": 76,
    },
    "Defensive": {
        "Gold": 55,
        "BTC": 50,
        "SGLD": 58,
    },
}

score_inputs = {
    "liquidity": sum(sections["Liquidity"].values()) / len(sections["Liquidity"]),
    "sentiment": sum(sections["Sentiment"].values()) / len(sections["Sentiment"]),
    "breadth": sum(sections["Breadth"].values()) / len(sections["Breadth"]),
    "ai_tech": sum(sections["AI/Tech"].values()) / len(sections["AI/Tech"]),
    "defensive": sum(sections["Defensive"].values()) / len(sections["Defensive"]),
}
score_result = calculate_market_score(score_inputs)

col1, col2 = st.columns(2)
col1.metric("Market Score", f"{score_result['score']}/100")
col2.metric("Regime", score_result["regime"])

for section, indicators in sections.items():
    st.subheader(section)
    rows = [{"Indicator": name, "Mock Score": value, "Status": "Constructive" if value >= 60 else "Watch"} for name, value in indicators.items()]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
