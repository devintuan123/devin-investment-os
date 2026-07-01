from __future__ import annotations


LANG_ZH = "zh"
LANG_EN = "en"
SUPPORTED_LANGS = {LANG_ZH, LANG_EN}
_fallback_lang = LANG_ZH


TRANSLATIONS = {
    LANG_EN: {
        "language": "Language",
        "traditional_chinese": "Traditional Chinese",
        "english": "English",
        "refresh_data": "Refresh Data",
        "app_title": "Devin Investment OS",
        "app_caption": "Read-only market regime, portfolio risk, watchlist zones, and daily playbook.",
        "market_score": "Market Score",
        "market_regime": "Market Regime",
        "today_action": "Today Action",
        "data_confidence": "Data Confidence",
        "active_provider_status": "Active Provider Status",
        "market_components": "Market Components",
        "recommended_action": "Recommended Action",
        "what_changed_today": "What Changed Today",
        "warnings": "Warnings",
        "watchlist": "Watchlist",
        "watchlist_decision_signals": "Watchlist Decision Signals",
        "quick_portfolio": "Quick Portfolio",
        "navigation": "Navigation",
        "daily_playbook": "Daily Playbook",
        "data_quality": "Data Quality",
        "settings": "Settings",
        "macro": "Macro",
        "portfolio": "Portfolio",
        "asset_scores": "Asset Scores",
        "history": "History",
        "tv_alerts": "TradingView Alerts",
        "decision_scoring": "Decision Scoring",
        "category": "Category",
        "signal": "Signal",
        "save_watchlist": "Save Watchlist",
        "watchlist_saved": "Watchlist saved.",
        "all": "All",
        "ticker": "Ticker",
        "latest_price": "Latest Price",
        "ma20": "MA20",
        "ma60": "MA60",
        "ma120": "MA120",
        "drawdown_52w_pct": "52W Drawdown %",
        "trend_score": "Trend Score",
        "pullback_score": "Pullback Score",
        "action_label": "Action Label",
        "risk_label": "Risk Label",
        "delayed_verify_broker_quote": "Delayed / verify broker quote",
        "tw_reference_warning": "Taiwan stock data is reference-only. Do not use for execution.",
        "daily_caption": "Read-only daily decision support. Verify broker quotes before real trading.",
        "market_regime_summary": "Market Regime Summary",
        "what_to_watch": "What To Watch",
        "buy_zone_candidates": "Buy-Zone Candidates",
        "risk_warnings": "Risk Warnings",
        "suggested_action": "Suggested Action",
        "telegram_ready_summary": "Telegram-Ready Summary",
        "provider": "Provider",
        "latest_successful_fetch": "Latest Successful Fetch",
        "freshness": "Freshness",
        "confidence": "Confidence",
        "warning": "Warning",
        "configured": "Configured",
        "connected": "Connected",
        "market_session_status": "Market Session Status",
        "fetch_time": "Fetch Time",
        "quote_time": "Quote Time",
        "latest_price_label": "Latest Price",
        "freshness_status": "Freshness Status",
        "future_disabled_providers": "Future / Disabled Providers",
        "source_hierarchy": "Source Hierarchy",
        "overall_confidence": "Overall Confidence",
        "confidence_score": "Confidence Score",
        "risk_on": "Risk-On",
        "neutral": "Neutral",
        "risk_off": "Risk-Off",
        "potential_buy_zone": "Potential buy zone - verify quote",
        "extended_do_not_chase": "Extended / Do not chase",
        "healthy_trend_hold": "Healthy trend / Hold",
        "pullback_watch": "Pullback watch",
        "broken_trend_avoid": "Broken trend / Avoid",
        "aggressive_buy_zone": "Aggressive Buy Zone",
        "gradual_buy_zone": "Gradual Buy Zone",
        "hold_dca_only": "Hold / DCA Only",
        "watch_wait": "Watch / Wait",
        "reduce_risk": "Reduce Risk",
        "high": "High",
        "elevated": "Elevated",
        "moderate": "Moderate",
        "balanced": "Balanced",
        "available": "Available",
        "missing": "Missing",
        "not_configured": "Not configured",
        "future_disabled": "Future disabled",
        "no_holdings": "No holdings found.",
        "no_watchlist": "No watchlist items found.",
        "tw_warning_full": "Taiwan stock data is reference-only. Do not use for execution.",
        "yf_warning": "yfinance data may be delayed or best-effort.",
        "fred_warning": "FRED macro data may be daily or lagged.",
        "broker_warning": "Verify broker quote before actual trading.",
    },
    LANG_ZH: {
        "language": "\u8a9e\u8a00",
        "traditional_chinese": "\u7e41\u9ad4\u4e2d\u6587",
        "english": "English",
        "refresh_data": "\u91cd\u65b0\u6574\u7406\u8cc7\u6599",
        "app_title": "Devin \u6295\u8cc7\u4f5c\u696d\u7cfb\u7d71",
        "app_caption": "\u552f\u8b80\u5e02\u5834\u72c0\u614b\u3001\u6295\u8cc7\u7d44\u5408\u98a8\u96aa\u3001\u89c0\u5bdf\u6e05\u55ae\u5340\u9593\u8207\u6bcf\u65e5\u4f5c\u6230\u8a08\u756b\u3002",
        "market_score": "\u5e02\u5834\u5206\u6578",
        "market_regime": "\u5e02\u5834\u72c0\u614b",
        "today_action": "\u4eca\u65e5\u5efa\u8b70\u884c\u52d5",
        "data_confidence": "\u8cc7\u6599\u4fe1\u5fc3",
        "active_provider_status": "\u555f\u7528\u8cc7\u6599\u4f86\u6e90\u72c0\u614b",
        "market_components": "\u5e02\u5834\u7d44\u6210\u5206\u6578",
        "recommended_action": "\u5efa\u8b70\u884c\u52d5",
        "what_changed_today": "\u4eca\u65e5\u8b8a\u5316",
        "warnings": "\u8b66\u793a",
        "watchlist": "\u89c0\u5bdf\u6e05\u55ae",
        "watchlist_decision_signals": "\u89c0\u5bdf\u6e05\u55ae\u6c7a\u7b56\u8a0a\u865f",
        "quick_portfolio": "\u6295\u8cc7\u7d44\u5408\u901f\u89bd",
        "navigation": "\u5c0e\u89bd",
        "daily_playbook": "\u6bcf\u65e5\u4f5c\u6230\u8a08\u756b",
        "data_quality": "\u8cc7\u6599\u54c1\u8cea",
        "settings": "\u8a2d\u5b9a",
        "macro": "\u7e3d\u7d93",
        "portfolio": "\u6295\u8cc7\u7d44\u5408",
        "asset_scores": "\u8cc7\u7522\u5206\u6578",
        "history": "\u6b77\u53f2",
        "tv_alerts": "TradingView \u8b66\u793a",
        "decision_scoring": "\u6c7a\u7b56\u8a55\u5206",
        "category": "\u5206\u985e",
        "signal": "\u8a0a\u865f",
        "save_watchlist": "\u5132\u5b58\u89c0\u5bdf\u6e05\u55ae",
        "watchlist_saved": "\u89c0\u5bdf\u6e05\u55ae\u5df2\u5132\u5b58\u3002",
        "all": "\u5168\u90e8",
        "ticker": "\u4ee3\u865f",
        "latest_price": "\u6700\u65b0\u50f9\u683c",
        "ma20": "20 \u65e5\u5747\u7dda",
        "ma60": "60 \u65e5\u5747\u7dda",
        "ma120": "120 \u65e5\u5747\u7dda",
        "drawdown_52w_pct": "\u8ddd 52 \u9031\u9ad8\u9ede\u8dcc\u5e45 %",
        "trend_score": "\u8da8\u52e2\u5206\u6578",
        "pullback_score": "\u56de\u6a94\u5206\u6578",
        "action_label": "\u884c\u52d5\u6a19\u7c64",
        "risk_label": "\u98a8\u96aa\u6a19\u7c64",
        "delayed_verify_broker_quote": "\u5ef6\u9072\uff0f\u8acb\u5411\u5238\u5546\u78ba\u8a8d\u5831\u50f9",
        "tw_reference_warning": "\u53f0\u80a1\u8cc7\u6599\u50c5\u4f9b\u53c3\u8003\uff0c\u4e0d\u53ef\u7528\u65bc\u4e0b\u55ae\u57f7\u884c\u3002",
        "daily_caption": "\u552f\u8b80\u6bcf\u65e5\u6c7a\u7b56\u8f14\u52a9\u3002\u5be6\u969b\u4ea4\u6613\u524d\u8acb\u78ba\u8a8d\u5238\u5546\u5831\u50f9\u3002",
        "market_regime_summary": "\u5e02\u5834\u72c0\u614b\u6458\u8981",
        "what_to_watch": "\u89c0\u5bdf\u91cd\u9ede",
        "buy_zone_candidates": "\u8cb7\u9032\u5340\u5019\u9078",
        "risk_warnings": "\u98a8\u96aa\u8b66\u793a",
        "suggested_action": "\u5efa\u8b70\u884c\u52d5",
        "telegram_ready_summary": "Telegram \u6458\u8981",
        "provider": "\u8cc7\u6599\u4f86\u6e90",
        "latest_successful_fetch": "\u6700\u8fd1\u6210\u529f\u6293\u53d6",
        "freshness": "\u65b0\u9bae\u5ea6",
        "confidence": "\u4fe1\u5fc3",
        "warning": "\u8b66\u793a",
        "configured": "\u5df2\u8a2d\u5b9a",
        "connected": "\u5df2\u9023\u7dda",
        "market_session_status": "\u5e02\u5834\u4ea4\u6613\u6642\u6bb5",
        "fetch_time": "\u6293\u53d6\u6642\u9593",
        "quote_time": "\u5831\u50f9\u6642\u9593",
        "latest_price_label": "\u6700\u65b0\u50f9\u683c",
        "freshness_status": "\u65b0\u9bae\u5ea6\u72c0\u614b",
        "future_disabled_providers": "\u672a\u4f86\uff0f\u505c\u7528\u8cc7\u6599\u4f86\u6e90",
        "source_hierarchy": "\u8cc7\u6599\u4f86\u6e90\u512a\u5148\u9806\u5e8f",
        "overall_confidence": "\u6574\u9ad4\u4fe1\u5fc3",
        "confidence_score": "\u4fe1\u5fc3\u5206\u6578",
        "risk_on": "\u98a8\u96aa\u504f\u597d",
        "neutral": "\u4e2d\u6027",
        "risk_off": "\u98a8\u96aa\u8da8\u907f",
        "potential_buy_zone": "\u6f5b\u5728\u8cb7\u9032\u5340\uff0c\u8acb\u78ba\u8a8d\u5831\u50f9",
        "extended_do_not_chase": "\u6f32\u5e45\u5ef6\u4f38\uff0c\u52ff\u8ffd\u9ad8",
        "healthy_trend_hold": "\u8da8\u52e2\u5065\u5eb7\uff0c\u6301\u6709",
        "pullback_watch": "\u56de\u6a94\u89c0\u5bdf",
        "broken_trend_avoid": "\u8da8\u52e2\u8f49\u5f31\uff0c\u907f\u514d",
        "aggressive_buy_zone": "\u7a4d\u6975\u8cb7\u9032\u5340",
        "gradual_buy_zone": "\u5206\u6279\u8cb7\u9032\u5340",
        "hold_dca_only": "\u6301\u6709\uff0f\u50c5\u5b9a\u671f\u5b9a\u984d",
        "watch_wait": "\u89c0\u5bdf\uff0f\u7b49\u5f85",
        "reduce_risk": "\u964d\u4f4e\u98a8\u96aa",
        "high": "\u9ad8",
        "elevated": "\u504f\u9ad8",
        "moderate": "\u4e2d\u7b49",
        "balanced": "\u5e73\u8861",
        "available": "\u53ef\u7528",
        "missing": "\u7f3a\u5c11\u8a2d\u5b9a",
        "not_configured": "\u672a\u8a2d\u5b9a",
        "future_disabled": "\u672a\u4f86\u505c\u7528",
        "no_holdings": "\u5c1a\u7121\u6301\u80a1\u8cc7\u6599\u3002",
        "no_watchlist": "\u5c1a\u7121\u89c0\u5bdf\u6e05\u55ae\u8cc7\u6599\u3002",
        "tw_warning_full": "\u53f0\u80a1\u8cc7\u6599\u50c5\u4f9b\u53c3\u8003\uff0c\u4e0d\u53ef\u7528\u65bc\u4e0b\u55ae\u57f7\u884c\u3002",
        "yf_warning": "yfinance \u8cc7\u6599\u53ef\u80fd\u5ef6\u9072\uff0c\u50c5\u4f9b\u53c3\u8003\u3002",
        "fred_warning": "FRED \u7e3d\u7d93\u8cc7\u6599\u53ef\u80fd\u70ba\u6bcf\u65e5\u66f4\u65b0\u6216\u843d\u5f8c\u8cc7\u6599\u3002",
        "broker_warning": "\u5be6\u969b\u4ea4\u6613\u524d\u8acb\u78ba\u8a8d\u5238\u5546\u5831\u50f9\u3002",
    },
}

