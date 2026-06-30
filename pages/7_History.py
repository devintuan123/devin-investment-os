import pandas as pd
import plotly.express as px
import streamlit as st

from utils.snapshots import load_snapshots


st.set_page_config(page_title="History", page_icon="DI", layout="wide")
st.title("History")
st.caption("Snapshot history for market scores, regimes, and previous alerts.")

snapshots = load_snapshots()
if not snapshots:
    st.info("No snapshots yet. Run `python scripts/create_daily_snapshot.py` to create the first one.")
else:
    rows = [
        {
            "timestamp": item.get("timestamp"),
            "market_score": item.get("market_score"),
            "regime": item.get("regime"),
            "alerts": len(item.get("alerts", [])),
        }
        for item in snapshots
    ]
    df = pd.DataFrame(rows)
    st.plotly_chart(px.line(df, x="timestamp", y="market_score", title="Market Score History"), use_container_width=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.subheader("Latest Alerts")
    for alert in snapshots[-1].get("alerts", []):
        st.write(f"- {alert}")
