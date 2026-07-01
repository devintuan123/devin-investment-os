import pandas as pd
import streamlit as st

from utils.data import load_watchlist
from utils.i18n import (
    get_lang,
    render_language_sidebar,
    render_refresh_button,
    t,
    translate_action_label,
    translate_regime,
    translate_warning,
)
from utils.market_regime import calculate_market_regime
from utils.watchlist_scoring import DEFAULT_WATCHLIST, score_watchlist


st.set_page_config(page_title="Daily Playbook", page_icon="DI", layout="wide")
render_language_sidebar()
render_refresh_button()
st.title(t("daily_playbook"))
st.caption(t("daily_caption"))

regime = calculate_market_regime()
watchlist = load_watchlist()
tickers = watchlist["ticker"].dropna().astype(str).tolist() if not watchlist.empty else DEFAULT_WATCHLIST
watch_scores = score_watchlist(tickers)
watch_df = pd.DataFrame(watch_scores)

st.subheader(f"1. {t('market_regime_summary')}")
summary_cols = st.columns(4)
summary_cols[0].metric(t("market_score"), f"{regime['market_score']}/100")
summary_cols[1].metric(t("market_regime"), translate_regime(regime["market_regime"]))
summary_cols[2].metric(t("suggested_action"), translate_action_label(regime["today_action"]))
summary_cols[3].metric(t("confidence"), t(regime["confidence_level"].lower()))
st.write(regime["recommended_action"] if get_lang() == "en" else "核心部位續抱；只在計畫內回檔分批加碼；避免追高延伸標的。")

st.subheader(f"2. {t('what_changed_today')}")
changed_items = regime["what_changed"] if get_lang() == "en" else [
    "SPY 與 QQQ 仍需觀察 20 日與 60 日均線確認。",
    "VIX 低於 18 時較有利風險偏好。",
    "Binance BTCUSDT 唯讀價格可用。",
]
for item in changed_items:
    st.write(f"- {item}")

st.subheader(f"3. {t('what_to_watch')}")
watch_items = regime["what_to_watch"] if get_lang() == "en" else [
    "確認 SPY／QQQ 是否站穩 20 日與 60 日均線。",
    "觀察 VIX 是否維持在 18 以下。",
    "實際交易前請確認券商報價。",
]
for item in watch_items:
    st.write(f"- {item}")

st.subheader(f"4. {t('buy_zone_candidates')}")
buy_zone = watch_df[watch_df["action_label"].eq("Potential buy zone - verify quote")].head(5)
pullback = watch_df[watch_df["action_label"].eq("Pullback watch")].head(5)
if buy_zone.empty and pullback.empty:
    st.write("- No clean buy-zone candidates. Watch / wait." if get_lang() == "en" else "- 尚無明確買進區候選，先觀察等待。")
else:
    for _, row in pd.concat([buy_zone, pullback]).head(8).iterrows():
        st.write(f"- {row['ticker']}: {translate_action_label(row['action_label'])} ({row['distance_ma20_pct']:.1f}% vs MA20)")

st.subheader(f"5. {t('risk_warnings')}")
for item in regime["risk_warnings"]:
    st.warning(item if get_lang() == "en" else "目前沒有重大風險趨避觸發，但資料仍僅供決策輔助。")
for warning in regime["warnings"]:
    if "Taiwan stock data" in warning:
        st.warning(translate_warning(warning))
extended = watch_df[watch_df["action_label"].eq("Extended / Do not chase")].head(5)
for _, row in extended.iterrows():
    st.warning(f"{row['ticker']}: {translate_action_label('Extended / Do not chase')}")

st.subheader(f"6. {t('suggested_action')}")
suggestions = (
    [
        regime["recommended_action"],
        "Buy only in layers; never chase vertical moves.",
        "DCA core ETFs only when market confidence is not High.",
        "Raise cash if VIX confirms risk-off.",
    ]
    if get_lang() == "en"
    else [
        "核心部位續抱；只在計畫內回檔分批加碼。",
        "只分層買進，不追高急漲標的。",
        "資料信心不足時只定期定額核心 ETF。",
        "若 VIX 確認風險趨避，應提高現金部位。",
    ]
)
for item in suggestions:
    st.write(f"- {item}")

st.subheader(f"7. {t('telegram_ready_summary')}")
top_signals = watch_df[["ticker", "action_label"]].head(3).to_dict("records") if not watch_df.empty else []
if get_lang() == "en":
    telegram_summary = "\n".join(
        [
            "Devin Investment OS Daily Playbook",
            f"Market Score: {regime['market_score']}/100",
            f"Regime: {regime['market_regime']}",
            f"Action: {regime['today_action']}",
            f"VIX: {regime['key_metrics'].get('VIX')}",
            "Top Watchlist Signals:",
            *[f"- {item['ticker']}: {item['action_label']}" for item in top_signals],
            "Risk Warning: decision-support only; verify broker quote before trading.",
        ]
    )
else:
    telegram_summary = "\n".join(
        [
            "Devin 投資作業系統每日作戰計畫",
            f"市場分數：{regime['market_score']}/100",
            f"市場狀態：{translate_regime(regime['market_regime'])}",
            f"行動：{translate_action_label(regime['today_action'])}",
            f"VIX：{regime['key_metrics'].get('VIX')}",
            "觀察清單訊號：",
            *[f"- {item['ticker']}：{translate_action_label(item['action_label'])}" for item in top_signals],
            "風險警示：資料僅供決策輔助；交易前請確認券商報價。",
        ]
    )
st.code(telegram_summary, language="text")
