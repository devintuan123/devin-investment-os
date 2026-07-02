from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.market_regime import calculate_market_regime

CHECKS = [
    [sys.executable, "scripts/audit_data_sources.py"],
    [sys.executable, "scripts/audit_scoring_formulas.py"],
    [sys.executable, "scripts/test_scoring_integrity.py"],
]


def main() -> int:
    failures = []
    for command in CHECKS:
        print("[RUN] " + " ".join(command[1:]))
        result = subprocess.run(command, cwd=ROOT_DIR, text=True, capture_output=True)
        if result.stdout:
            print(result.stdout.rstrip())
        if result.stderr:
            print(result.stderr.rstrip())
        if result.returncode != 0:
            failures.append(" ".join(command[1:]))
    failures.extend(check_active_scores())
    if failures:
        print("Data integrity gate failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Data integrity gate passed.")
    return 0


def check_active_scores() -> list[str]:
    failures = []
    regime = calculate_market_regime()
    components = regime.get("components", {})
    values = list(components.values())
    if any(not isinstance(value, (int, float)) or math.isnan(float(value)) or math.isinf(float(value)) for value in values):
        failures.append("active component score is NaN/inf/non-numeric")
    if any(float(value) < 0 or float(value) > 100 for value in values):
        failures.append("active component score outside 0-100")
    if values and len(set(values)) == 1:
        failures.append("all major component scores are identical without justification")
    diagnostics = regime.get("score_diagnostics", [])
    if diagnostics:
        fallback_count = sum(1 for row in diagnostics if row.get("fallback_used"))
        if fallback_count / len(diagnostics) > 0.5:
            failures.append("more than 50% of components use fallback values")
        if any(row.get("fallback_used") and row.get("confidence", 100) > 55 for row in diagnostics):
            failures.append("missing/fallback data shown as high confidence")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