ACTION_LABEL_KEYS = {
    "Potential buy zone - verify quote": "potential_buy_zone",
    "Extended / Do not chase": "extended_do_not_chase",
    "Healthy trend / Hold": "healthy_trend_hold",
    "Pullback watch": "pullback_watch",
    "Broken trend / Avoid": "broken_trend_avoid",
    "Aggressive Buy Zone": "aggressive_buy_zone",
    "Gradual Buy Zone": "gradual_buy_zone",
    "Hold / DCA Only": "hold_dca_only",
    "Watch / Wait": "watch_wait",
    "Reduce Risk": "reduce_risk",
}

RISK_LABEL_KEYS = {"High": "high", "Elevated": "elevated", "Moderate": "moderate", "Balanced": "balanced"}
REGIME_KEYS = {"Risk-On": "risk_on", "Neutral": "neutral", "Risk-Off": "risk_off"}


def get_lang() -> str:
    try:
        import streamlit as st
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        if get_script_run_ctx() is None:
            return _fallback_lang
        return st.session_state.get("lang", _fallback_lang)
    except Exception:
        return _fallback_lang


def set_lang(lang: str) -> None:
    global _fallback_lang
    if lang not in SUPPORTED_LANGS:
        lang = LANG_ZH
    _fallback_lang = lang
    try:
        import streamlit as st
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        if get_script_run_ctx() is None:
            return
        st.session_state["lang"] = lang
    except Exception:
        pass


