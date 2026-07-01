from datetime import datetime

import pandas as pd
import streamlit as st

from utils.data import load_portfolio, load_watchlist
from utils.market_regime import calculate_market_regime
from utils.portfolio_risk import portfolio_summary
from utils.provider_status import active_provider_rows
from utils.watchlist_scoring import score_watchlist


st.set_page_config(page_title="Devin Investment OS", page_icon="DI", layout="wide")

st.markdown(
    """
    <style>
        .block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
        [data-testid="stMetric"] {border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px;}
        .action-box {border: 1px solid #d1d5db; border-radius: 10px; padding: 1rem; background: #f9fafb;}
        @media (max-width: 768px) {
            .block-container {padding-left: 1rem; padding-right: 1rem;}
            h1 {font-size: 1.8rem;}
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Devin Investment OS")
st.caption("Read-only market regime, portfolio risk, watchlist zones, and daily playbook.")

regime = calculate_market_regime()
portfolio = load_portfolio()
watchlist = load_watchlist()
risk = portfolio_summary(portfolio)
watchlist_tickers = watchlist["ticker"].dropna().astype(str).tolist() if not watchlist.empty else None
watch_scores = score_watchlist(watchlist_tickers)
watch_df = pd.DataFrame(watch_scores)

status_cols = st.columns(4)
status_cols[0].metric("Market Score", f"{regime['market_score']}/100")
status_cols[1].metric("Market Regime", regime["market_regime"])
status_cols[2].metric("Today Action", regime["today_action"])
status_cols[3].metric("Data Confidence", regime["confidence_level"])

st.caption(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Portfolio Risk: {risk['risk_score']}/100")

st.subheader("Active Provider Status")
provider_cols = st.columns(4)
for index, row in enumerate(active_provider_rows()):
    provider_cols[index].metric(row["Provider"], row["Status"].title())

st.subheader("Market Components")
component_cols = st.columns(4)
for index, (name, score) in enumerate(regime["components"].items()):
    component_cols[index % 4].metric(name, f"{score}/100")

st.subheader("Recommended Action")
st.markdown(f"<div class='action-box'>{regime['recommended_action']}</div>", unsafe_allow_html=True)

left, right = st.columns(2)
with left:
    st.subheader("What Changed Today")
    for item in regime["what_changed"]:
        st.write(f"- {item}")
with right:
    st.subheader("Warnings")
    for warning in regime["warnings"][:5]:
        st.warning(warning)

st.subheader("Watchlist Decision Signals")
if watch_df.empty:
    st.info("No watchlist items found.")
else:
    signal_cols = [
        "ticker",
        "latest_price",
        "distance_ma20_pct",
        "distance_ma60_pct",
        "drawdown_52w_pct",
        "trend_score",
        "pullback_score",
        "risk_label",
        "action_label",
    ]
    st.dataframe(watch_df[signal_cols], use_container_width=True, hide_index=True)

st.subheader("Quick Portfolio")
if portfolio.empty:
    st.info("No holdings found.")
else:
    columns = [c for c in ["ticker", "name", "shares", "current_price", "market_value", "action_signal"] if c in portfolio]
    st.dataframe(portfolio[columns], use_container_width=True, hide_index=True)
    for item in risk["suggestions"]:
        st.write(f"- {item}")

st.subheader("Navigation")
links = st.columns(9)
links[0].page_link("pages/1_Macro_Dashboard.py", label="Macro")
links[1].page_link("pages/2_Portfolio.py", label="Portfolio")
links[2].page_link("pages/3_Watchlist.py", label="Watchlist")
links[3].page_link("pages/5_Asset_Scores.py", label="Asset Scores")
links[4].page_link("pages/6_Daily_Playbook.py", label="Daily Playbook")
links[5].page_link("pages/7_History.py", label="History")
links[6].page_link("pages/8_TradingView_Alerts.py", label="TV Alerts")
links[7].page_link("pages/9_Data_Quality.py", label="Data Quality")
links[8].page_link("pages/4_Settings.py", label="Settings")
