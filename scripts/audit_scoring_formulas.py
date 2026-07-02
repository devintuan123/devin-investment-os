from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.market_regime import calculate_market_regime
from utils.watchlist_scoring import score_watchlist
from utils.buy_zone_engine import score_buy_zones
from utils.portfolio_engine import load_portfolio, portfolio_health_score
from utils.sector_heat_engine import calculate_theme_heat_score
from utils.alert_engine import evaluate_alerts

REPORT_MD = ROOT_DIR / "reports" / "data_integrity_current_outputs.md"
REPORT_JSON = ROOT_DIR / "reports" / "data_integrity_current_outputs.json"
FORMULA_DOC = ROOT_DIR / "docs" / "SCORING_FORMULAS.md"
FORMULA_AUDIT_MD = ROOT_DIR / "reports" / "scoring_formula_audit.md"
FORMULA_AUDIT_JSON = ROOT_DIR / "reports" / "scoring_formula_audit.json"


def main() -> int:
    regime = calculate_market_regime()
    current = capture_current_outputs(regime)
    formula_audit = build_formula_audit(regime)
    failures = collect_failures(current, formula_audit)
    current["failures"] = failures
    formula_audit["failures"] = failures
    write_current_outputs(current)
    write_formula_audit(formula_audit)
    write_formula_docs(formula_audit)
    print(FORMULA_AUDIT_MD.read_text(encoding="utf-8"))
    return 1 if failures else 0


def capture_current_outputs(regime: dict) -> dict:
    diagnostics = regime.get("score_diagnostics", [])
    watchlist = score_watchlist()
    buy_zones = score_buy_zones()
    sector = calculate_theme_heat_score().to_dict("records")
    portfolio = portfolio_health_score(load_portfolio())
    alerts = evaluate_alerts()
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "home": {
            "Market Score": regime.get("market_score"),
            "Market Regime": regime.get("market_regime"),
            "Today Action": regime.get("today_action"),
            "Data Confidence": regime.get("confidence_score"),
            "components": regime.get("components", {}),
            "warnings": regime.get("warnings", []),
        },
        "macro_dashboard": diagnostics,
        "daily_playbook": {
            "what_changed": regime.get("what_changed", []),
            "what_to_watch": regime.get("what_to_watch", []),
            "risk_warnings": regime.get("risk_warnings", []),
            "recommended_action": regime.get("recommended_action"),
        },
        "market_regime_engine": regime,
        "watchlist_scoring": watchlist,
        "buy_zones": buy_zones,
        "sector_heat": sector[:20],
        "portfolio_scoring": portfolio,
        "alerts": alerts,
        "identical_scores": regime.get("identical_score_diagnostics", []),
    }


def build_formula_audit(regime: dict) -> dict:
    formulas = []
    for row in regime.get("score_diagnostics", []):
        formulas.append({
            "function_name": component_function_name(row["component"]),
            "purpose": f"Calculate {row['component']} contribution to market regime.",
            "raw_inputs": row.get("raw_inputs"),
            "transformed_inputs": row.get("formula"),
            "score_range": "0-100",
            "clamp_behavior": "bounded with _bound or equivalent min/max clamp",
            "missing_data_behavior": "fallback lowers confidence and shows warning; unavailable providers stay low confidence",
            "weights": row.get("weight"),
            "output_labels": "component score, confidence, warning, fallback_used",
            "assumptions": "read-only decision support; delayed/best-effort market data",
            "data_confidence_adjustment": row.get("confidence"),
            "fallback_default_values": row.get("fallback_used"),
            "formula_version": row.get("formula_version"),
        })
    formulas.extend(extra_formulas())
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "formulas": formulas}


def component_function_name(component: str) -> str:
    mapping = {
        "US Market": "calculate_market_regime/_trend_score",
        "US Tech": "calculate_market_regime/_trend_score",
        "Taiwan": "calculate_market_regime/_trend_score",
        "Crypto": "_crypto_score",
        "Gold": "_gold_score",
        "Macro": "_macro_score",
        "Volatility": "_volatility_score",
        "Liquidity": "_liquidity_score",
        "Sentiment": "_sentiment_score",
        "Breadth": "_breadth_score",
        "Defensive": "_defensive_score",
    }
    return mapping.get(component, component)


