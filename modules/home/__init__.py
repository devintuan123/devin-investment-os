import pandas as pd
import streamlit as st

from utils.buy_zone_engine import score_buy_zones
from utils.i18n import t, translate_action_label, translate_regime, translate_risk_label, translate_term, translate_warning
from utils.interactive_table import render_interactive_table
from utils.market_regime import calculate_market_regime
from utils.portfolio_engine import calculate_position_values, load_portfolio, portfolio_health_score
from utils.provider_status import active_provider_rows
from utils.alert_engine import evaluate_alerts
from utils.snapshot_store import load_latest_snapshot, summarize_snapshot_trend
from utils.strategy_rules import get_cash_deployment_mode
from utils.ui import get_current_lang, render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


def render(lang: str) -> None:
    st.markdown(
        """
        <style>
            .block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
            [data-testid="stMetric"] {border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px;}
            .action-box {border: 1px solid #d1d5db; border-radius: 10px; padding: 1rem; background: #f9fafb;}
            @media (max-width: 768px) {.block-container {padding-left: 1rem; padding-right: 1rem;} h1 {font-size: 1.8rem;}}
        </style>
        """,
        unsafe_allow_html=True,
    )

    regime = calculate_market_regime()
    portfolio = load_portfolio()
    positions = calculate_position_values(portfolio)
    health = portfolio_health_score(portfolio)
    buy_zones = pd.DataFrame(score_buy_zones())
    average_drift = float(positions["drift"].abs().mean()) if not positions.empty else 0.0
    cash_mode = get_cash_deployment_mode(regime["market_score"], regime["market_regime"], average_drift)
    latest_snapshot = load_latest_snapshot()
    snapshot_trend = summarize_snapshot_trend()
    active_alerts = evaluate_alerts()

    st.title(t("app_title"))
    st.caption(t("app_caption"))

    cols = st.columns(4)
    cols[0].metric(t("market_score"), f"{regime['market_score']}/100")
    cols[1].metric(t("market_regime"), translate_regime(regime["market_regime"]))
    cols[2].metric(t("today_action"), translate_action_label(regime["today_action"]))
    cols[3].metric(t("data_confidence"), t(regime["confidence_level"].lower()))

    status_cols = st.columns(4)
    status_cols[0].metric(t("strategy_mode"), t(cash_mode))
    status_cols[1].metric(t("cash_deployment_mode"), t(cash_mode))
    status_cols[2].metric(t("snapshot_status"), latest_snapshot.get("timestamp", t("no_snapshots")))
    status_cols[3].metric(t("active_alerts"), str(len(active_alerts)))

    st.subheader(t("active_provider_status"))
    provider_cols = st.columns(4)
    for index, row in enumerate(active_provider_rows()):
        provider_cols[index].metric(row["Provider"], row["Status"])

    st.subheader(t("market_components"))
    component_cols = st.columns(4)
    for index, (name, score) in enumerate(regime["components"].items()):
        component_cols[index % 4].metric(translate_term(name), f"{score}/100")

    st.subheader(t("recommended_action"))
    st.markdown(f"<div class='action-box'>{regime['recommended_action'] if lang == 'en' else t('read_only_notice')}</div>", unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.subheader(t("portfolio_drift_summary"))
        st.metric(t("portfolio_health"), f"{health['score']}/100")
        for warning in health["warnings"][:3]:
            st.write(f"- {warning if lang == 'en' else t('read_only_notice')}")
    with right:
        st.subheader(t("warnings"))
        for warning in regime["warnings"][:4]:
            st.warning(translate_warning(warning))

    st.subheader(t("top_add_candidates"))
    if buy_zones.empty:
        st.info(t("no_data"))
    else:
        candidates = buy_zones[buy_zones["action_label"].isin(["Potential Layer 1", "Potential Layer 2", "Deep Pullback Watch", "Hold"])].head(5).copy()
        if candidates.empty:
            st.info(t("no_data"))
        else:
            candidates["strategy_action"] = candidates["strategy_action"].map(translate_action_label)
            render_interactive_table(candidates[["ticker", "asset_category", "latest_price", "drawdown_52w_pct", "strategy_action", "strategy_warning"]], table_key="home_candidates", lang=lang)

    st.subheader(t("quick_portfolio"))
    if positions.empty:
        st.info(t("no_holdings"))
    else:
        view = positions[["symbol", "category", "strategy_category", "market_value", "current_weight", "target_weight", "strategy_target_weight", "drift", "strategy_drift", "action_suggestion"]].copy()
        view["action_suggestion"] = view["action_suggestion"].map(translate_action_label)
        render_interactive_table(view, table_key="home_portfolio", lang=lang)

    st.subheader(t("snapshot_trend"))
    render_interactive_table(pd.DataFrame([snapshot_trend]), table_key="home_snapshot_trend", lang=lang)

    st.subheader(t("navigation"))
    links = st.columns(10)
    links[0].page_link("pages/1_Macro_Dashboard.py", label=t("macro"))
    links[1].page_link("pages/2_Portfolio.py", label=t("portfolio"))
    links[2].page_link("pages/3_Watchlist.py", label=t("watchlist"))
    links[3].page_link("pages/5_Asset_Scores.py", label=t("asset_scores"))
    links[4].page_link("pages/6_Daily_Playbook.py", label=t("daily_playbook"))
    links[5].page_link("pages/10_Buy_Zones.py", label=t("buy_zones"))
    links[6].page_link("pages/7_History.py", label=t("history"))
    links[7].page_link("pages/8_TradingView_Alerts.py", label=t("tv_alerts"))
    links[8].page_link("pages/9_Data_Quality.py", label=t("data_quality"))
    links[9].page_link("pages/4_Settings.py", label=t("settings"))
