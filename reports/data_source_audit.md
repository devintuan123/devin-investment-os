# Data Source Audit

Generated: 2026-07-02T14:29:06.468937+00:00

Status: PASS

## yfinance
- SPY: price=748.2150268554688 rows=125 source=yfinance confidence=75 warning=yfinance data may be delayed or best-effort.
- QQQ: price=722.4199829101562 rows=125 source=yfinance confidence=75 warning=yfinance data may be delayed or best-effort.
- NVDA: price=197.74989318847656 rows=125 source=yfinance confidence=75 warning=yfinance data may be delayed or best-effort.
- TSM: price=450.6600036621094 rows=125 source=yfinance confidence=75 warning=yfinance data may be delayed or best-effort.
- 0050.TW: price=108.80000305175781 rows=118 source=yfinance confidence=60 warning=Taiwan stock data is reference-only. Do not use for execution.
- 2330.TW: price=2465.0 rows=118 source=yfinance confidence=60 warning=Taiwan stock data is reference-only. Do not use for execution.
- GC=F: price=4143.39990234375 rows=125 source=yfinance confidence=75 warning=yfinance data may be delayed or best-effort.
- ^VIX: price=15.8100004196167 rows=126 source=yfinance confidence=75 warning=yfinance data may be delayed or best-effort.
- BTC-USD: price=61691.45 rows=182 source=binance confidence=90 warning=Read-only crypto reference data.

## Binance
- BTCUSDT: connected=True price=61691.45 confidence=85 warning=Read-only public endpoint.
- ETHUSDT: connected=True price=1702.44 confidence=85 warning=Read-only public endpoint.

## FRED
- DGS10: connected=True date=2026-06-30 value=4.44 previous=4.38 confidence=78 warning=daily/lagged macro data
- DGS2: connected=True date=2026-06-30 value=4.14 previous=4.1 confidence=78 warning=daily/lagged macro data
- FEDFUNDS: connected=True date=2026-06-01 value=3.63 previous=3.63 confidence=78 warning=daily/lagged macro data
- CPIAUCSL: connected=True date=2026-05-01 value=333.979 previous=332.407 confidence=78 warning=daily/lagged macro data
- M2SL: connected=True date=2026-05-01 value=23052.3 previous=22804.5 confidence=78 warning=daily/lagged macro data

## Local Files
- data/portfolio.csv: exists=True rows=13 missing=[] duplicates=0 warnings=[]
- data/watchlist.csv: exists=True rows=10 missing=[] duplicates=0 warnings=[]
- data/theme_universe.csv: exists=True rows=70 missing=[] duplicates=0 warnings=[]
- data/strategy_rules.yaml: exists=True rows=n/a missing=[] duplicates=n/a warnings=[]
- data/alert_rules.yaml: exists=True rows=n/a missing=[] duplicates=n/a warnings=[]

## Snapshots
- exists=True count=1 latest=2026-07-02.json

## Failures
- none
