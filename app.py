import pandas as pd
import streamlit as st

from utils.data import load_portfolio, load_watchlist
from utils.scoring import calculate_market_score


st.set_page_config(
    page_title="Devin Investment OS",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        [data-testid="stMetric"] {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 12px;
        }
        @media (max-width: 768px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            h1 {
                font-size: 1.8rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def action_summary(score_result: dict) -> list[str]:
    score = score_result["score"]
    if score >= 80:
        return ["Risk budget can stay active.", "Review watchlist breakouts.", "Avoid chasing extended positions."]
    if score >= 60:
        return ["Keep core holdings.", "Add only near planned buy zones.", "Watch rates, DXY, and breadth."]
    if score >= 40:
        return ["Stay selective.", "Trim weak positions.", "Wait for clearer confirmation."]
    if score >= 20:
        return ["Reduce high-beta exposure.", "Protect capital.", "Focus on defensive assets."]
    return ["Stay defensive.", "Avoid new risk.", "Preserve cash and review stop levels."]


st.title("Devin Investment OS")
st.caption("Local-first investment dashboard for portfolio tracking, watchlists, macro signals, and Telegram reports.")

mock_inputs = {
    "liquidity": 68,
    "sentiment": 62,
    "breadth": 58,
    "ai_tech": 74,
    "defensive": 52,
}
score_result = calculate_market_score(mock_inputs)

score_col, regime_col = st.columns(2)
score_col.metric("Market Score", f"{score_result['score']}/100")
regime_col.metric("Regime", score_result["regime"])

st.subheader("Today's Action Summary")
for item in action_summary(score_result):
    st.write(f"- {item}")

portfolio = load_portfolio()
watchlist = load_watchlist()

st.subheader("Quick Portfolio")
if portfolio.empty:
    st.info("No portfolio rows found.")
else:
    st.dataframe(portfolio, use_container_width=True, hide_index=True)

st.subheader("Watchlist Preview")
if watchlist.empty:
    st.info("No watchlist rows found.")
else:
    preview_columns = [column for column in ["ticker", "name", "buy_zone_low", "buy_zone_high", "sell_zone", "stop_level"] if column in watchlist]
    st.dataframe(watchlist[preview_columns], use_container_width=True, hide_index=True)

st.subheader("Navigation")
col1, col2, col3, col4 = st.columns(4)
col1.page_link("pages/1_Macro_Dashboard.py", label="Macro")
col2.page_link("pages/2_Portfolio.py", label="Portfolio")
col3.page_link("pages/3_Watchlist.py", label="Watchlist")
col4.page_link("pages/4_Settings.py", label="Settings")
