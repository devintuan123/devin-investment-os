from __future__ import annotations

import streamlit as st

from modules.shared.tables import render_interactive_table
from utils.i18n import t
from utils.sector_heat_engine import calculate_theme_heat_score, fetch_theme_prices, get_candidate_symbols_by_theme


def render(lang: str) -> None:
    st.title(t("sector_heat_page"))
    st.caption(t("proxy_heat_warning"))

    with st.spinner(t("loading")):
        symbol_rows = fetch_theme_prices()
        theme_scores = calculate_theme_heat_score(symbol_rows)
        candidates = get_candidate_symbols_by_theme()

    if theme_scores.empty:
        st.info(t("no_data"))
        return

    summary_cols = st.columns(4)
    summary_cols[0].metric(t("hot_themes"), int((theme_scores["heat_label"] == "Hot / Extended").sum()))
    summary_cols[1].metric(t("rotation_in"), int((theme_scores["rotation_label"] == "Rotation In").sum()))
    summary_cols[2].metric(t("cooling"), int((theme_scores["heat_label"] == "Cooling").sum()))
    summary_cols[3].metric(t("candidate_list"), len(candidates))

    st.warning(t("proxy_heat_warning"))

    tabs = st.tabs([t("summary"), "US", t("taiwan"), "UCITS", t("candidate_list")])
    with tabs[0]:
        st.subheader(t("hot_themes"))
        render_interactive_table(theme_scores, table_key="sector_heat_summary", lang=lang, default_sort=t("heat_score"))
    with tabs[1]:
        render_interactive_table(theme_scores[theme_scores["market"] == "US"], table_key="sector_heat_us", lang=lang)
    with tabs[2]:
        render_interactive_table(theme_scores[theme_scores["market"] == "Taiwan"], table_key="sector_heat_taiwan", lang=lang)
    with tabs[3]:
        render_interactive_table(theme_scores[theme_scores["market"] == "LSE"], table_key="sector_heat_ucits", lang=lang)
    with tabs[4]:
        render_interactive_table(candidates, table_key="sector_heat_candidates", lang=lang)
