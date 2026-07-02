# Data Integrity Current Outputs

Generated: 2026-07-02T13:52:42.626287+00:00

## Home / Market Regime
- Market Score: 65
- Market Regime: Risk-On
- Today Action: Gradual Buy Zone
- Data Confidence: 92
- components: {'US Market': 80, 'US Tech': 58, 'Taiwan': 86, 'Crypto': 26, 'Gold': 52, 'Macro': 54, 'Volatility': 82, 'Liquidity': 64, 'Sentiment': 88, 'Breadth': 78, 'Defensive': 40}
- warnings: ['yfinance data may be delayed or best-effort.', 'FRED macro data may be daily or lagged.', 'Verify broker quote before actual trading.', 'Taiwan stock data is reference-only. Do not use for execution.']

## Score Diagnostics
- US Market: score=80 provider=yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=75 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=SPY: price=751, ma60=730.3, r20=-0.43 | QQQ: price=729.5, ma60=696.1, r20=-1.98
- US Tech: score=58 provider=yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=75 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=NVDA: price=198.4, ma60=207.2, r20=-7.61 | TSM: price=456, ma60=411.5, r20=4.41 | PLTR: price=131.1, ma60=135.4, r20=-7.82 | GEV: price=1130, ma60=1032, r20=17.78 | MRVL: price=273.8, ma60=209.1, r20=-9.23
- Taiwan: score=86 provider=Yahoo Finance / yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=60 fallback=False formula=market_regime_v2 warning=Taiwan stock data is reference-only. Do not use for execution. raw=0050.TW: price=108.8, ma60=97.14, r20=1.12 | 2330.TW: price=2465, ma60=2256, r20=1.65 | 2454.TW: price=4345, ma60=3461, r20=-4.40 | 2327.TW: price=1055, ma60=618.2, r20=28.66
- Crypto: score=26 provider=Binance, Binance read-only timestamp=2026-07-02T13:52:26.859501+00:00 confidence=88 fallback=False formula=market_regime_v2 warning=Read-only crypto reference data. raw=BTC-USD: price=6.191e+04, ma60=6.99e+04, r20=-2.68 | BTCUSDT: price=61905.32, connected=True | ETHUSDT: price=1712.49, connected=True
- Gold: score=52 provider=yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=75 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=GC=F: price=4141, ma60=4489, r20=-6.66 | SPY: price=751, ma60=730.3, r20=-0.43 | QQQ: price=729.5, ma60=696.1, r20=-1.98
- Macro: score=54 provider=FRED, yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=76 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=DGS10: value=4.44, date=2026-06-30 | DGS2: value=4.14, date=2026-06-30 | FEDFUNDS: value=3.63, date=2026-06-01 | CPIAUCSL: value=333.979, date=2026-05-01 | M2SL: value=23052.3, date=2026-05-01 | DX-Y.NYB: price=100.8, ma60=99.28, r20=1.24
- Volatility: score=82 provider=yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=75 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=^VIX: price=15.97, ma60=17.81, r20=-0.56
- Liquidity: score=64 provider=FRED, yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=76 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=DX-Y.NYB: price=100.8, ma60=99.28, r20=1.24 | ^VIX: price=15.97, ma60=17.81, r20=-0.56 | DGS10: value=4.44, date=2026-06-30
- Sentiment: score=88 provider=yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=75 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=SPY: price=751, ma60=730.3, r20=-0.43 | QQQ: price=729.5, ma60=696.1, r20=-1.98 | ^VIX: price=15.97, ma60=17.81, r20=-0.56
- Breadth: score=78 provider=Yahoo Finance / yfinance, yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=71 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort.; Taiwan stock data is reference-only. Do not use for execution. raw=SPY: price=751, ma60=730.3, r20=-0.43 | QQQ: price=729.5, ma60=696.1, r20=-1.98 | 0050.TW: price=108.8, ma60=97.14, r20=1.12 | VWRA.L: price=189.5, ma60=184.8, r20=-0.48
- Defensive: score=40 provider=yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=75 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=GC=F: price=4141, ma60=4489, r20=-6.66 | SGLD.L: price=397.7, ma60=431.7, r20=-7.58 | ^VIX: price=15.97, ma60=17.81, r20=-0.56 | SPY: price=751, ma60=730.3, r20=-0.43

## Identical Scores
- none

## Portfolio
{'score': 66, 'summary': 'Average drift 12.2%', 'warnings': ['Portfolio drift is elevated.']}

## Failures
- none
