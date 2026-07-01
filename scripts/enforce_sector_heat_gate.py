from __future__ import annotations

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def main() -> int:
    findings = []
    required_files = [
        "utils/sector_heat_engine.py",
        "data/theme_universe.csv",
        "modules/sector_heat/__init__.py",
        "pages/11_Sector_Heat.py",
    ]
    for item in required_files:
        if not (ROOT_DIR / item).exists():
            findings.append(f"Missing {item}")
    daily = (ROOT_DIR / "modules" / "daily_playbook" / "__init__.py").read_text(encoding="utf-8")
    telegram = (ROOT_DIR / "scripts" / "send_daily_report.py").read_text(encoding="utf-8")
    for source_name, source in [("Daily Playbook", daily), ("Telegram report", telegram)]:
        if "sector_heat" not in source and "Sector Heat" not in source:
            findings.append(f"{source_name} does not reference sector heat")
        if "proxy_heat_warning" not in source:
            findings.append(f"{source_name} does not show proxy heat limitations")
    engine = (ROOT_DIR / "utils" / "sector_heat_engine.py").read_text(encoding="utf-8") if (ROOT_DIR / "utils" / "sector_heat_engine.py").exists() else ""
    if "not exact fund flows" not in engine:
        findings.append("Sector heat engine must state not exact fund flows")
    if findings:
        print("FAIL sector heat gate")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PASS sector heat gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
