import pandas as pd
import streamlit as st

from utils.market_data import safe_fetch_with_fallback
from utils.providers.tokenized_equity_provider import (
    REFERENCE_WARNING,
    discover_supported_tokenized_equities,
    get_tokenized_equity_basis,
    tokenized_equity_health_check,
)


st.set_page_config(page_title="Data Quality", page_icon="DI", layout="wide")
st.title("Data Quality")
st.caption("Provider hierarchy, freshness, reliability caps, and reference-data warnings.")

st.subheader("Source Hierarchy")
st.write("- Crypto: Binance > yfinance > fallback")
st.write("- US/ETF: IBKR future > yfinance > fallback")
st.write("- Taiwan: Yuanta future/CSV > yfinance > fallback")
st.write("- Signals: TradingView webhook > internal rules")

st.subheader("Tokenized Equity")
health = tokenized_equity_health_check()
col1, col2, col3 = st.columns(3)
col1.metric("Provider", health["provider"])
col2.metric("Available Symbols", health["available_count"])
col3.metric("Reliability Cap", f"{health['reliability_cap']}/100")
st.warning(REFERENCE_WARNING)

rows = []
for item in discover_supported_tokenized_equities():
    if item["available"]:
        basis = get_tokenized_equity_basis(item["symbol"])
        rows.append(
            {
                "Provider": "Tokenized Equity",
                "Underlying": item["underlying"],
                "Supported Symbol": item["symbol"],
                "Available": True,
                "Price": basis.get("price"),
                "Official Price": basis.get("official_price"),
                "Basis %": basis.get("basis_pct"),
                "Freshness": basis.get("freshness"),
                "Reliability Cap": basis.get("reliability_cap"),
                "Confidence": basis.get("confidence"),
                "Warning": basis.get("warning"),
            }
        )
    else:
        rows.append(
            {
                "Provider": "Tokenized Equity",
                "Underlying": item["underlying"],
                "Supported Symbol": item["symbol"],
                "Available": False,
                "Price": None,
                "Official Price": None,
                "Basis %": None,
                "Freshness": "unavailable",
                "Reliability Cap": 0,
                "Confidence": 0,
                "Warning": item["warning"],
            }
        )

st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.subheader("Sample Official Sources")
official_rows = [safe_fetch_with_fallback(ticker) for ticker in ["SPY", "QQQ", "NVDA", "TSLA", "BTC-USD"]]
official_df = pd.DataFrame(official_rows)
columns = [column for column in ["ticker", "price", "source", "warning"] if column in official_df]
st.dataframe(official_df[columns], use_container_width=True, hide_index=True)
