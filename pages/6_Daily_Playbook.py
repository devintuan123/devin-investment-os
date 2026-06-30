import streamlit as st

from utils.scoring import calculate_market_score


st.set_page_config(page_title="Daily Playbook", page_icon="DI", layout="wide")
st.title("Daily Playbook")
st.caption("A concise operating plan for the next trading session.")

score = calculate_market_score({"liquidity": 68, "sentiment": 62, "breadth": 58, "ai_tech": 74, "defensive": 52})

st.subheader("1. Market Regime")
st.metric(score["regime"], f"{score['score']}/100")
st.write(score["summary"])

st.subheader("2. What Changed Today")
st.write("- AI / Tech remains the strongest sleeve.")
st.write("- Liquidity is constructive but not a full green light.")
st.write("- Breadth is mixed, so avoid low-quality breakouts.")

st.subheader("3. What To Buy If Market Pulls Back")
for item in ["VWRA", "0050", "GEV", "IEMA", "TSMC / 2330"]:
    st.write(f"- {item}")

st.subheader("4. What Not To Chase")
for item in ["PLTR averaging down", "MRVL averaging down", "Chasing sharp spikes after news"]:
    st.write(f"- {item}")

st.subheader("5. Risk Alerts")
st.write("- Respect stop levels before adding fresh risk.")
st.write("- Keep high-beta exposure sized below core ETF exposure.")

st.subheader("6. Suggested Cash Stance")
st.write("Hold moderate cash and deploy only into predefined Buy Zone levels.")
