WEIGHTS = {
    "liquidity": 0.25,
    "sentiment": 0.20,
    "breadth": 0.20,
    "ai_tech": 0.20,
    "defensive": 0.15,
}

CATEGORY_META = {
    "liquidity": ("Liquidity", ["US10Y", "Real Yield", "DXY", "FedWatch"]),
    "sentiment": ("Sentiment", ["VIX", "Put/Call Ratio", "Fear & Greed"]),
    "breadth": ("Breadth", ["Advance/Decline", "New High/New Low", "% above 200MA"]),
    "ai_tech": ("AI / Tech", ["SOX", "NVDA", "TSMC ADR", "GEV"]),
    "defensive": ("Defensive / Hedge", ["Gold", "BTC", "SGLD"]),
}


def calculate_market_score(inputs: dict) -> dict:
    categories = {}
    total = 0.0

    for key, weight in WEIGHTS.items():
        score = _bounded_score(inputs.get(key, 55))
        label, indicators = CATEGORY_META[key]
        categories[key] = {
            "score": score,
            "label": _condition_label(score),
            "explanation": _category_explanation(label, score),
            "indicators": indicators,
        }
        total += score * weight

    final_score = int(round(total))
    regime = _regime_for_score(final_score)

    return {
        "score": final_score,
        "regime": regime,
        "summary": f"{regime}: market score is {final_score}/100.",
        "categories": categories,
        "actions": _actions_for_score(final_score),
    }


def _regime_for_score(score: int) -> str:
    if score >= 80:
        return "Risk On"
    if score >= 60:
        return "Bullish Neutral"
    if score >= 40:
        return "Neutral"
    if score >= 20:
        return "Risk Off"
    return "Defensive"


def _bounded_score(value: object) -> int:
    try:
        return int(max(0, min(100, float(value))))
    except (TypeError, ValueError):
        return 55


def _condition_label(score: int) -> str:
    if score >= 80:
        return "Strong"
    if score >= 60:
        return "Constructive"
    if score >= 40:
        return "Mixed"
    if score >= 20:
        return "Weak"
    return "Defensive"


def _category_explanation(label: str, score: int) -> str:
    if score >= 60:
        return f"{label} conditions support selective risk."
    if score >= 40:
        return f"{label} conditions are mixed and need confirmation."
    return f"{label} conditions argue for tighter risk control."


def _actions_for_score(score: int) -> list[str]:
    if score >= 80:
        return ["Hold winners", "Buy planned pullbacks", "Trim extended spikes"]
    if score >= 60:
        return ["Hold core positions", "Buy Zone only", "Watch high-beta risk"]
    if score >= 40:
        return ["Stay selective", "Keep cash ready", "Avoid chasing"]
    if score >= 20:
        return ["Reduce weak exposure", "Respect stops", "Prefer defensive hedges"]
    return ["Avoid new risk", "Raise cash", "Review stop levels"]