def t(key: str) -> str:
    lang = get_lang()
    return TRANSLATIONS.get(lang, TRANSLATIONS[LANG_ZH]).get(key, TRANSLATIONS[LANG_EN].get(key, key))


def translate_action_label(label: str) -> str:
    return t(ACTION_LABEL_KEYS.get(label, label))


def translate_risk_label(label: str) -> str:
    return t(RISK_LABEL_KEYS.get(label, label))


def translate_regime(label: str) -> str:
    return t(REGIME_KEYS.get(label, label))


def translate_status(label: str) -> str:
    key = str(label or "").lower().replace(" ", "_").replace("/", "_")
    return t(key)


def translate_warning(message: str) -> str:
    text = str(message or "")
    if "Taiwan stock data is reference-only" in text:
        return t("tw_warning_full")
    if "yfinance data may be delayed" in text:
        return t("yf_warning")
    if "FRED macro data may be daily" in text:
        return t("fred_warning")
    if "Verify broker quote" in text:
        return t("broker_warning")
    return text if get_lang() == LANG_EN else t("broker_warning")


def render_language_sidebar() -> None:
    import streamlit as st

    labels = {LANG_ZH: t("traditional_chinese"), LANG_EN: t("english")}
    current = get_lang()
    choice = st.sidebar.radio(
        t("language"),
        options=[LANG_ZH, LANG_EN],
        format_func=lambda value: labels[value],
        index=[LANG_ZH, LANG_EN].index(current),
    )
    set_lang(choice)


def render_refresh_button() -> None:
    import streamlit as st

    if st.sidebar.button(t("refresh_data"), use_container_width=True):
        st.cache_data.clear()
        st.rerun()
