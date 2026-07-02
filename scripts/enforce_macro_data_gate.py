from __future__ import annotations

import json
from pathlib import Path
import sys

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
REPORT_DIR = ROOT_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

from utils.fred_provider import get_macro_series_snapshot
from utils.market_data import get_market_proxy_snapshot
from utils.scoring_diagnostics import (
    build_score_diagnostics,
    detect_missing_macro_inputs,
    detect_suspicious_identical_scores,
    summarize_score_data_quality,
)


def main() -> int:
    issues: list[str] = []
    checks: list[str] = []

    _check_macro_page_source(issues, checks)
    _check_provider_rows(issues, checks)
    _check_score_quality(issues, checks)

    lines = ["# Macro Data Gate Report", "", "## Checks", *[f"- {check}" for check in checks], "", "## Issues"]
    lines.extend([f"- {issue}" for issue in issues] if issues else ["- None"])
    (REPORT_DIR / "macro_data_gate_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (REPORT_DIR / "macro_data_gate_report.json").write_text(
        json.dumps({"checks": checks, "issues": issues}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if issues:
        print("FAIL macro data gate")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("PASS macro data gate")
    return 0


def _check_macro_page_source(issues: list[str], checks: list[str]) -> None:
    source = (ROOT_DIR / "modules" / "macro" / "__init__.py").read_text(encoding="utf-8")
    required = {
        "FRED raw data section": "fred_raw_data",
        "Market Proxy Data section": "market_proxy_data",
        "Score Diagnostics section": "score_diagnostics",
        "FRED snapshot call": "get_macro_series_snapshot",
        "market proxy snapshot call": "get_market_proxy_snapshot",
        "top missing-data warning": "macro_missing_data_warning",
    }
    for label, token in required.items():
        if token not in source:
            issues.append(f"Macro Dashboard missing {label}.")
        else:
            checks.append(f"Macro Dashboard includes {label}.")


def _check_provider_rows(issues: list[str], checks: list[str]) -> None:
    fred = get_macro_series_snapshot()
    proxies = get_market_proxy_snapshot()
    for label, frame in [("FRED", fred), ("yfinance market proxy", proxies)]:
        if frame.empty:
            issues.append(f"{label} provider returned zero rows without visible diagnostics.")
            continue
        checks.append(f"{label} provider returned {len(frame)} diagnostic rows.")
        missing_mask = frame["missing"].fillna(False).astype(bool) if "missing" in frame else pd.Series(False, index=frame.index)
        fallback_mask = frame["fallback_used"].fillna(False).astype(bool) if "fallback_used" in frame else pd.Series(False, index=frame.index)
        if "latest_date" in frame and frame[~missing_mask]["latest_date"].isna().any():
            issues.append(f"{label} has valid rows with missing timestamps.")
        high_conf_missing = frame[(missing_mask | fallback_mask) & (frame["confidence"].fillna(0) >= 60)]
        if not high_conf_missing.empty:
            issues.append(f"{label} missing/fallback rows are shown with normal confidence.")


def _check_score_quality(issues: list[str], checks: list[str]) -> None:
    diagnostics = build_score_diagnostics()
    quality = summarize_score_data_quality()
    missing = detect_missing_macro_inputs()
    identical = detect_suspicious_identical_scores()

    if diagnostics.empty:
        issues.append("Score diagnostics returned zero rows.")
        return

    fallback_count = int(diagnostics["fallback_used"].fillna(False).sum()) if "fallback_used" in diagnostics else 0
    if fallback_count > len(diagnostics) / 2 and quality["confidence"] > 50:
        issues.append("More than 50% fallback components without low top-level confidence.")
    else:
        checks.append("Fallback-heavy scores reduce top-level confidence.")

    suspicious = [row for row in identical if row.get("suspicious")]
    if suspicious:
        checks.append("Suspicious identical scores are explicitly flagged.")
    if len(diagnostics["score"].dropna().unique()) == 1 and not suspicious:
        issues.append("All macro component scores are identical without fallback diagnostics.")

    if missing:
        checks.append(f"Missing/fallback macro inputs are visible ({len(missing)} issue rows).")
    else:
        checks.append("No missing/fallback macro inputs detected.")


if __name__ == "__main__":
    raise SystemExit(main())
