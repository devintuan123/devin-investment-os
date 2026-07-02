# Scoring Formulas

Read-only scoring documentation. Scores are decision-support references only and must not be treated as broker quotes or execution instructions.

## calculate_market_regime/_trend_score
- Purpose: Calculate US Market contribution to market regime.
- Raw Inputs: SPY: price=747.8, ma60=730.2, r20=-0.86 | QQQ: price=721.7, ma60=696, r20=-3.02
- Transformed Inputs: average trend score using price vs MA20/MA60, 20D return, 52W drawdown
- Score Range: 0-100
- Clamp Behavior: bounded with _bound or equivalent min/max clamp
- Missing Data Behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- Weights: 1.0
- Output Labels: component score, confidence, warning, fallback_used
- Assumptions: read-only decision support; delayed/best-effort market data
- Data Confidence Adjustment: 75
- Fallback Default Values: False
- Formula Version: market_regime_v2

## calculate_market_regime/_trend_score
- Purpose: Calculate US Tech contribution to market regime.
- Raw Inputs: NVDA: price=197.7, ma60=207.2, r20=-7.94 | TSM: price=450.1, ma60=411.4, r20=3.07 | PLTR: price=129.7, ma60=135.3, r20=-8.77 | GEV: price=1126, ma60=1032, r20=17.42 | MRVL: price=260.3, ma60=208.9, r20=-13.71
- Transformed Inputs: average trend score across AI/tech proxies
- Score Range: 0-100
- Clamp Behavior: bounded with _bound or equivalent min/max clamp
- Missing Data Behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- Weights: 1.0
- Output Labels: component score, confidence, warning, fallback_used
- Assumptions: read-only decision support; delayed/best-effort market data
- Data Confidence Adjustment: 75
- Fallback Default Values: False
- Formula Version: market_regime_v2

## calculate_market_regime/_trend_score
- Purpose: Calculate Taiwan contribution to market regime.
- Raw Inputs: 0050.TW: price=108.8, ma60=97.14, r20=1.12 | 2330.TW: price=2465, ma60=2256, r20=1.65 | 2454.TW: price=4345, ma60=3461, r20=-4.40 | 2327.TW: price=1055, ma60=618.2, r20=28.66
- Transformed Inputs: average trend score across Taiwan proxies
- Score Range: 0-100
- Clamp Behavior: bounded with _bound or equivalent min/max clamp
- Missing Data Behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- Weights: 1.0
- Output Labels: component score, confidence, warning, fallback_used
- Assumptions: read-only decision support; delayed/best-effort market data
- Data Confidence Adjustment: 60
- Fallback Default Values: False
- Formula Version: market_regime_v2

## _crypto_score
- Purpose: Calculate Crypto contribution to market regime.
- Raw Inputs: BTC-USD: price=6.168e+04, ma60=6.989e+04, r20=-3.05 | BTCUSDT: price=61680.79, connected=True | ETHUSDT: price=1703.0, connected=True
- Transformed Inputs: BTC trend score plus Binance read-only availability adjustment
- Score Range: 0-100
- Clamp Behavior: bounded with _bound or equivalent min/max clamp
- Missing Data Behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- Weights: 1.0
- Output Labels: component score, confidence, warning, fallback_used
- Assumptions: read-only decision support; delayed/best-effort market data
- Data Confidence Adjustment: 88
- Fallback Default Values: False
- Formula Version: market_regime_v2

## _gold_score
- Purpose: Calculate Gold contribution to market regime.
- Raw Inputs: GC=F: price=4140, ma60=4489, r20=-6.67 | SPY: price=747.8, ma60=730.2, r20=-0.86 | QQQ: price=721.7, ma60=696, r20=-3.02
- Transformed Inputs: gold trend adjusted against equity trend
- Score Range: 0-100
- Clamp Behavior: bounded with _bound or equivalent min/max clamp
- Missing Data Behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- Weights: 0.8
- Output Labels: component score, confidence, warning, fallback_used
- Assumptions: read-only decision support; delayed/best-effort market data
- Data Confidence Adjustment: 75
- Fallback Default Values: False
- Formula Version: market_regime_v2

## _macro_score
- Purpose: Calculate Macro contribution to market regime.
- Raw Inputs: DGS10: value=4.44, date=2026-06-30 | DGS2: value=4.14, date=2026-06-30 | FEDFUNDS: value=3.63, date=2026-06-01 | CPIAUCSL: value=333.979, date=2026-05-01 | M2SL: value=23052.3, date=2026-05-01 | DX-Y.NYB: price=100.7, ma60=99.28, r20=1.15
- Transformed Inputs: base macro score adjusted for yield pressure, inversion, DXY trend, FRED availability
- Score Range: 0-100
- Clamp Behavior: bounded with _bound or equivalent min/max clamp
- Missing Data Behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- Weights: 1.2
- Output Labels: component score, confidence, warning, fallback_used
- Assumptions: read-only decision support; delayed/best-effort market data
- Data Confidence Adjustment: 76
- Fallback Default Values: False
- Formula Version: market_regime_v2

## _volatility_score
- Purpose: Calculate Volatility contribution to market regime.
- Raw Inputs: ^VIX: price=15.82, ma60=17.8, r20=-1.49
- Transformed Inputs: discrete VIX risk appetite thresholds
- Score Range: 0-100
- Clamp Behavior: bounded with _bound or equivalent min/max clamp
- Missing Data Behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- Weights: 1.0
- Output Labels: component score, confidence, warning, fallback_used
- Assumptions: read-only decision support; delayed/best-effort market data
- Data Confidence Adjustment: 75
- Fallback Default Values: False
- Formula Version: market_regime_v2

