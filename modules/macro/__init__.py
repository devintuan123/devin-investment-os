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

    st.subheader(t("score_diagnostics"))
    diagnostics = pd.DataFrame(regime.get("score_diagnostics", []))
    if diagnostics.empty:
        st.warning(t("insufficient_data_warning"))
    else:
        display_columns = [
            "component",
            "score",
            "raw_inputs",
            "provider",
            "latest_timestamp",
            "confidence",
            "fallback_used",
            "warning",
            "formula_version",
        ]
        render_interactive_table(diagnostics[[column for column in display_columns if column in diagnostics]], table_key="macro_score_diagnostics", lang=lang)
        for row in regime.get("score_diagnostics", []):
            with st.expander(f"{translate_term(row['component'])}: {row['score']}/100"):
                st.write(f"{t('raw_data')}: {row.get('raw_inputs', '')}")
                st.write(f"{t('source')}: {row.get('provider', '')}")
                st.write(f"{t('latest_timestamp')}: {row.get('latest_timestamp', '')}")
                st.write(f"{t('formula')}: {row.get('formula', '')}")
                st.write(f"{t('weight')}: {row.get('weight', '')}")
                st.write(f"{t('confidence')}: {row.get('confidence', '')}")
                st.write(f"{t('fallback_used')}: {row.get('fallback_used', False)}")
                st.write(f"{t('main_drivers')}: {row.get('warning') or t('no_major_warning')}")

    if regime.get("identical_score_diagnostics"):
        st.warning(t("identical_score_warning"))
        render_interactive_table(pd.DataFrame(regime["identical_score_diagnostics"]), table_key="macro_identical_scores", lang=lang)

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
