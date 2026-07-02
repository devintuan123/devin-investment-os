import pandas as pd
import streamlit as st

from utils.i18n import t, translate_regime, translate_term, translate_text
from utils.interactive_table import render_interactive_table
from utils.indicators import market_indicators
from utils.fred_provider import get_macro_series_snapshot
from utils.market_data import get_market_proxy_snapshot
from utils.market_regime import calculate_market_regime
from utils.scoring_diagnostics import build_score_diagnostics, detect_missing_macro_inputs, summarize_score_data_quality
from utils.ui import get_current_lang, render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


def render(lang: str) -> None:
    regime = calculate_market_regime()
    fred_snapshot = get_macro_series_snapshot()
    proxy_snapshot = get_market_proxy_snapshot()
    score_diagnostics = build_score_diagnostics(lang)
    quality = summarize_score_data_quality()
    missing_inputs = detect_missing_macro_inputs()
    st.title(t("macro_dashboard"))
    st.caption(t("macro_caption"))

    if missing_inputs:
        st.warning(t("macro_missing_data_warning"))
        for item in missing_inputs[:6]:
            st.write(f"- {item['provider']} {item['item']}: {item['warning']}")

    cols = st.columns(2)
    cols[0].metric(t("market_score"), f"{regime['market_score']}/100")
    cols[1].metric(t("market_regime"), translate_regime(regime["market_regime"]))

    st.subheader(f"{t('macro_data_status')} / Macro Data Status")
    status_cols = st.columns(4)
    status_cols[0].metric("FRED", t("connected") if quality["fred_connected"] else t("disconnected"))
    status_cols[1].metric("yfinance", t("connected") if quality["yfinance_connected"] else t("disconnected"))
    status_cols[2].metric("Binance", "BTCUSDT" if "BTC" in regime.get("key_metrics", {}) else t("available"))
    status_cols[3].metric(t("data_confidence"), f"{quality['confidence']}/100")
    st.write(
        f"{t('latest_timestamp')}: {_latest_macro_date(fred_snapshot, proxy_snapshot)} | "
        f"{t('available')}: {quality['valid_rows']} | {t('missing')}: {quality['missing_rows']} | "
        f"{t('fallback_used')}: {quality['fallback_rows']}"
    )

    st.subheader(f"{t('fred_raw_data')} / FRED Raw Data")
    if fred_snapshot.empty:
        st.error("FRED returned zero diagnostic rows.")
    else:
        render_interactive_table(
            fred_snapshot[
                [
                    "label",
                    "series_id",
                    "latest_date",
                    "latest_value",
                    "change",
                    "provider",
                    "freshness_status",
                    "confidence",
                    "fallback_used",
                    "error",
                ]
            ],
            table_key="macro_fred_raw_data",
            lang=lang,
        )

    st.subheader(f"{t('market_proxy_data')} / Market Proxy Data")
    if proxy_snapshot.empty:
        st.error("yfinance market proxy provider returned zero diagnostic rows.")
    else:
        render_interactive_table(
            proxy_snapshot[
                [
                    "label",
                    "symbol",
                    "latest_date",
                    "latest_price",
                    "return_5d",
                    "return_20d",
                    "ma20",
                    "ma60",
                    "provider",
                    "freshness_status",
                    "confidence",
                    "fallback_used",
                    "error",
                ]
            ],
            table_key="macro_market_proxy_data",
            lang=lang,
        )

    st.subheader(t("score_diagnostics"))
    diagnostics = score_diagnostics if not score_diagnostics.empty else pd.DataFrame(regime.get("score_diagnostics", []))
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


def _latest_macro_date(fred_snapshot: pd.DataFrame, proxy_snapshot: pd.DataFrame) -> str:
    values = []
    for frame, column in [(fred_snapshot, "latest_date"), (proxy_snapshot, "latest_date")]:
        if not frame.empty and column in frame:
            values.extend([str(value) for value in frame[column].dropna().tolist() if str(value)])
    return max(values) if values else "unavailable"
