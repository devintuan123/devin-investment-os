from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

CHECKS = [
    ("compileall", [sys.executable, "-m", "compileall", "-q", "."]),
    ("full_runtime_audit", [sys.executable, "scripts/full_runtime_audit.py"]),
    ("enforce_i18n_hard_gate", [sys.executable, "scripts/enforce_i18n_hard_gate.py"]),
    ("enforce_table_usability_gate", [sys.executable, "scripts/enforce_table_usability_gate.py"]),
    ("enforce_modular_pages_gate", [sys.executable, "scripts/enforce_modular_pages_gate.py"]),
    ("enforce_portfolio_management_gate", [sys.executable, "scripts/enforce_portfolio_management_gate.py"]),
    ("enforce_sector_heat_gate", [sys.executable, "scripts/enforce_sector_heat_gate.py"]),
    ("enforce_strategy_rules_gate", [sys.executable, "scripts/enforce_strategy_rules_gate.py"]),
    ("enforce_snapshot_gate", [sys.executable, "scripts/enforce_snapshot_gate.py"]),
    ("enforce_alert_gate", [sys.executable, "scripts/enforce_alert_gate.py"]),
    ("audit_i18n", [sys.executable, "scripts/audit_i18n.py"]),
    ("audit_table_i18n", [sys.executable, "scripts/audit_table_i18n.py"]),
    ("audit_navigation_i18n", [sys.executable, "scripts/audit_navigation_i18n.py"]),
    ("ui_text_snapshot", [sys.executable, "scripts/ui_text_snapshot.py"]),
    ("telegram_dry_run_zh", [sys.executable, "scripts/send_daily_report.py", "--dry-run", "--lang", "zh"]),
    ("telegram_dry_run_en", [sys.executable, "scripts/send_daily_report.py", "--dry-run", "--lang", "en"]),
]
MANDATORY = {
    "compileall",
    "full_runtime_audit",
    "enforce_i18n_hard_gate",
    "enforce_table_usability_gate",
    "enforce_modular_pages_gate",
    "enforce_portfolio_management_gate",
    "enforce_sector_heat_gate",
    "enforce_strategy_rules_gate",
    "enforce_snapshot_gate",
    "enforce_alert_gate",
    "telegram_dry_run_zh",
    "telegram_dry_run_en",
}


def main() -> int:
    print("Devin Investment OS quality gate")
    failures = []

    for name, command in CHECKS:
        script_path = _script_path(command)
        if script_path and not script_path.exists():
            if name in MANDATORY:
                print(f"[FAIL] {name}: mandatory script missing ({script_path.relative_to(ROOT_DIR)})")
                failures.append(name)
            else:
                print(f"[WARN] {name}: optional script missing ({script_path.relative_to(ROOT_DIR)})")
            continue

        print(f"[RUN] {name}")
        result = subprocess.run(command, cwd=ROOT_DIR, text=True, capture_output=True)
        if result.stdout:
            print(result.stdout.rstrip())
        if result.stderr:
            print(result.stderr.rstrip())

        if result.returncode == 0:
            print(f"[PASS] {name}")
        else:
            print(f"[FAIL] {name} exited {result.returncode}")
            failures.append(name)

    if failures:
        print("Quality gate failed: " + ", ".join(failures))
        return 1

    print("Quality gate passed.")
    return 0


def _script_path(command: list[str]) -> Path | None:
    for part in command:
        if part.startswith("scripts/") or part.startswith("scripts\\"):
            return ROOT_DIR / part
    return None


if __name__ == "__main__":
    raise SystemExit(main())
