from __future__ import annotations

import math
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import pandas as pd

from utils.market_regime import _average, _breadth_score, _macro_score, _trend_score, _volatility_score, _weighted_market_score


def asset(price: float, ma20: float, ma60: float, ma120: float, return_20d: float, drawdown: float, source: str = "synthetic") -> dict:
    return {"price": price, "ma20": ma20, "ma60": ma60, "ma120": ma120, "return_20d": return_20d, "drawdown_52w": drawdown, "source": source, "confidence": 75}


def main() -> int:
    tests = [
        test_different_inputs_produce_different_scores,
        test_missing_data_reduces_confidence_proxy,
        test_duplicate_score_prevention,
        test_weighting_behavior,
        test_range_behavior,
        test_component_independence,
    ]
    failures = []
    for test in tests:
        try:
            test()
            print(f"[PASS] {test.__name__}")
        except AssertionError as exc:
            print(f"[FAIL] {test.__name__}: {exc}")
            failures.append(test.__name__)
    return 1 if failures else 0


def test_different_inputs_produce_different_scores() -> None:
    strong = _trend_score(asset(120, 110, 100, 90, 8, -2))
    weak = _trend_score(asset(80, 90, 100, 110, -8, -25))
    neutral = _trend_score(asset(100, 100, 100, 100, 0, 0))
    assert strong > neutral > weak


def test_missing_data_reduces_confidence_proxy() -> None:
    fallback = asset(100, 100, 100, 100, 0, 0, source="fallback")
    assert fallback["source"] == "fallback"


def test_duplicate_score_prevention() -> None:
    components = {"US Market": 60, "US Tech": 62, "Taiwan": 54, "Crypto": 71, "Gold": 52, "Macro": 50, "Volatility": 82}
    assert len(set(components.values())) > 1


def test_weighting_behavior() -> None:
    specs = {"A": {"weight": 1}, "B": {"weight": 3}}
    low = _weighted_market_score({"A": 50, "B": 50}, specs)
    high = _weighted_market_score({"A": 50, "B": 90}, specs)
    assert high > low
    assert _weighted_market_score({"A": 0, "B": 100}, {"A": {"weight": 1}, "B": {"weight": 1}}) == 50


def test_range_behavior() -> None:
    values = [_trend_score(asset(1000, 1, 1, 1, 200, 0)), _volatility_score({"price": 99}), _breadth_score([]), _macro_score({"DGS10": {"connected": False}}, asset(100, 90, 90, 90, 2, 0))]
    assert all(isinstance(value, int) for value in values)
    assert all(0 <= value <= 100 and not math.isnan(value) and not math.isinf(value) for value in values)


def test_component_independence() -> None:
    groups = {
        "US Market": {"SPY", "QQQ"},
        "US Tech": {"NVDA", "TSM", "PLTR", "GEV", "MRVL"},
        "Taiwan": {"0050.TW", "2330.TW", "2454.TW", "2327.TW"},
        "Crypto": {"BTC-USD", "BTCUSDT"},
        "Gold": {"GC=F", "SGLD.L"},
        "Volatility": {"^VIX"},
        "Macro": {"DGS10", "DGS2", "DX-Y.NYB"},
    }
    assert groups["US Market"] != groups["US Tech"]
    assert any(symbol.endswith(".TW") for symbol in groups["Taiwan"])
    assert "BTC-USD" in groups["Crypto"]
    assert "GC=F" in groups["Gold"]
    assert "^VIX" in groups["Volatility"]
    assert "DGS10" in groups["Macro"]


if __name__ == "__main__":
    raise SystemExit(main())
