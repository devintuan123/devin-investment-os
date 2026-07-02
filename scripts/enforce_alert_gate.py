from __future__ import annotations

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def main() -> int:
    findings = []
    required = [
        ROOT_DIR / "data" / "alert_rules.yaml",
        ROOT_DIR / "utils" / "alert_engine.py",
        ROOT_DIR / "scripts" / "send_alerts.py",
    ]
    for path in required:
        if not path.exists():
            findings.append(f"Missing {path.relative_to(ROOT_DIR)}")
    engine = (ROOT_DIR / "utils" / "alert_engine.py").read_text(encoding="utf-8")
    if "suppress_duplicate_alerts" not in engine or "alert_state.json" not in engine:
        findings.append("Duplicate suppression or alert state missing")
    forbidden = ["place_order", "withdraw", "futures", "margin", "auto_order"]
    if any(term in engine.lower() for term in forbidden):
        findings.append("Trading/execution language found in alert engine")
    if findings:
        print("FAIL alert gate")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PASS alert gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
