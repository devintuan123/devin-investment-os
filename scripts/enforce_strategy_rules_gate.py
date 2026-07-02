from __future__ import annotations

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def main() -> int:
    findings = []
    required = [ROOT_DIR / "data" / "strategy_rules.yaml", ROOT_DIR / "utils" / "strategy_rules.py"]
    for path in required:
        if not path.exists():
            findings.append(f"Missing {path.relative_to(ROOT_DIR)}")
    forbidden = ["Buy Now", "Must Buy", "Immediate Buy", "Guaranteed"]
    source_paths = [
        ROOT_DIR / "utils" / "buy_zone_engine.py",
        ROOT_DIR / "modules" / "daily_playbook" / "__init__.py",
        ROOT_DIR / "scripts" / "send_daily_report.py",
    ]
    for path in source_paths:
        text = path.read_text(encoding="utf-8")
        if "strategy_rules" not in text and "strategy_action" not in text:
            findings.append(f"Strategy rules not referenced by {path.relative_to(ROOT_DIR)}")
        for phrase in forbidden:
            if phrase in text:
                findings.append(f"Forbidden action language in {path.relative_to(ROOT_DIR)}: {phrase}")
    if findings:
        print("FAIL strategy rules gate")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PASS strategy rules gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
