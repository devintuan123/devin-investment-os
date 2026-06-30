import streamlit as st

from utils.data import load_portfolio, load_watchlist
from utils.scoring import calculate_market_score


st.set_page_config(page_title="Devin Investment OS", page_icon="DI", layout="wide")

st.markdown(
    """
    <style>
        .block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
        [data-testid="stMetric"] {border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px;}
        @media (max-width: 768px) {
            .block-container {padding-left: 1rem; padding-right: 1rem;}
            h1 {font-size: 1.8rem;}
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Devin Investment OS")
st.caption("Market regime, portfolio risk, watchlist zones, and daily playbook.")

score = calculate_market_score(
    {"liquidity": 68, "sentiment": 62, "breadth": 58, "ai_tech": 74, "defensive": 52}
)
portfolio = load_portfolio()
watchlist = load_watchlist()

col1, col2, col3 = st.columns(3)
col1.metric("Market Score", f"{score['score']}/100")
col2.metric("Regime", score["regime"])
col3.metric("Watchlist Items", len(watchlist))

st.subheader("Today's Actions")
for action in score["actions"]:
    st.write(f"- {action}")

st.subheader("Category Scores")
cols = st.columns(5)
for idx, category in enumerate(score["categories"].values()):
    cols[idx].metric(category["label"], f"{category['score']}/100")

st.subheader("Quick Portfolio")
if portfolio.empty:
    st.info("No holdings found.")
else:
    columns = [c for c in ["ticker", "name", "shares", "current_price", "market_value", "action_signal"] if c in portfolio]
    st.dataframe(portfolio[columns], use_container_width=True, hide_index=True)

st.subheader("Watchlist Preview")
if watchlist.empty:
    st.info("No watchlist items found.")
else:
    columns = [c for c in ["ticker", "name", "current_price", "buy_zone_low", "buy_zone_high", "trim_zone", "stop_level"] if c in watchlist]
    st.dataframe(watchlist[columns], use_container_width=True, hide_index=True)

st.subheader("Navigation")
links = st.columns(6)
links[0].page_link("pages/1_Macro_Dashboard.py", label="Macro")
links[1].page_link("pages/2_Portfolio.py", label="Portfolio")
links[2].page_link("pages/3_Watchlist.py", label="Watchlist")
links[3].page_link("pages/5_Asset_Scores.py", label="Asset Scores")
links[4].page_link("pages/6_Daily_Playbook.py", label="Daily Playbook")
links[5].page_link("pages/4_Settings.py", label="Settings")
