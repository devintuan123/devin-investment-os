# Macro Data Truth Check

Generated: 2026-07-02T14:48:55.180220+00:00

## Answers
- is_fred_data_actually_being_fetched: True
- is_yfinance_data_actually_being_fetched: False
- are_macro_dashboard_inputs_empty: False
- are_fallback_values_being_used: True
- is_ui_hiding_data_failures: True

## FRED
- DGS10 (10Y Treasury yield): connected=True latest=2026-06-30 value=4.44 rows=88 missing=False stale=False fallback=False error=
- DGS2 (2Y Treasury yield): connected=True latest=2026-06-30 value=4.14 rows=88 missing=False stale=False fallback=False error=
- FEDFUNDS (Fed funds rate): connected=True latest=2026-06-01 value=3.63 rows=90 missing=False stale=False fallback=False error=
- CPIAUCSL (CPI): connected=True latest=2026-05-01 value=333.979 rows=89 missing=False stale=False fallback=False error=
- M2SL (M2 money supply): connected=True latest=2026-05-01 value=23052.3 rows=90 missing=False stale=False fallback=False error=
- BAMLH0A0HYM2 (High yield spread): connected=True latest=2026-07-01 value=2.74 rows=90 missing=False stale=False fallback=False error=
- T10Y2Y (10Y-2Y yield spread): connected=True latest=2026-07-01 value=0.31 rows=88 missing=False stale=False fallback=False error=
- DFF (Effective federal funds rate): connected=True latest=2026-06-30 value=3.63 rows=90 missing=False stale=False fallback=False error=

## yfinance Market Proxies
- ^GSPC (US Market): latest=2026-07-02 22:48:51.899724 price=100.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for ^GSPC: No history returned
- SPY (US Market fallback): latest=2026-07-02 22:48:52.102234 price=550.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for SPY: No history returned
- QQQ (US Tech): latest=2026-07-02 22:48:52.273037 price=480.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for QQQ: No history returned
- ^VIX (Volatility): latest=2026-07-02 22:48:52.400363 price=16.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for ^VIX: No history returned
- DX-Y.NYB (US Dollar / liquidity proxy): latest=2026-07-02 22:48:52.566966 price=105.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for DX-Y.NYB: No history returned
- UUP (US Dollar fallback): latest=2026-07-02 22:48:52.888981 price=100.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for UUP: No history returned
- TLT (bonds / rates proxy): latest=2026-07-02 22:48:53.100083 price=100.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for TLT: No history returned
- IEF (bonds fallback): latest=2026-07-02 22:48:53.405537 price=100.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for IEF: No history returned
- GLD (Gold): latest=2026-07-02 22:48:53.633819 price=100.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for GLD: No history returned
- GC=F (Gold fallback): latest=2026-07-02 22:48:53.776177 price=2350.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for GC=F: No history returned
- BTC-USD (Crypto): latest=2026-07-02 22:48:53.903741 price=65000.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for BTC-USD: No history returned
- 0050.TW (Taiwan Market): latest=2026-07-02 22:48:54.155502 price=102.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for 0050.TW: No history returned
- ^TWII (Taiwan fallback): latest=2026-07-02 22:48:54.408518 price=100.0 rows=90 missing=False stale=False fallback=True error=Using fallback history for ^TWII: No history returned

## Binance
- BTCUSDT: configured=True connected=True price=61498.91 timestamp=2026-07-02T14:48:55.180145+00:00 error=
