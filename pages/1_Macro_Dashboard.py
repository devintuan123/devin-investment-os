import pandas as pd
import streamlit as st

from utils.i18n import t, translate_regime
from utils.indicators import market_indicators
from utils.market_regime import calculate_market_regime
from utils.ui import render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


st.set_page_config(page_title="Macro Dashboard", page_icon="DI", layout="wide")
render_sidebar_language_switch()
render_refresh_button()
render_sidebar_provider_status()

regime = calculate_market_regime()
st.title(t("macro_dashboard"))
st.caption(t("macro_caption"))

cols = st.columns(2)
cols[0].metric(t("market_score"), f"{regime['market_score']}/100")
cols[1].metric(t("market_regime"), translate_regime(regime["market_regime"]))

for section, payload in market_indicators().items():
    st.subheader(section)
    c1, c2 = st.columns(2)
    c1.metric(t("score"), f"{payload['score']}/100")
    c2.metric(t("status"), payload["status"])
    st.write(f"{t('explanation')}: {payload['explanation']}")
    st.write(f"{t('what_changed')}: {payload['what_changed']}")
    rows = pd.DataFrame(payload["data"])
    columns = ["ticker", "price", "return_5d", "return_1m", "distance_ma_50d", "drawdown_52w", "freshness_status", "confidence"]
    st.dataframe(rows[[column for column in columns if column in rows]], use_container_width=True, hide_index=True)
