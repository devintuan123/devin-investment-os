# Data Integrity Current Outputs

Generated: 2026-07-02T14:29:39.721945+00:00

## Home / Market Regime
- Market Score: 65
- Market Regime: Risk-On
- Today Action: Gradual Buy Zone
- Data Confidence: 92
- components: {'US Market': 80, 'US Tech': 56, 'Taiwan': 86, 'Crypto': 26, 'Gold': 52, 'Macro': 54, 'Volatility': 82, 'Liquidity': 64, 'Sentiment': 88, 'Breadth': 78, 'Defensive': 40}
- warnings: ['yfinance data may be delayed or best-effort.', 'FRED macro data may be daily or lagged.', 'Verify broker quote before actual trading.', 'Taiwan stock data is reference-only. Do not use for execution.']

## Score Diagnostics
- US Market: score=80 provider=yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=75 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=SPY: price=747.8, ma60=730.2, r20=-0.86 | QQQ: price=721.7, ma60=696, r20=-3.02
- US Tech: score=56 provider=yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=75 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=NVDA: price=197.7, ma60=207.2, r20=-7.94 | TSM: price=450.1, ma60=411.4, r20=3.07 | PLTR: price=129.7, ma60=135.3, r20=-8.77 | GEV: price=1126, ma60=1032, r20=17.42 | MRVL: price=260.3, ma60=208.9, r20=-13.71
- Taiwan: score=86 provider=Yahoo Finance / yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=60 fallback=False formula=market_regime_v2 warning=Taiwan stock data is reference-only. Do not use for execution. raw=0050.TW: price=108.8, ma60=97.14, r20=1.12 | 2330.TW: price=2465, ma60=2256, r20=1.65 | 2454.TW: price=4345, ma60=3461, r20=-4.40 | 2327.TW: price=1055, ma60=618.2, r20=28.66
- Crypto: score=26 provider=Binance, Binance read-only timestamp=2026-07-02T14:29:20.700385+00:00 confidence=88 fallback=False formula=market_regime_v2 warning=Read-only crypto reference data. raw=BTC-USD: price=6.168e+04, ma60=6.989e+04, r20=-3.05 | BTCUSDT: price=61680.79, connected=True | ETHUSDT: price=1703.0, connected=True
- Gold: score=52 provider=yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=75 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=GC=F: price=4140, ma60=4489, r20=-6.67 | SPY: price=747.8, ma60=730.2, r20=-0.86 | QQQ: price=721.7, ma60=696, r20=-3.02
- Macro: score=54 provider=FRED, yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=76 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=DGS10: value=4.44, date=2026-06-30 | DGS2: value=4.14, date=2026-06-30 | FEDFUNDS: value=3.63, date=2026-06-01 | CPIAUCSL: value=333.979, date=2026-05-01 | M2SL: value=23052.3, date=2026-05-01 | DX-Y.NYB: price=100.7, ma60=99.28, r20=1.15
- Volatility: score=82 provider=yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=75 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=^VIX: price=15.82, ma60=17.8, r20=-1.49
- Liquidity: score=64 provider=FRED, yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=76 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=DX-Y.NYB: price=100.7, ma60=99.28, r20=1.15 | ^VIX: price=15.82, ma60=17.8, r20=-1.49 | DGS10: value=4.44, date=2026-06-30
- Sentiment: score=88 provider=yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=75 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=SPY: price=747.8, ma60=730.2, r20=-0.86 | QQQ: price=721.7, ma60=696, r20=-3.02 | ^VIX: price=15.82, ma60=17.8, r20=-1.49
- Breadth: score=78 provider=Yahoo Finance / yfinance, yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=71 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort.; Taiwan stock data is reference-only. Do not use for execution. raw=SPY: price=747.8, ma60=730.2, r20=-0.86 | QQQ: price=721.7, ma60=696, r20=-3.02 | 0050.TW: price=108.8, ma60=97.14, r20=1.12 | VWRA.L: price=190.1, ma60=184.8, r20=-0.18
- Defensive: score=40 provider=yfinance timestamp=2026-07-02T00:00:00+00:00 confidence=75 fallback=False formula=market_regime_v2 warning=yfinance data may be delayed or best-effort. raw=GC=F: price=4140, ma60=4489, r20=-6.67 | SGLD.L: price=397.1, ma60=431.7, r20=-7.71 | ^VIX: price=15.82, ma60=17.8, r20=-1.49 | SPY: price=747.8, ma60=730.2, r20=-0.86

## Identical Scores
- none

## Portfolio
{'score': 65, 'summary': 'Average drift 12.3%', 'warnings': ['Portfolio drift is elevated.']}

## Failures
- none
