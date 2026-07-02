# Devin Investment OS Performance Audit

Generated UTC: 2026-07-02T10:12:43+00:00

| Function / Module | Duration (s) | Tickers | Cache | Bottleneck | Recommendation |
|---|---:|---:|---|---|---|
| Market regime calculation | 12.981 |  | not measurable in CLI audit | high | Cache regime and batch core market tickers |
| Watchlist scoring | 2.756 | 15 | not measurable in CLI audit | low | Acceptable |
| Portfolio valuation | 1.927 | 13 | not measurable in CLI audit | low | Acceptable |
| Buy zone scoring | 15.495 | 13 | not measurable in CLI audit | high | Batch yfinance calls and reuse cached history |
| Sector heat calculation | 9.8 | 70 | not measurable in CLI audit | high | Use quick scan, batch yfinance history, and cache results |
| Daily Playbook generation | 88.57 |  | not measurable in CLI audit | critical | Cache expensive market data and avoid recomputation on Home |
| Snapshot creation | 46.637 |  | not measurable in CLI audit | critical | Cache expensive market data and avoid recomputation on Home |
| Alert evaluation | 43.337 |  | not measurable in CLI audit | critical | Cache expensive market data and avoid recomputation on Home |
| yfinance batch fetch | 0.772 | 8 | not measurable in CLI audit | low | Acceptable |
| yfinance history fetch | 0.122 | 5 | not measurable in CLI audit | low | Acceptable |
| Binance fetch | 0.489 | 1 | not measurable in CLI audit | low | Acceptable |
| FRED fetch | 0.81 | 1 | not measurable in CLI audit | low | Acceptable |
