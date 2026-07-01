from __future__ import annotations

import streamlit as st

from utils.i18n import LANG_EN, LANG_ZH, get_lang, set_lang, t
from utils.provider_status import active_provider_rows


def get_current_lang() -> str:
    return get_lang()


def render_sidebar_language_switch() -> None:
    labels = {LANG_ZH: t("traditional_chinese"), LANG_EN: t("english")}
    current = get_lang()
    selected = st.sidebar.radio(
        t("language"),
        options=[LANG_ZH, LANG_EN],
        format_func=lambda value: labels[value],
        index=[LANG_ZH, LANG_EN].index(current),
    )
    set_lang(selected)


def render_sidebar_provider_status() -> None:
    with st.sidebar.expander(t("provider_status"), expanded=False):
        for row in active_provider_rows():
            st.write(f"{row['Provider']}: {row['Status']}")


def render_refresh_button() -> None:
    if st.sidebar.button(t("refresh_data"), use_container_width=True):
        st.cache_data.clear()
        st.rerun()
