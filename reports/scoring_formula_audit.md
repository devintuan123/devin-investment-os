# Scoring Formula Audit

Generated: 2026-07-02T13:52:42.626339+00:00

Status: PASS

## calculate_market_regime/_trend_score
- purpose: Calculate US Market contribution to market regime.
- raw_inputs: SPY: price=751, ma60=730.3, r20=-0.43 | QQQ: price=729.5, ma60=696.1, r20=-1.98
- transformed_inputs: average trend score using price vs MA20/MA60, 20D return, 52W drawdown
- score_range: 0-100
- clamp_behavior: bounded with _bound or equivalent min/max clamp
- missing_data_behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- weights: 1.0
- output_labels: component score, confidence, warning, fallback_used
- assumptions: read-only decision support; delayed/best-effort market data
- data_confidence_adjustment: 75
- fallback_default_values: False
- formula_version: market_regime_v2

## calculate_market_regime/_trend_score
- purpose: Calculate US Tech contribution to market regime.
- raw_inputs: NVDA: price=198.4, ma60=207.2, r20=-7.61 | TSM: price=456, ma60=411.5, r20=4.41 | PLTR: price=131.1, ma60=135.4, r20=-7.82 | GEV: price=1130, ma60=1032, r20=17.78 | MRVL: price=273.8, ma60=209.1, r20=-9.23
- transformed_inputs: average trend score across AI/tech proxies
- score_range: 0-100
- clamp_behavior: bounded with _bound or equivalent min/max clamp
- missing_data_behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- weights: 1.0
- output_labels: component score, confidence, warning, fallback_used
- assumptions: read-only decision support; delayed/best-effort market data
- data_confidence_adjustment: 75
- fallback_default_values: False
- formula_version: market_regime_v2

## calculate_market_regime/_trend_score
- purpose: Calculate Taiwan contribution to market regime.
- raw_inputs: 0050.TW: price=108.8, ma60=97.14, r20=1.12 | 2330.TW: price=2465, ma60=2256, r20=1.65 | 2454.TW: price=4345, ma60=3461, r20=-4.40 | 2327.TW: price=1055, ma60=618.2, r20=28.66
- transformed_inputs: average trend score across Taiwan proxies
- score_range: 0-100
- clamp_behavior: bounded with _bound or equivalent min/max clamp
- missing_data_behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- weights: 1.0
- output_labels: component score, confidence, warning, fallback_used
- assumptions: read-only decision support; delayed/best-effort market data
- data_confidence_adjustment: 60
- fallback_default_values: False
- formula_version: market_regime_v2

## _crypto_score
- purpose: Calculate Crypto contribution to market regime.
- raw_inputs: BTC-USD: price=6.191e+04, ma60=6.99e+04, r20=-2.68 | BTCUSDT: price=61905.32, connected=True | ETHUSDT: price=1712.49, connected=True
- transformed_inputs: BTC trend score plus Binance read-only availability adjustment
- score_range: 0-100
- clamp_behavior: bounded with _bound or equivalent min/max clamp
- missing_data_behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- weights: 1.0
- output_labels: component score, confidence, warning, fallback_used
- assumptions: read-only decision support; delayed/best-effort market data
- data_confidence_adjustment: 88
- fallback_default_values: False
- formula_version: market_regime_v2

## _gold_score
- purpose: Calculate Gold contribution to market regime.
- raw_inputs: GC=F: price=4141, ma60=4489, r20=-6.66 | SPY: price=751, ma60=730.3, r20=-0.43 | QQQ: price=729.5, ma60=696.1, r20=-1.98
- transformed_inputs: gold trend adjusted against equity trend
- score_range: 0-100
- clamp_behavior: bounded with _bound or equivalent min/max clamp
- missing_data_behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- weights: 0.8
- output_labels: component score, confidence, warning, fallback_used
- assumptions: read-only decision support; delayed/best-effort market data
- data_confidence_adjustment: 75
- fallback_default_values: False
- formula_version: market_regime_v2

## _macro_score
- purpose: Calculate Macro contribution to market regime.
- raw_inputs: DGS10: value=4.44, date=2026-06-30 | DGS2: value=4.14, date=2026-06-30 | FEDFUNDS: value=3.63, date=2026-06-01 | CPIAUCSL: value=333.979, date=2026-05-01 | M2SL: value=23052.3, date=2026-05-01 | DX-Y.NYB: price=100.8, ma60=99.28, r20=1.24
- transformed_inputs: base macro score adjusted for yield pressure, inversion, DXY trend, FRED availability
- score_range: 0-100
- clamp_behavior: bounded with _bound or equivalent min/max clamp
- missing_data_behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- weights: 1.2
- output_labels: component score, confidence, warning, fallback_used
- assumptions: read-only decision support; delayed/best-effort market data
- data_confidence_adjustment: 76
- fallback_default_values: False
- formula_version: market_regime_v2

## _volatility_score
- purpose: Calculate Volatility contribution to market regime.
- raw_inputs: ^VIX: price=15.97, ma60=17.81, r20=-0.56
- transformed_inputs: discrete VIX risk appetite thresholds
- score_range: 0-100
- clamp_behavior: bounded with _bound or equivalent min/max clamp
- missing_data_behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- weights: 1.0
- output_labels: component score, confidence, warning, fallback_used
- assumptions: read-only decision support; delayed/best-effort market data
- data_confidence_adjustment: 75
- fallback_default_values: False
- formula_version: market_regime_v2

