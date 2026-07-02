import pandas as pd
import streamlit as st

from utils.i18n import t, translate_regime, translate_term, translate_text
from utils.interactive_table import render_interactive_table
from utils.indicators import market_indicators
from utils.market_regime import calculate_market_regime
from utils.ui import get_current_lang, render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


def render(lang: str) -> None:
    regime = calculate_market_regime()
    st.title(t("macro_dashboard"))
    st.caption(t("macro_caption"))

    cols = st.columns(2)
    cols[0].metric(t("market_score"), f"{regime['market_score']}/100")
    cols[1].metric(t("market_regime"), translate_regime(regime["market_regime"]))

    for section, payload in market_indicators().items():
        st.subheader(translate_term(section))
        c1, c2 = st.columns(2)
        c1.metric(t("score"), f"{payload['score']}/100")
        c2.metric(t("status"), translate_term(payload["status"]))
        st.write(f"{t('explanation')}: {translate_text(payload['explanation'])}")
        st.write(f"{t('what_changed')}: {translate_text(payload['what_changed'])}")
        rows = pd.DataFrame(payload["data"])
        columns = ["ticker", "price", "return_5d", "return_1m", "distance_ma_50d", "drawdown_52w", "freshness_status", "confidence"]
        render_interactive_table(rows[[column for column in columns if column in rows]], table_key=f"macro_{section}", lang=lang)
