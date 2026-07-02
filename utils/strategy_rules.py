from __future__ import annotations

from copy import deepcopy
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
STRATEGY_RULES_PATH = ROOT_DIR / "data" / "strategy_rules.yaml"

DEFAULT_RULES = {
    "global_rules": {
        "no_chasing_extended_assets": True,
        "broker_quote_required_before_trading": True,
        "yfinance_reference_only": True,
        "taiwan_yfinance_delayed_warning": True,
        "max_single_stock_weight_default": 10,
        "max_high_vol_stock_weight_default": 5,
        "crypto_max_weight_default": 5,
        "gold_target_weight_default": 2,
        "cash_deployment_mode": ["aggressive", "gradual", "dca_only", "wait"],
    },
    "asset_categories": {
        "Core ETF": {
            "examples": ["VWRA.L", "0050.TW", "CNX1.L"],
            "style": "long-term DCA",
            "risk_level": "medium",
            "buy_rule": "allow gradual buy on pullback",
        },
        "Satellite Stock": {
            "examples": ["PLTR", "GEV", "MRVL", "NVDA"],
            "style": "high volatility satellite",
            "risk_level": "high",
            "buy_rule": "only in buy zone, do not chase",
        },
        "Crypto": {
            "examples": ["BTC-USD", "BTCUSDT"],
            "style": "risk appetite asset",
            "risk_level": "high",
            "buy_rule": "only gradual buy when market regime supports",
        },
        "Gold": {
            "examples": ["SGLD.L", "GC=F"],
            "style": "defensive hedge",
            "risk_level": "medium",
            "buy_rule": "do not chase, use as hedge",
        },
        "Taiwan Stock": {
            "examples": ["2330.TW", "2454.TW", "2327.TW"],
            "style": "Taiwan equity",
            "risk_level": "medium_high",
            "buy_rule": "reference-only yfinance, verify broker quote",
        },
    },
    "default_target_allocation": {
        "VWRA.L": 40,
        "0050.TW": 20,
        "CNX1.L": 15,
        "PLTR": 10,
        "BTC-USD": 5,
        "SGLD.L": 2,
        "IEMA.L": "optional satellite",
        "WHEA.L": "optional satellite",
        "GEV": "optional satellite",
        "MRVL": "optional satellite",
        "2330.TW": "optional Taiwan stock",
        "2454.TW": "optional Taiwan stock",
        "2327.TW": "optional Taiwan stock",
    },
    "action_language_rules": {
        "forbidden": ["Buy Now", "Must Buy", "Immediate Buy", "Guaranteed"],
        "allowed": [
            "Potential buy zone",
            "Consider gradual allocation",
            "Watch",
            "Verify broker quote",
            "DCA only",
            "Hold",
            "Reduce risk",
            "Avoid chasing",
        ],
    },
}


def load_strategy_rules() -> dict:
    rules = deepcopy(DEFAULT_RULES)
    if not STRATEGY_RULES_PATH.exists():
        return rules
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(STRATEGY_RULES_PATH.read_text(encoding="utf-8")) or {}
        if isinstance(loaded, dict):
            rules.update(loaded)
    except Exception:
        pass
    return rules


def get_asset_category(symbol: str) -> str:
    symbol = _normalize_symbol(symbol)
    rules = load_strategy_rules()
    for category, config in rules.get("asset_categories", {}).items():
        examples = {_normalize_symbol(item) for item in config.get("examples", [])}
        if symbol in examples:
            return category
    if symbol.endswith(".TW"):
        return "Taiwan Stock"
    if symbol.endswith("-USD") or symbol.endswith("USDT"):
        return "Crypto"
    if symbol in {"SGLD.L", "GC=F"}:
        return "Gold"
    if symbol.endswith(".L") or symbol in {"0050.TW", "00878.TW"}:
        return "Core ETF"
    return "Satellite Stock"


def get_target_weight(symbol: str) -> float | None:
    raw = load_strategy_rules().get("default_target_allocation", {}).get(_normalize_symbol(symbol))
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def get_asset_risk_policy(symbol: str) -> dict:
    category = get_asset_category(symbol)
    rules = load_strategy_rules()
    config = rules.get("asset_categories", {}).get(category, {})
    global_rules = rules.get("global_rules", {})
    max_weight = global_rules.get("max_single_stock_weight_default", 10)
    if category == "Satellite Stock" and config.get("risk_level") == "high":
        max_weight = global_rules.get("max_high_vol_stock_weight_default", 5)
    elif category == "Crypto":
        max_weight = global_rules.get("crypto_max_weight_default", 5)
    elif category == "Gold":
        max_weight = global_rules.get("gold_target_weight_default", 2)
    return {
        "category": category,
        "style": config.get("style", ""),
        "risk_level": config.get("risk_level", "medium"),
        "buy_rule": config.get("buy_rule", ""),
        "max_weight": max_weight,
    }


def classify_action_by_strategy(symbol: str, raw_signal: str, market_regime: str, data_confidence: int | str) -> str:
    category = get_asset_category(symbol)
    raw = str(raw_signal or "Watch")
    confidence = _confidence_number(data_confidence)
    if confidence < 50:
        return "Watch"
    if "avoid" in raw.lower() or "extended" in raw.lower() or "chase" in raw.lower():
        return "Avoid chasing"
    if market_regime == "Risk-Off" and category in {"Satellite Stock", "Crypto"}:
        return "Reduce risk"
    if category == "Core ETF" and raw in {"Potential Layer 1", "Potential Layer 2", "Hold"}:
        return "DCA only"
    if category in {"Satellite Stock", "Crypto"} and raw in {"Potential Layer 1", "Potential Layer 2", "Deep Pullback Watch"}:
        return "Consider gradual allocation"
    if category in {"Gold", "Taiwan Stock"} and raw in {"Potential Layer 1", "Potential Layer 2", "Deep Pullback Watch"}:
        return "Potential buy zone"
    if raw == "Hold":
        return "Hold"
    return "Watch"


def get_cash_deployment_mode(market_score: int | float, regime: str, portfolio_drift: int | float) -> str:
    score = float(market_score or 0)
    drift = abs(float(portfolio_drift or 0))
    if regime == "Risk-Off" or score < 40:
        return "wait"
    if score >= 75 and drift >= 5:
        return "aggressive"
    if score >= 55:
        return "gradual"
    return "dca_only"


def strategy_warning_for_symbol(symbol: str) -> str:
    category = get_asset_category(symbol)
    if category == "Taiwan Stock":
        return "Taiwan yfinance data is delayed reference only; verify broker quote."
    if category == "Satellite Stock":
        return "High-volatility satellite; avoid chasing and respect target weight."
    if category == "Crypto":
        return "Crypto risk asset; use gradual sizing only when regime supports."
    if category == "Gold":
        return "Defensive hedge; do not chase extended moves."
    return "Broker quote required before trading."


def _normalize_symbol(symbol: str) -> str:
    return str(symbol or "").strip().upper()


def _confidence_number(value: int | str) -> int:
    if isinstance(value, (int, float)):
        return int(value)
    lookup = {"High": 80, "Medium": 60, "Low": 40, "高": 80, "中": 60, "低": 40}
    return lookup.get(str(value), 60)