## _liquidity_score
- purpose: Calculate Liquidity contribution to market regime.
- raw_inputs: DX-Y.NYB: price=100.8, ma60=99.28, r20=1.24 | ^VIX: price=15.97, ma60=17.81, r20=-0.56 | DGS10: value=4.44, date=2026-06-30
- transformed_inputs: DXY, VIX, and 10Y yield-change pressure
- score_range: 0-100
- clamp_behavior: bounded with _bound or equivalent min/max clamp
- missing_data_behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- weights: 1.0
- output_labels: component score, confidence, warning, fallback_used
- assumptions: read-only decision support; delayed/best-effort market data
- data_confidence_adjustment: 76
- fallback_default_values: False
- formula_version: market_regime_v2

## _sentiment_score
- purpose: Calculate Sentiment contribution to market regime.
- raw_inputs: SPY: price=751, ma60=730.3, r20=-0.43 | QQQ: price=729.5, ma60=696.1, r20=-1.98 | ^VIX: price=15.97, ma60=17.81, r20=-0.56
- transformed_inputs: SPY/QQQ trend adjusted by VIX
- score_range: 0-100
- clamp_behavior: bounded with _bound or equivalent min/max clamp
- missing_data_behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- weights: 1.0
- output_labels: component score, confidence, warning, fallback_used
- assumptions: read-only decision support; delayed/best-effort market data
- data_confidence_adjustment: 75
- fallback_default_values: False
- formula_version: market_regime_v2

## _breadth_score
- purpose: Calculate Breadth contribution to market regime.
- raw_inputs: SPY: price=751, ma60=730.3, r20=-0.43 | QQQ: price=729.5, ma60=696.1, r20=-1.98 | 0050.TW: price=108.8, ma60=97.14, r20=1.12 | VWRA.L: price=189.5, ma60=184.8, r20=-0.48
- transformed_inputs: share above MA60 and positive 20D momentum
- score_range: 0-100
- clamp_behavior: bounded with _bound or equivalent min/max clamp
- missing_data_behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- weights: 1.0
- output_labels: component score, confidence, warning, fallback_used
- assumptions: read-only decision support; delayed/best-effort market data
- data_confidence_adjustment: 71
- fallback_default_values: False
- formula_version: market_regime_v2

## _defensive_score
- purpose: Calculate Defensive contribution to market regime.
- raw_inputs: GC=F: price=4141, ma60=4489, r20=-6.66 | SGLD.L: price=397.7, ma60=431.7, r20=-7.58 | ^VIX: price=15.97, ma60=17.81, r20=-0.56 | SPY: price=751, ma60=730.3, r20=-0.43
- transformed_inputs: gold hedge strength and VIX stress versus equity weakness
- score_range: 0-100
- clamp_behavior: bounded with _bound or equivalent min/max clamp
- missing_data_behavior: fallback lowers confidence and shows warning; unavailable providers stay low confidence
- weights: 0.8
- output_labels: component score, confidence, warning, fallback_used
- assumptions: read-only decision support; delayed/best-effort market data
- data_confidence_adjustment: 75
- fallback_default_values: False
- formula_version: market_regime_v2

## score_watchlist/score_ticker
- purpose: Watchlist trend/pullback/action/risk labels
- raw_inputs: price, MA20, MA60, MA120, 52W drawdown
- score_range: 0-100
- clamp_behavior: min/max clamp
- missing_data_behavior: fallback quote/history warning carried to row
- weights: rule-based
- output_labels: trend_score, pullback_score, action_label, risk_label
- assumptions: broker quote must be verified
- formula_version: watchlist_v1

## score_buy_zones/score_buy_zone
- purpose: Buy-zone reference bands
- raw_inputs: price, MA20, MA60, MA120, 52W high, drawdown, volatility
- score_range: labels not total score
- clamp_behavior: zone thresholds
- missing_data_behavior: fallback warning carried to row
- weights: rule-based
- output_labels: current_zone_status, action_label, strategy_action
- assumptions: no Buy Now; gradual/reference only
- formula_version: buy_zone_v1

## portfolio_health_score
- purpose: Portfolio drift health
- raw_inputs: manual holdings, latest prices, target weights
- score_range: 0-100
- clamp_behavior: 90 - drift penalty - missing penalty bounded
- missing_data_behavior: missing price reduces score and warning
- weights: drift and missing-data penalties
- output_labels: score, summary, warnings
- assumptions: manual portfolio may differ from broker
- formula_version: portfolio_v1

## calculate_theme_heat_score
- purpose: Sector/theme heat proxy
- raw_inputs: theme universe, 5D/20D returns, MA distance, breadth
- score_range: 0-100
- clamp_behavior: bounded heat and rotation scores
- missing_data_behavior: proxy warning and fallback history warning
- weights: 50 + return_5d*4 + return_20d*1.5 + MA strength + breadth adjustment
- output_labels: heat_score, rotation_score, heat_label
- assumptions: proxy heat only, not exact fund flows
- formula_version: sector_heat_v1

## evaluate_alerts
- purpose: Read-only alert trigger logic
- raw_inputs: market regime, prices, portfolio drift, sector heat, strategy rules
- score_range: rule triggers
- clamp_behavior: n/a
- missing_data_behavior: missing providers create warnings rather than execution
- weights: rule thresholds
- output_labels: severity, title, value, warning
- assumptions: no trades executed
- formula_version: alerts_v1

## Failures
- none
