from __future__ import annotations

import streamlit as st

from utils.i18n import LANG_EN, LANG_ZH, get_lang, set_lang, t
from utils.provider_status import active_provider_rows


def get_current_lang() -> str:
    return get_lang()


def render_sidebar_language_switch() -> None:
    st.sidebar.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    labels = {LANG_ZH: t("traditional_chinese"), LANG_EN: t("english")}
    current = get_lang()
    selected = st.sidebar.radio(
        t("language"),
        options=[LANG_ZH, LANG_EN],
        format_func=lambda value: labels[value],
        index=[LANG_ZH, LANG_EN].index(current),
    )
    set_lang(selected)
    render_sidebar_navigation()


def render_sidebar_navigation() -> None:
    st.sidebar.subheader(t("navigation"))
    links = [
        ("app.py", "home"),
        ("pages/1_Macro_Dashboard.py", "macro_dashboard"),
        ("pages/2_Portfolio.py", "portfolio"),
        ("pages/3_Watchlist.py", "watchlist"),
        ("pages/5_Asset_Scores.py", "asset_scores"),
        ("pages/6_Daily_Playbook.py", "daily_playbook"),
        ("pages/10_Buy_Zones.py", "buy_zones"),
        ("pages/11_Sector_Heat.py", "sector_heat_page"),
        ("pages/7_History.py", "history"),
        ("pages/9_Data_Quality.py", "data_quality"),
        ("pages/4_Settings.py", "settings"),
    ]
    for target, label_key in links:
        st.sidebar.page_link(target, label=t(label_key))


def render_sidebar_provider_status() -> None:
    with st.sidebar.expander(t("provider_status"), expanded=False):
        for row in active_provider_rows():
            st.write(f"{row['Provider']}: {row['Status']}")


def render_refresh_button() -> None:
    if st.sidebar.button(t("refresh_data"), use_container_width=True):
        st.cache_data.clear()
        st.rerun()
