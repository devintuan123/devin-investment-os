from datetime import datetime

import pandas as pd
import streamlit as st

from utils.data import load_portfolio, load_watchlist
from utils.i18n import (
    get_lang,
    render_language_sidebar,
    render_refresh_button,
    t,
    translate_action_label,
    translate_regime,
    translate_risk_label,
    translate_status,
    translate_warning,
)
from utils.market_regime import calculate_market_regime
from utils.portfolio_risk import portfolio_summary
from utils.provider_status import active_provider_rows
from utils.watchlist_scoring import score_watchlist


st.set_page_config(page_title="Devin Investment OS", page_icon="DI", layout="wide")
render_language_sidebar()
render_refresh_button()

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

st.title(t("app_title"))
st.caption(t("app_caption"))

regime = calculate_market_regime()
portfolio = load_portfolio()
watchlist = load_watchlist()
risk = portfolio_summary(portfolio)
watchlist_tickers = watchlist["ticker"].dropna().astype(str).tolist() if not watchlist.empty else None
watch_scores = score_watchlist(watchlist_tickers)
watch_df = pd.DataFrame(watch_scores)

status_cols = st.columns(4)
status_cols[0].metric(t("market_score"), f"{regime['market_score']}/100")
status_cols[1].metric(t("market_regime"), translate_regime(regime["market_regime"]))
status_cols[2].metric(t("today_action"), translate_action_label(regime["today_action"]))
status_cols[3].metric(t("data_confidence"), t(regime["confidence_level"].lower()))

st.caption(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Portfolio Risk: {risk['risk_score']}/100")

st.subheader(t("active_provider_status"))
provider_cols = st.columns(4)
for index, row in enumerate(active_provider_rows()):
    provider_cols[index].metric(row["Provider"], translate_status(row["Status"]))

st.subheader(t("market_components"))
component_cols = st.columns(4)
for index, (name, score) in enumerate(regime["components"].items()):
    component_cols[index % 4].metric(name, f"{score}/100")

st.subheader(t("recommended_action"))
recommended_action = regime["recommended_action"] if get_lang() == "en" else "核心部位續抱；只在計畫內回檔分批加碼；避免追高延伸標的。"
st.markdown(f"<div class='action-box'>{recommended_action}</div>", unsafe_allow_html=True)

left, right = st.columns(2)
with left:
    st.subheader(t("what_changed_today"))
    changed_items = regime["what_changed"] if get_lang() == "en" else [
        "SPY 與 QQQ 仍需觀察 20 日與 60 日均線確認。",
        "VIX 低於 18 時較有利風險偏好。",
        "Binance BTCUSDT 唯讀價格可用。",
    ]
    for item in changed_items:
        st.write(f"- {item}")
with right:
    st.subheader(t("warnings"))
    for warning in regime["warnings"][:5]:
        st.warning(translate_warning(warning))

st.subheader(t("watchlist_decision_signals"))
if watch_df.empty:
    st.info(t("no_watchlist"))
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
    display_df = watch_df[signal_cols].copy()
    display_df["action_label"] = display_df["action_label"].map(translate_action_label)
    display_df["risk_label"] = display_df["risk_label"].map(translate_risk_label)
    if get_lang() == "zh":
        display_df = display_df.rename(
            columns={
                "ticker": t("ticker"),
                "latest_price": t("latest_price"),
                "distance_ma20_pct": "距 20 日均線 %",
                "distance_ma60_pct": "距 60 日均線 %",
                "drawdown_52w_pct": t("drawdown_52w_pct"),
                "trend_score": t("trend_score"),
                "pullback_score": t("pullback_score"),
                "risk_label": t("risk_label"),
                "action_label": t("action_label"),
            }
        )
    st.dataframe(display_df, use_container_width=True, hide_index=True)

st.subheader(t("quick_portfolio"))
if portfolio.empty:
    st.info(t("no_holdings"))
else:
    columns = [c for c in ["ticker", "name", "shares", "current_price", "market_value", "action_signal"] if c in portfolio]
    st.dataframe(portfolio[columns], use_container_width=True, hide_index=True)
    for item in risk["suggestions"]:
        st.write(f"- {item}")

st.subheader(t("navigation"))
links = st.columns(9)
links[0].page_link("pages/1_Macro_Dashboard.py", label=t("macro"))
links[1].page_link("pages/2_Portfolio.py", label=t("portfolio"))
links[2].page_link("pages/3_Watchlist.py", label=t("watchlist"))
links[3].page_link("pages/5_Asset_Scores.py", label=t("asset_scores"))
links[4].page_link("pages/6_Daily_Playbook.py", label=t("daily_playbook"))
links[5].page_link("pages/7_History.py", label=t("history"))
links[6].page_link("pages/8_TradingView_Alerts.py", label="TV Alerts")
links[7].page_link("pages/9_Data_Quality.py", label=t("data_quality"))
links[8].page_link("pages/4_Settings.py", label=t("settings"))
