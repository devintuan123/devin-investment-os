import pandas as pd
import streamlit as st

from utils.buy_zone_engine import score_buy_zones
from utils.i18n import t, translate_action_label, translate_regime, translate_warning
from utils.interactive_table import render_interactive_table
from utils.market_regime import calculate_market_regime
from utils.portfolio_engine import calculate_position_values, load_portfolio, portfolio_health_score
from utils.ui import get_current_lang, render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


st.set_page_config(page_title="Daily Playbook", page_icon="DI", layout="wide")
render_sidebar_language_switch()
render_refresh_button()
render_sidebar_provider_status()

regime = calculate_market_regime()
lang = get_current_lang()
positions = calculate_position_values(load_portfolio())
health = portfolio_health_score(load_portfolio())
buy_zones = pd.DataFrame(score_buy_zones())

st.title(t("daily_playbook"))
st.caption(t("daily_caption"))

st.subheader(t("market_regime_summary"))
summary_cols = st.columns(4)
summary_cols[0].metric(t("market_score"), f"{regime['market_score']}/100")
summary_cols[1].metric(t("market_regime"), translate_regime(regime["market_regime"]))
summary_cols[2].metric(t("suggested_action"), translate_action_label(regime["today_action"]))
summary_cols[3].metric(t("confidence"), t(regime["confidence_level"].lower()))
st.write(regime["recommended_action"])

st.subheader(t("portfolio_drift_summary"))
st.metric(t("portfolio_health"), f"{health['score']}/100")
if not positions.empty:
    drift_view = positions[["symbol", "current_weight", "target_weight", "drift", "action_suggestion"]].head(8).copy()
    drift_view["action_suggestion"] = drift_view["action_suggestion"].map(translate_action_label)
    render_interactive_table(drift_view, table_key="daily_drift", lang=lang)

st.subheader(t("what_changed_today"))
for item in regime["what_changed"]:
    st.write(f"- {item}")

st.subheader(t("what_to_watch"))
for item in regime["what_to_watch"]:
    st.write(f"- {item}")

st.subheader(t("buy_zone_candidates"))
if buy_zones.empty:
    st.info(t("no_data"))
else:
    add_candidates = buy_zones[buy_zones["action_label"].isin(["Potential Layer 1", "Potential Layer 2", "Deep Pullback Watch", "Hold"])].head(3).copy()
    add_candidates["action_label"] = add_candidates["action_label"].map(translate_action_label)
    render_interactive_table(add_candidates[["ticker", "latest_price", "drawdown_52w_pct", "action_label", "warning"]], table_key="daily_add_candidates", lang=lang)

st.subheader(t("top_avoid_warnings"))
if not buy_zones.empty:
    avoid = buy_zones[buy_zones["action_label"].isin(["Broken trend, avoid", "Extended, do not chase"])].head(3).copy()
    if avoid.empty:
        st.info(t("no_data"))
    else:
        avoid["action_label"] = avoid["action_label"].map(translate_action_label)
        render_interactive_table(avoid[["ticker", "latest_price", "drawdown_52w_pct", "action_label"]], table_key="daily_avoid", lang=lang)

st.subheader(t("risk_warnings"))
for warning in regime["risk_warnings"]:
    st.warning(warning)
for warning in regime["warnings"]:
    st.warning(translate_warning(warning))

st.subheader(t("cash_deployment"))
if regime["market_regime"] == "Risk-On":
    st.write(t("gradual"))
elif regime["market_regime"] == "Risk-Off":
    st.write(t("wait"))
else:
    st.write(t("dca_only"))

st.subheader(t("telegram_ready_summary"))
top_signals = buy_zones[["ticker", "action_label"]].head(3).to_dict("records") if not buy_zones.empty else []
telegram_summary = "\n".join(
    [
        "Devin Investment OS Daily Playbook",
        f"{t('market_score')}: {regime['market_score']}/100",
        f"{t('market_regime')}: {translate_regime(regime['market_regime'])}",
        f"{t('suggested_action')}: {translate_action_label(regime['today_action'])}",
        f"{t('portfolio_health')}: {health['score']}/100",
        t("buy_zone_candidates"),
        *[f"- {item['ticker']}: {translate_action_label(item['action_label'])}" for item in top_signals],
        t("broker_warning"),
    ]
)
st.code(telegram_summary, language="text")
