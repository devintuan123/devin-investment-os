from __future__ import annotations

import streamlit as st

from modules.shared.styles import apply_global_styles
from utils.ui import get_current_lang, render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


def configure_page(title: str = "Devin Investment OS") -> None:
    st.set_page_config(page_title=title, page_icon="DI", layout="wide")
    apply_global_styles()


def render_page_shell() -> str:
    apply_global_styles()
    render_sidebar_language_switch()
    render_refresh_button()
    render_sidebar_provider_status()
    return get_current_lang()