## _liquidity_score
- Purpose: Calculate Liquidity contribution to market regime.
- Raw Inputs: DX-Y.NYB: price=100.7, ma60=99.28, r20=1.15 | ^VIX: price=15.82, ma60=17.8, r20=-1.49 | DGS10: value=4.44, date=2026-06-30
- Transformed Inputs: DXY, VIX, and 10Y yield-change pressure
- Score Range: 0-100
- Clamp Behavior: bounded with _bound or equivalent min/max clamp
- Missing Data Behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- Weights: 1.0
- Output Labels: component score, confidence, warning, fallback_used
- Assumptions: read-only decision support; delayed/best-effort market data
- Data Confidence Adjustment: 76
- Fallback Default Values: False
- Formula Version: market_regime_v2

## _sentiment_score
- Purpose: Calculate Sentiment contribution to market regime.
- Raw Inputs: SPY: price=747.8, ma60=730.2, r20=-0.86 | QQQ: price=721.7, ma60=696, r20=-3.02 | ^VIX: price=15.82, ma60=17.8, r20=-1.49
- Transformed Inputs: SPY/QQQ trend adjusted by VIX
- Score Range: 0-100
- Clamp Behavior: bounded with _bound or equivalent min/max clamp
- Missing Data Behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- Weights: 1.0
- Output Labels: component score, confidence, warning, fallback_used
- Assumptions: read-only decision support; delayed/best-effort market data
- Data Confidence Adjustment: 75
- Fallback Default Values: False
- Formula Version: market_regime_v2

## _breadth_score
- Purpose: Calculate Breadth contribution to market regime.
- Raw Inputs: SPY: price=747.8, ma60=730.2, r20=-0.86 | QQQ: price=721.7, ma60=696, r20=-3.02 | 0050.TW: price=108.8, ma60=97.14, r20=1.12 | VWRA.L: price=190.1, ma60=184.8, r20=-0.18
- Transformed Inputs: share above MA60 and positive 20D momentum
- Score Range: 0-100
- Clamp Behavior: bounded with _bound or equivalent min/max clamp
- Missing Data Behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- Weights: 1.0
- Output Labels: component score, confidence, warning, fallback_used
- Assumptions: read-only decision support; delayed/best-effort market data
- Data Confidence Adjustment: 71
- Fallback Default Values: False
- Formula Version: market_regime_v2

## _defensive_score
- Purpose: Calculate Defensive contribution to market regime.
- Raw Inputs: GC=F: price=4140, ma60=4489, r20=-6.67 | SGLD.L: price=397.1, ma60=431.7, r20=-7.71 | ^VIX: price=15.82, ma60=17.8, r20=-1.49 | SPY: price=747.8, ma60=730.2, r20=-0.86
- Transformed Inputs: gold hedge strength and VIX stress versus equity weakness
- Score Range: 0-100
- Clamp Behavior: bounded with _bound or equivalent min/max clamp
- Missing Data Behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- Weights: 0.8
- Output Labels: component score, confidence, warning, fallback_used
- Assumptions: read-only decision support; delayed/best-effort market data
- Data Confidence Adjustment: 75
- Fallback Default Values: False
- Formula Version: market_regime_v2

## score_watchlist/score_ticker
- Purpose: Watchlist trend/pullback/action/risk labels
- Raw Inputs: price, MA20, MA60, MA120, 52W drawdown
- Score Range: 0-100
- Clamp Behavior: min/max clamp
- Missing Data Behavior: fallback quote/history warning carried to row
- Weights: rule-based
- Output Labels: trend_score, pullback_score, action_label, risk_label
- Assumptions: broker quote must be verified
- Formula Version: watchlist_v1

## score_buy_zones/score_buy_zone
- Purpose: Buy-zone reference bands
- Raw Inputs: price, MA20, MA60, MA120, 52W high, drawdown, volatility
- Score Range: labels not total score
- Clamp Behavior: zone thresholds
- Missing Data Behavior: fallback warning carried to row
- Weights: rule-based
- Output Labels: current_zone_status, action_label, strategy_action
- Assumptions: no Buy Now; gradual/reference only
- Formula Version: buy_zone_v1

## portfolio_health_score
- Purpose: Portfolio drift health
- Raw Inputs: manual holdings, latest prices, target weights
- Score Range: 0-100
- Clamp Behavior: 90 - drift penalty - missing penalty bounded
- Missing Data Behavior: missing price reduces score and warning
- Weights: drift and missing-data penalties
- Output Labels: score, summary, warnings
- Assumptions: manual portfolio may differ from broker
- Formula Version: portfolio_v1

## calculate_theme_heat_score
- Purpose: Sector/theme heat proxy
- Raw Inputs: theme universe, 5D/20D returns, MA distance, breadth
- Score Range: 0-100
- Clamp Behavior: bounded heat and rotation scores
- Missing Data Behavior: proxy warning and fallback history warning
- Weights: 50 + return_5d*4 + return_20d*1.5 + MA strength + breadth adjustment
- Output Labels: heat_score, rotation_score, heat_label
- Assumptions: proxy heat only, not exact fund flows
- Formula Version: sector_heat_v1

## evaluate_alerts
- Purpose: Read-only alert trigger logic
- Raw Inputs: market regime, prices, portfolio drift, sector heat, strategy rules
- Score Range: rule triggers
- Clamp Behavior: n/a
- Missing Data Behavior: missing providers create warnings rather than execution
- Weights: rule thresholds
- Output Labels: severity, title, value, warning
- Assumptions: no trades executed
- Formula Version: alerts_v1
