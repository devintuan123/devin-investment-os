# Devin Investment OS Performance Audit

Generated UTC: 2026-07-02T10:18:45+00:00

| Function / Module | Duration (s) | Tickers | Cache | Bottleneck | Recommendation |
|---|---:|---:|---|---|---|
| Market regime calculation | 10.562 |  | not measurable in CLI audit | high | Cache regime and batch core market tickers |
| Watchlist scoring | 0.783 | 15 | not measurable in CLI audit | low | Acceptable |
| Portfolio valuation | 0.745 | 13 | not measurable in CLI audit | low | Acceptable |
| Buy zone scoring | 0.711 | 13 | not measurable in CLI audit | low | Acceptable |
| Sector heat calculation | 1.303 | 70 | not measurable in CLI audit | low | Acceptable |
| Daily Playbook generation | 2.071 |  | not measurable in CLI audit | low | Acceptable |
| Snapshot creation | 1.043 |  | not measurable in CLI audit | low | Acceptable |
| Alert evaluation | 0.772 |  | not measurable in CLI audit | low | Acceptable |
| yfinance batch fetch | 0.277 | 8 | not measurable in CLI audit | low | Acceptable |
| yfinance history fetch | 0.767 | 5 | not measurable in CLI audit | low | Acceptable |
| Binance fetch | 0.0 | 1 | not measurable in CLI audit | low | Acceptable |
| FRED fetch | 0.0 | 1 | not measurable in CLI audit | low | Acceptable |
