import pandas as pd
import plotly.express as px
import streamlit as st

from utils.i18n import t
from utils.interactive_table import render_interactive_table
from utils.snapshot_store import load_snapshot_history, summarize_snapshot_trend
from utils.ui import get_current_lang, render_refresh_button, render_sidebar_language_switch, render_sidebar_provider_status


def render(lang: str) -> None:
    st.title(t("history"))
    st.caption(t("history_caption"))

    snapshots = load_snapshot_history()
    if not snapshots:
        st.info(t("no_snapshots"))
    else:
        rows = [{"timestamp": item.get("timestamp"), "market_score": item.get("market_score"), "market_regime": item.get("market_regime"), "cash_deployment_mode": item.get("cash_deployment_mode"), "alerts": len(item.get("top_risk_warnings", []))} for item in snapshots]
        df = pd.DataFrame(rows)
        st.subheader(t("snapshot_trend"))
        render_interactive_table(pd.DataFrame([summarize_snapshot_trend()]), table_key="history_snapshot_trend", lang=lang)
        st.plotly_chart(px.line(df, x="timestamp", y="market_score", title=t("market_score")), use_container_width=True)
        render_interactive_table(df, table_key="history_snapshots", lang=lang)
        if "market_regime" in df:
            st.plotly_chart(px.scatter(df, x="timestamp", y="market_regime", title=t("regime_history")), use_container_width=True)
        drift_rows = []
        sector_rows = []
        for snapshot in snapshots:
            drift_rows.append({"timestamp": snapshot.get("timestamp"), "average_abs_drift": snapshot.get("portfolio_drift_summary", {}).get("average_abs_drift", 0)})
            for row in snapshot.get("top_hot_themes", [])[:5]:
                sector_rows.append({"timestamp": snapshot.get("timestamp"), "theme": row.get("theme"), "heat_score": row.get("heat_score")})
        st.subheader(t("portfolio_drift_trend"))
        render_interactive_table(pd.DataFrame(drift_rows), table_key="history_drift_trend", lang=lang)
        st.subheader(t("sector_heat_trend"))
        render_interactive_table(pd.DataFrame(sector_rows), table_key="history_sector_heat_trend", lang=lang)
        st.subheader(t("latest_alerts"))
        for alert in snapshots[-1].get("top_risk_warnings", []):
            st.write(f"- {alert.get('ticker')}: {alert.get('strategy_action')}")