def extra_formulas() -> list[dict]:
    return [
        {"function_name": "score_watchlist/score_ticker", "purpose": "Watchlist trend/pullback/action/risk labels", "raw_inputs": "price, MA20, MA60, MA120, 52W drawdown", "score_range": "0-100", "clamp_behavior": "min/max clamp", "missing_data_behavior": "fallback quote/history warning carried to row", "weights": "rule-based", "output_labels": "trend_score, pullback_score, action_label, risk_label", "assumptions": "broker quote must be verified", "formula_version": "watchlist_v1"},
        {"function_name": "score_buy_zones/score_buy_zone", "purpose": "Buy-zone reference bands", "raw_inputs": "price, MA20, MA60, MA120, 52W high, drawdown, volatility", "score_range": "labels not total score", "clamp_behavior": "zone thresholds", "missing_data_behavior": "fallback warning carried to row", "weights": "rule-based", "output_labels": "current_zone_status, action_label, strategy_action", "assumptions": "no Buy Now; gradual/reference only", "formula_version": "buy_zone_v1"},
        {"function_name": "portfolio_health_score", "purpose": "Portfolio drift health", "raw_inputs": "manual holdings, latest prices, target weights", "score_range": "0-100", "clamp_behavior": "90 - drift penalty - missing penalty bounded", "missing_data_behavior": "missing price reduces score and warning", "weights": "drift and missing-data penalties", "output_labels": "score, summary, warnings", "assumptions": "manual portfolio may differ from broker", "formula_version": "portfolio_v1"},
        {"function_name": "calculate_theme_heat_score", "purpose": "Sector/theme heat proxy", "raw_inputs": "theme universe, 5D/20D returns, MA distance, breadth", "score_range": "0-100", "clamp_behavior": "bounded heat and rotation scores", "missing_data_behavior": "proxy warning and fallback history warning", "weights": "50 + return_5d*4 + return_20d*1.5 + MA strength + breadth adjustment", "output_labels": "heat_score, rotation_score, heat_label", "assumptions": "proxy heat only, not exact fund flows", "formula_version": "sector_heat_v1"},
        {"function_name": "evaluate_alerts", "purpose": "Read-only alert trigger logic", "raw_inputs": "market regime, prices, portfolio drift, sector heat, strategy rules", "score_range": "rule triggers", "clamp_behavior": "n/a", "missing_data_behavior": "missing providers create warnings rather than execution", "weights": "rule thresholds", "output_labels": "severity, title, value, warning", "assumptions": "no trades executed", "formula_version": "alerts_v1"},
    ]


def collect_failures(current: dict, audit: dict) -> list[str]:
    failures = []
    components = current["home"]["components"]
    values = list(components.values())
    if any(not isinstance(value, (int, float)) or math.isnan(float(value)) or math.isinf(float(value)) for value in values):
        failures.append("component score contains NaN/inf or nonnumeric value")
    if any(float(value) < 0 or float(value) > 100 for value in values):
        failures.append("component score outside 0-100")
    if len(set(values)) == 1:
        failures.append("all major component scores are identical")
    diagnostics = current["macro_dashboard"]
    if diagnostics:
        fallback_ratio = sum(1 for row in diagnostics if row.get("fallback_used")) / len(diagnostics)
        if fallback_ratio > 0.5:
            failures.append("more than 50% of components use fallback values")
        if any(row.get("fallback_used") and row.get("confidence", 100) > 55 for row in diagnostics):
            failures.append("fallback data shown with high confidence")
    return failures


def write_current_outputs(current: dict) -> None:
    REPORT_JSON.write_text(json.dumps(current, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    lines = ["# Data Integrity Current Outputs", "", f"Generated: {current['generated_at']}", "", "## Home / Market Regime"]
    for key, value in current["home"].items():
        lines.append(f"- {key}: {value}")
    lines.append("\n## Score Diagnostics")
    for row in current["macro_dashboard"]:
        lines.append(f"- {row['component']}: score={row['score']} provider={row['provider']} timestamp={row['latest_timestamp']} confidence={row['confidence']} fallback={row['fallback_used']} formula={row['formula_version']} warning={row['warning'] or 'none'} raw={row['raw_inputs']}")
    lines.append("\n## Identical Scores")
    lines.extend([f"- score={row['score']} components={row['components']} justification={row['justification']}" for row in current["identical_scores"]] or ["- none"])
    lines.append("\n## Portfolio")
    lines.append(str(current["portfolio_scoring"]))
    lines.append("\n## Failures")
    lines.extend([f"- {failure}" for failure in current.get("failures", [])] or ["- none"])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_formula_audit(audit: dict) -> None:
    FORMULA_AUDIT_JSON.write_text(json.dumps(audit, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    lines = ["# Scoring Formula Audit", "", f"Generated: {audit['generated_at']}", "", f"Status: {'FAIL' if audit.get('failures') else 'PASS'}"]
    for formula in audit["formulas"]:
        lines.append(f"\n## {formula['function_name']}")
        for key, value in formula.items():
            if key != "function_name":
                lines.append(f"- {key}: {value}")
    lines.append("\n## Failures")
    lines.extend([f"- {failure}" for failure in audit.get("failures", [])] or ["- none"])
    FORMULA_AUDIT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_formula_docs(audit: dict) -> None:
    lines = ["# Scoring Formulas", "", "Read-only scoring documentation. Scores are decision-support references only and must not be treated as broker quotes or execution instructions."]
    for formula in audit["formulas"]:
        lines.append(f"\n## {formula['function_name']}")
        for key, value in formula.items():
            if key != "function_name":
                lines.append(f"- {key.replace('_', ' ').title()}: {value}")
    FORMULA_DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
