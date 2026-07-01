import pandas as pd
import streamlit as st

from utils.i18n import t, translate_action_label
from utils.market_regime import calculate_market_regime
from utils.table_i18n import translate_dataframe
from utils.ui import get_current_lang, render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


st.set_page_config(page_title="Asset Scores", page_icon="DI", layout="wide")
render_sidebar_language_switch()
render_refresh_button()
render_sidebar_provider_status()

regime = calculate_market_regime()
lang = get_current_lang()
st.title(t("asset_scores"))
st.caption(t("asset_scores_caption"))

rows = []
for name, score in regime["components"].items():
    rows.append({"category": name, "score": score, "status": regime["market_regime"], "action": regime["today_action"]})
df = pd.DataFrame(rows)

cols = st.columns(4)
cols[0].metric(t("best_score"), max(regime["components"], key=regime["components"].get))
cols[1].metric(t("risk_watch"), t("risk_warnings"))
cols[2].metric(t("core_bias"), translate_action_label("Hold"))
cols[3].metric(t("action"), translate_action_label(regime["today_action"]))

st.dataframe(translate_dataframe(df, lang), use_container_width=True, hide_index=True)
st.warning(t("broker_warning"))
