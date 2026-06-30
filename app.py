import streamlit as st
from datetime import datetime

from utils.data import load_portfolio, load_watchlist
from utils.market_data import get_prices
from utils.playbook import daily_playbook
from utils.portfolio_risk import portfolio_summary
from utils.scoring import calculate_market_score
from utils.signals import watchlist_signal


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
playbook = daily_playbook()
risk = portfolio_summary(portfolio)
watchlist["signal"] = watchlist.apply(watchlist_signal, axis=1)
best_buys = watchlist[watchlist["signal"] == "Buy Zone"].head(3)
risk_alerts = watchlist[watchlist["signal"] == "Risk Alert"].head(3)
data_status = get_prices(["SPY", "QQQ", "GC=F"])
warning_count = int((data_status.get("warning", "") != "").sum()) if not data_status.empty else 0

col1, col2, col3 = st.columns(3)
col1.metric("Market Score", f"{score['score']}/100")
col2.metric("Regime", score["regime"])
col3.metric("Portfolio Risk", f"{risk['risk_score']}/100")

st.caption(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Data source status: {'fallback warnings' if warning_count else 'live/fallback ready'}")

st.subheader("Today's Actions")
for action in score["actions"]:
    st.write(f"- {action}")

cols = st.columns(3)
with cols[0]:
    st.subheader("Top Risk Alerts")
    if risk_alerts.empty:
        st.write("- None")
    else:
        for _, row in risk_alerts.iterrows():
            st.write(f"- {row['ticker']}: Risk Alert")
with cols[1]:
    st.subheader("Best Buy Candidates")
    if best_buys.empty:
        st.write("- No active Buy Zone hits")
    else:
        for _, row in best_buys.iterrows():
            st.write(f"- {row['ticker']}: Buy Zone")
with cols[2]:
    st.subheader("Cash Stance")
    st.write(playbook["cash_stance"])

st.subheader("Do Not Chase")
for item in playbook["do_not_chase"]:
    st.write(f"- {item}")

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
    st.write("Portfolio suggestions:")
    for item in risk["suggestions"]:
        st.write(f"- {item}")

st.subheader("Watchlist Preview")
if watchlist.empty:
    st.info("No watchlist items found.")
else:
    columns = [c for c in ["ticker", "name", "current_price", "buy_zone_low", "buy_zone_high", "trim_zone", "stop_level"] if c in watchlist]
    st.dataframe(watchlist[columns], use_container_width=True, hide_index=True)

st.subheader("Navigation")
links = st.columns(7)
links[0].page_link("pages/1_Macro_Dashboard.py", label="Macro")
links[1].page_link("pages/2_Portfolio.py", label="Portfolio")
links[2].page_link("pages/3_Watchlist.py", label="Watchlist")
links[3].page_link("pages/5_Asset_Scores.py", label="Asset Scores")
links[4].page_link("pages/6_Daily_Playbook.py", label="Daily Playbook")
links[5].page_link("pages/7_History.py", label="History")
links[6].page_link("pages/4_Settings.py", label="Settings")
