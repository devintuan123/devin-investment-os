import pandas as pd
import streamlit as st

from utils.config import is_configured
from utils.i18n import t, translate_regime, translate_warning
from utils.interactive_table import render_interactive_table
from utils.market_data import safe_fetch_with_fallback
from utils.market_regime import calculate_market_regime
from utils.provider_status import future_disabled_provider_rows
from utils.tw_market_time import get_tw_market_session_label, get_tw_next_session_hint, is_tw_market_open
from utils.ui import get_current_lang, render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status
from utils.watchlist_scoring import DEFAULT_WATCHLIST


def render(lang: str) -> None:
    def _provider_configured(provider: str) -> bool:
        if provider == "yfinance":
            return True
        if provider == "Binance":
            return is_configured("BINANCE_API_KEY", "BINANCE_API_SECRET")
        if provider == "FRED":
            return is_configured("FRED_API_KEY")
        if provider == "Telegram":
            return is_configured("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID")
        return False


    def _provider_connected(row: dict) -> bool:
        latest = str(row.get("Latest successful fetch", "")).lower()
        return latest not in {"", "unavailable", "none"} and "unavailable" not in latest



    regime = calculate_market_regime()
    st.title(t("data_quality"))
    st.caption(t("read_only_notice"))

    st.subheader(t("market_session_status"))
    session_cols = st.columns(3)
    session_cols[0].metric("TWSE", get_tw_market_session_label())
    session_cols[1].metric(t("active"), t("yes") if is_tw_market_open() else t("no"))
    session_cols[2].write(get_tw_next_session_hint())

    st.subheader(t("provider_status"))
    quality_rows = []
    for row in regime["provider_quality"]:
        provider = row["Provider"]
        quality_rows.append({t("provider"): provider, t("configured"): t("yes") if _provider_configured(provider) else t("no"), t("connected"): t("yes") if _provider_connected(row) else t("no"), t("latest_successful_fetch"): row.get("Latest successful fetch"), t("freshness"): row.get("Freshness"), t("confidence"): row.get("Confidence"), t("warning"): translate_warning(row.get("Warning", ""))})
    render_interactive_table(pd.DataFrame(quality_rows), table_key="data_quality_providers", lang=lang)

    st.subheader(t("freshness"))
    ticker_rows = []
    for ticker in DEFAULT_WATCHLIST:
        quote = safe_fetch_with_fallback(ticker)
        ticker_rows.append({t("ticker"): ticker, t("provider"): quote.get("provider_label") or quote.get("source"), t("latest_price_label"): quote.get("price"), t("fetch_time"): quote.get("fetch_timestamp"), t("quote_time"): quote.get("quote_timestamp"), t("market_session_status"): get_tw_market_session_label() if ticker.endswith(".TW") else "n/a", t("freshness_status"): quote.get("freshness_status"), t("confidence"): quote.get("confidence"), t("warning"): translate_warning(quote.get("provider_warning", ""))})
    render_interactive_table(pd.DataFrame(ticker_rows), table_key="data_quality_tickers", lang=lang)

    st.subheader(t("overall_confidence"))
    cols = st.columns(4)
    cols[0].metric(t("overall_confidence"), t(regime["confidence_level"].lower()))
    cols[1].metric(t("confidence_score"), f"{regime['confidence_score']}/100")
    cols[2].metric(t("market_score"), f"{regime['market_score']}/100")
    cols[3].metric(t("market_regime"), translate_regime(regime["market_regime"]))

    st.subheader(t("warnings"))
    for warning in regime["warnings"]:
        st.warning(translate_warning(warning))

    with st.expander(t("future_disabled_providers"), expanded=False):
        render_interactive_table(pd.DataFrame(future_disabled_provider_rows()), table_key="data_quality_disabled", lang=lang)
        st.write(t("read_only_notice"))
