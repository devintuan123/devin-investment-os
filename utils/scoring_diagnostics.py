from __future__ import annotations

from statistics import mean
from typing import Any

import pandas as pd

from utils.fred_provider import get_macro_series_snapshot
from utils.market_data import get_market_proxy_snapshot
from utils.market_regime import calculate_market_regime


MACRO_COMPONENTS = {
    "Macro",
    "Volatility",
    "Liquidity",
    "Sentiment",
    "Breadth",
    "Defensive",
    "US Market",
    "US Tech",
    "Taiwan",
    "Taiwan Market",
    "Crypto",
    "Gold",
}


def build_score_diagnostics(lang: str = "zh") -> pd.DataFrame:
    regime = calculate_market_regime()
    rows = regime.get("score_diagnostics", [])
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    frame["component_has_input_warning"] = frame["warning"].fillna("").astype(str).str.len() > 0
    frame["suspicious_identical_score"] = frame["component"].isin(_identical_components(regime))
    frame["lang"] = lang
    return frame


def get_component_input_trace(component: str) -> dict[str, Any]:
    diagnostics = build_score_diagnostics()
    matches = diagnostics[diagnostics["component"].astype(str).str.lower() == str(component).lower()]
    return matches.iloc[0].to_dict() if not matches.empty else {}


def detect_suspicious_identical_scores() -> list[dict[str, Any]]:
    regime = calculate_market_regime()
    rows = []
    diagnostics = pd.DataFrame(regime.get("score_diagnostics", []))
    for group in regime.get("identical_score_diagnostics", []):
        components = group.get("components", [])
        matching = diagnostics[diagnostics["component"].isin(components)] if not diagnostics.empty else pd.DataFrame()
        fallback_count = int(matching.get("fallback_used", pd.Series(dtype=bool)).fillna(False).sum()) if not matching.empty else 0
        rows.append(
            {
                "score": group.get("score"),
                "components": components,
                "fallback_count": fallback_count,
                "suspicious": fallback_count > 0,
                "warning": "Identical scores include fallback components; inspect raw data before trusting score."
                if fallback_count
                else group.get("justification", ""),
            }
        )
    return rows


def detect_missing_macro_inputs() -> list[dict[str, Any]]:
    missing = []
    for source, frame in (("FRED", get_macro_series_snapshot()), ("yfinance", get_market_proxy_snapshot())):
        if frame.empty:
            missing.append({"provider": source, "item": "all", "warning": f"{source} returned zero diagnostic rows"})
            continue
        for row in frame.to_dict("records"):
            if bool(row.get("missing")) or bool(row.get("fallback_used")) or row.get("error"):
                missing.append(
                    {
                        "provider": source,
                        "item": row.get("series_id") or row.get("symbol"),
                        "warning": row.get("error") or row.get("freshness_status") or "missing input",
                    }
                )
    return missing


def summarize_score_data_quality() -> dict[str, Any]:
    fred = get_macro_series_snapshot()
    proxies = get_market_proxy_snapshot()
    diagnostics = build_score_diagnostics()
    frames = [frame for frame in [fred, proxies] if not frame.empty]
    total_rows = int(sum(len(frame) for frame in frames))
    missing_rows = int(sum(frame.get("missing", pd.Series(dtype=bool)).fillna(False).sum() for frame in frames))
    fallback_rows = int(sum(frame.get("fallback_used", pd.Series(dtype=bool)).fillna(False).sum() for frame in frames))
    confidence_values = []
    for frame in [fred, proxies, diagnostics]:
        if not frame.empty and "confidence" in frame:
            confidence_values.extend([float(value) for value in frame["confidence"].dropna().tolist()])
    confidence = int(round(mean(confidence_values))) if confidence_values else 20
    fallback_component_count = int(diagnostics.get("fallback_used", pd.Series(dtype=bool)).fillna(False).sum()) if not diagnostics.empty else 0
    warning_count = len(detect_missing_macro_inputs())
    if fallback_component_count > len(diagnostics) / 2 if not diagnostics.empty else False:
        confidence = min(confidence, 45)
    if missing_rows:
        confidence = min(confidence, 55)
    return {
        "total_rows": total_rows,
        "valid_rows": total_rows - missing_rows,
        "missing_rows": missing_rows,
        "fallback_rows": fallback_rows,
        "fallback_component_count": fallback_component_count,
        "component_count": int(len(diagnostics)),
        "confidence": confidence,
        "warnings": warning_count,
        "fred_connected": bool(not fred.empty and fred.get("connected", pd.Series(dtype=bool)).fillna(False).any()),
        "yfinance_connected": bool(not proxies.empty and proxies.get("connected", pd.Series(dtype=bool)).fillna(False).any()),
    }


def _identical_components(regime: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for group in regime.get("identical_score_diagnostics", []):
        names.update(group.get("components", []))
    return names
