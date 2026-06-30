def calculate_market_score(inputs: dict) -> dict:
    weights = {
        "liquidity": 0.25,
        "sentiment": 0.20,
        "breadth": 0.20,
        "ai_tech": 0.20,
        "defensive": 0.15,
    }

    score = 0
    for key, weight in weights.items():
        value = float(inputs.get(key, 50))
        score += max(0, min(100, value)) * weight

    final_score = int(round(score))
    regime = _regime_for_score(final_score)

    return {
        "score": final_score,
        "regime": regime,
        "summary": f"Market score is {final_score}/100. Current regime: {regime}.",
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
