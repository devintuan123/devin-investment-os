from __future__ import annotations

from utils.ui import get_current_lang, render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


def render_page_shell() -> str:
    render_sidebar_language_switch()
    render_refresh_button()
    render_sidebar_provider_status()
    return get_current_lang()
