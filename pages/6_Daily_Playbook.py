import pandas as pd
import streamlit as st

from utils.data import load_watchlist
from utils.market_regime import calculate_market_regime
from utils.watchlist_scoring import DEFAULT_WATCHLIST, score_watchlist


st.set_page_config(page_title="Daily Playbook", page_icon="DI", layout="wide")
st.title("Daily Playbook")
st.caption("Read-only daily decision support. Verify broker quotes before real trading.")

regime = calculate_market_regime()
watchlist = load_watchlist()
tickers = watchlist["ticker"].dropna().astype(str).tolist() if not watchlist.empty else DEFAULT_WATCHLIST
watch_scores = score_watchlist(tickers)
watch_df = pd.DataFrame(watch_scores)

st.subheader("1. Market Regime Summary")
summary_cols = st.columns(4)
summary_cols[0].metric("Market Score", f"{regime['market_score']}/100")
summary_cols[1].metric("Regime", regime["market_regime"])
summary_cols[2].metric("Suggested Action", regime["today_action"])
summary_cols[3].metric("Confidence", regime["confidence_level"])
st.write(regime["recommended_action"])

st.subheader("2. What Changed Today")
for item in regime["what_changed"]:
    st.write(f"- {item}")

st.subheader("3. What To Watch")
for item in regime["what_to_watch"]:
    st.write(f"- {item}")

st.subheader("4. Buy-Zone Candidates")
buy_zone = watch_df[watch_df["action_label"].eq("Potential buy zone - verify quote")].head(5)
pullback = watch_df[watch_df["action_label"].eq("Pullback watch")].head(5)
if buy_zone.empty and pullback.empty:
    st.write("- No clean buy-zone candidates. Watch / wait.")
else:
    for _, row in pd.concat([buy_zone, pullback]).head(8).iterrows():
        st.write(f"- {row['ticker']}: {row['action_label']} ({row['distance_ma20_pct']:.1f}% vs MA20)")

st.subheader("5. Risk Warnings")
for item in regime["risk_warnings"]:
    st.warning(item)
extended = watch_df[watch_df["action_label"].eq("Extended / Do not chase")].head(5)
for _, row in extended.iterrows():
    st.warning(f"{row['ticker']}: Extended / Do not chase")

st.subheader("6. Suggested Action")
suggestions = [
    regime["recommended_action"],
    "Buy only in layers; never chase vertical moves.",
    "DCA core ETFs only when market confidence is not High.",
    "Raise cash if VIX confirms risk-off.",
]
for item in suggestions:
    st.write(f"- {item}")

st.subheader("7. Telegram-Ready Summary")
top_signals = watch_df[["ticker", "action_label"]].head(3).to_dict("records") if not watch_df.empty else []
telegram_summary = "\n".join(
    [
        "Devin Investment OS Daily Playbook",
        f"Market Score: {regime['market_score']}/100",
        f"Regime: {regime['market_regime']}",
        f"Action: {regime['today_action']}",
        f"VIX: {regime['key_metrics'].get('VIX')}",
        "Top Watchlist Signals:",
        *[f"- {item['ticker']}: {item['action_label']}" for item in top_signals],
        "Risk Warning: decision-support only; verify broker quote before trading.",
    ]
)
st.code(telegram_summary, language="text")
