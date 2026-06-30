import streamlit as st

from utils.playbook import daily_playbook, scenario_playbook, weekly_playbook


st.set_page_config(page_title="Daily Playbook", page_icon="DI", layout="wide")
st.title("Daily Playbook")
st.caption("A concise operating plan for the next trading session.")

playbook = daily_playbook()

st.subheader("1. Market Regime")
st.metric(playbook["market_regime"], f"{playbook['market_score']}/100")

st.subheader("2. What Changed Today")
st.write("- AI / Tech remains the strongest sleeve.")
st.write("- Liquidity is constructive but not a full green light.")
st.write("- Breadth is mixed, so avoid low-quality breakouts.")

st.subheader("3. What To Buy If Market Pulls Back")
for item in playbook["pullback_5"]:
    st.write(f"- 5% pullback: {item}")
for item in playbook["pullback_8"]:
    st.write(f"- 8% pullback: {item}")
for item in playbook["pullback_12_15"]:
    st.write(f"- 12-15% pullback: {item}")

st.subheader("4. What Not To Chase")
for item in playbook["do_not_chase"]:
    st.write(f"- {item}")

st.subheader("5. Risk Alerts")
st.write("- Respect stop levels before adding fresh risk.")
st.write("- Keep high-beta exposure sized below core ETF exposure.")

st.subheader("6. Suggested Cash Stance")
st.write(playbook["cash_stance"])

st.subheader("Weekly Focus")
for item in weekly_playbook()["focus"]:
    st.write(f"- {item}")

st.subheader("Scenarios")
for scenario in scenario_playbook():
    st.write(f"- {scenario['scenario']}: {scenario['action']}")
