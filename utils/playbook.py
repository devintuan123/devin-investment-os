from __future__ import annotations

from utils.scoring import calculate_market_score


def daily_playbook() -> dict:
    score = calculate_market_score({"liquidity": 68, "sentiment": 62, "breadth": 58, "ai_tech": 74, "defensive": 52})
    return {
        "market_regime": score["regime"],
        "market_score": score["score"],
        "what_changed": [
            "AI infrastructure remains the strongest satellite theme.",
            "Breadth is still mixed, so quality and zones matter.",
            "Defensive hedges remain useful portfolio stabilizers.",
        ],
        "do_now": score["actions"],
        "pullback_5": ["VWRA", "0050"],
        "pullback_8": ["GEV", "IEMA", "TSMC / 2330"],
        "pullback_12_15": ["Stage stronger buys", "Keep avoiding blind PLTR/MRVL averaging"],
        "do_not_chase": ["PLTR averaging down", "MRVL averaging down", "Sharp post-news spikes"],
        "reduce_if_fails": ["High-beta AI stocks", "Overweight single-name US exposure"],
        "cash_stance": _cash_stance(score["score"]),
    }


def weekly_playbook() -> dict:
    return {
        "focus": ["Review allocation drift", "Update watch zones", "Check Taiwan and AI satellite exposure"],
        "rebalance_bias": "Prefer core ETF additions before high-beta satellites.",
        "risk_review": "Single-name and high-beta exposure should stay below core ETF exposure.",
    }


def scenario_playbook() -> list[dict]:
    return [
        {"scenario": "Risk On", "action": "Hold winners and buy planned pullbacks."},
        {"scenario": "Neutral", "action": "Keep cash ready and avoid chasing."},
        {"scenario": "Risk Off", "action": "Respect stops and preserve capital."},
    ]


def _cash_stance(score: int) -> str:
    if score >= 80:
        return "Low to moderate cash; deploy only on planned pullbacks."
    if score >= 60:
        return "Moderate cash for 5% and 8% pullback plans."
    if score >= 40:
        return "Elevated cash; wait for confirmation."
    return "High cash; defensive posture."
