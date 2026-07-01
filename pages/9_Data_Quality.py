import pandas as pd
import streamlit as st

from utils.config import is_configured
from utils.i18n import (
    get_lang,
    render_language_sidebar,
    render_refresh_button,
    t,
    translate_regime,
    translate_warning,
)
from utils.market_data import safe_fetch_with_fallback
from utils.market_regime import calculate_market_regime
from utils.provider_status import future_disabled_provider_rows
from utils.tw_market_time import get_tw_market_session_label, get_tw_next_session_hint, is_tw_market_open
from utils.watchlist_scoring import DEFAULT_WATCHLIST


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


st.set_page_config(page_title="Data Quality", page_icon="DI", layout="wide")
render_language_sidebar()
render_refresh_button()
st.title(t("data_quality"))
st.caption(
    "Read-only provider freshness, confidence, and warnings."
    if get_lang() == "en"
    else "唯讀資料來源新鮮度、信心與警示。"
)

regime = calculate_market_regime()

st.subheader(t("market_session_status"))
session_cols = st.columns(3)
session_cols[0].metric("TWSE", get_tw_market_session_label())
session_cols[1].metric("Open", "Yes" if is_tw_market_open() else "No")
session_cols[2].write(get_tw_next_session_hint())

st.subheader(t("data_quality"))
quality_rows = []
for row in regime["provider_quality"]:
    provider = row["Provider"]
    quality_rows.append(
        {
            t("provider"): provider,
            t("configured"): "Yes" if _provider_configured(provider) else "No",
            t("connected"): "Yes" if _provider_connected(row) else "No",
            t("latest_successful_fetch"): row.get("Latest successful fetch"),
            t("freshness"): row.get("Freshness"),
            t("confidence"): row.get("Confidence"),
            t("warning"): translate_warning(row.get("Warning", "")),
        }
    )
st.dataframe(pd.DataFrame(quality_rows), use_container_width=True, hide_index=True)

st.subheader("Ticker / Provider Freshness" if get_lang() == "en" else "個股／資料來源新鮮度")
ticker_rows = []
for ticker in DEFAULT_WATCHLIST:
    quote = safe_fetch_with_fallback(ticker)
    ticker_rows.append(
        {
            t("ticker"): ticker,
            t("provider"): quote.get("provider_label") or quote.get("source"),
            t("latest_price_label"): quote.get("price"),
            t("fetch_time"): quote.get("fetch_timestamp"),
            t("quote_time"): quote.get("quote_timestamp"),
            t("market_session_status"): get_tw_market_session_label() if ticker.endswith(".TW") else "n/a",
            t("freshness_status"): quote.get("freshness_status"),
            t("confidence"): quote.get("confidence"),
            t("warning"): translate_warning(quote.get("provider_warning", "")),
        }
    )
st.dataframe(pd.DataFrame(ticker_rows), use_container_width=True, hide_index=True)

st.subheader(t("source_hierarchy"))
if get_lang() == "en":
    st.write("- Crypto: Binance read-only > yfinance > fallback")
    st.write("- Stocks / ETFs / Taiwan / gold: yfinance delayed / best-effort > fallback")
    st.write("- Macro: FRED daily / lagged")
    st.write("- Notifications: Telegram outbound only")
else:
    st.write("- 加密貨幣：Binance 唯讀 > yfinance > 備援")
    st.write("- 股票／ETF／台股／黃金：yfinance 延遲或盡力資料 > 備援")
    st.write("- 總經：FRED 每日或落後資料")
    st.write("- 通知：Telegram 僅外送通知")

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
    future_df = pd.DataFrame(future_disabled_provider_rows())
    st.dataframe(future_df, use_container_width=True, hide_index=True)
    st.write(
        "These providers remain disabled unless explicitly requested."
        if get_lang() == "en"
        else "這些資料來源維持停用，除非使用者明確要求啟用。"
    )
