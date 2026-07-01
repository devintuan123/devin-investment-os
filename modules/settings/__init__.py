import pandas as pd
import streamlit as st

from utils.config import safety_status
from utils.i18n import t
from utils.interactive_table import render_interactive_table
from utils.provider_status import active_provider_rows, future_disabled_provider_rows
from utils.telegram import send_telegram_message
from utils.ui import get_current_lang, render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


def render(lang: str) -> None:
    st.title(t("settings"))
    st.caption(t("settings_caption"))

    st.subheader(t("api_configuration"))
    active_rows = active_provider_rows()
    metric_cols = st.columns(4)
    for index, row in enumerate(active_rows):
        metric_cols[index].metric(row["Provider"], row["Status"])

    st.write(t("active_providers"))
    render_interactive_table(pd.DataFrame(active_rows), table_key="settings_active_providers", lang=lang)
    st.write(t("disabled_providers"))
    render_interactive_table(pd.DataFrame(future_disabled_provider_rows()), table_key="settings_disabled_providers", lang=lang)

    st.subheader(t("safety_status"))
    safety = safety_status()
    safe_cols = st.columns(5)
    safe_cols[0].checkbox(t("trading_disabled"), value=safety["trading_disabled"], disabled=True)
    safe_cols[1].checkbox(t("withdrawals_disabled"), value=safety["withdrawals_disabled"], disabled=True)
    safe_cols[2].checkbox(t("futures_disabled"), value=safety["futures_disabled"], disabled=True)
    safe_cols[3].checkbox(t("margin_disabled"), value=safety["margin_disabled"], disabled=True)
    safe_cols[4].checkbox(t("auto_order_disabled"), value=safety["auto_order_disabled"], disabled=True)
    for warning in safety["warnings"]:
        st.warning(warning)

    st.subheader(t("provider_strategy"))
    st.write(t("read_only_notice"))
    st.write(" / ".join(["yfinance", "Binance", "FRED", "Telegram"]))

    st.subheader(t("telegram_test"))
    message = st.text_area(t("telegram_ready_summary"), value=t("telegram_test_default"))
    if st.button(t("send_test_message"), use_container_width=True):
        st.success(t("sent")) if send_telegram_message(message) else st.warning(t("skipped_check_config"))

    st.subheader(t("security_notes"))
    st.write(t("broker_warning"))
    st.write(t("read_only_notice"))
