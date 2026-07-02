import pandas as pd
import streamlit as st

from utils.buy_zone_engine import DEFAULT_BUY_ZONE_TICKERS, score_buy_zones
from utils.i18n import t, translate_action_label, translate_warning
from utils.interactive_table import render_interactive_table
from utils.ui import get_current_lang, render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


def render(lang: str) -> None:
    st.title(t("buy_zones"))
    st.caption(t("buy_zones_caption"))

    scores = pd.DataFrame(score_buy_zones(DEFAULT_BUY_ZONE_TICKERS))
    if scores.empty:
        st.info(t("no_data"))
    else:
        view = scores[["ticker", "asset_category", "latest_price", "trend_status", "drawdown_52w_pct", "ma20", "ma60", "ma120", "buy_zone_1", "buy_zone_2", "buy_zone_3", "current_zone_status", "action_label", "strategy_action", "strategy_warning"]].copy()
        view["action_label"] = view["action_label"].map(translate_action_label)
        view["strategy_action"] = view["strategy_action"].map(translate_action_label)
        render_interactive_table(view, table_key="buy_zones", lang=lang)
        for warning in scores["warning"].dropna().astype(str).unique()[:5]:
            if warning:
                st.warning(translate_warning(warning))
