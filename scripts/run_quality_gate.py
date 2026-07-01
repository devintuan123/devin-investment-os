from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

CHECKS = [
    ("compileall", [sys.executable, "-m", "compileall", "-q", "."]),
    ("audit_i18n", [sys.executable, "scripts/audit_i18n.py"]),
    ("audit_table_i18n", [sys.executable, "scripts/audit_table_i18n.py"]),
    ("ui_text_snapshot", [sys.executable, "scripts/ui_text_snapshot.py"]),
    ("telegram_dry_run", [sys.executable, "scripts/send_daily_report.py", "--dry-run"]),
]


def main() -> int:
    print("Devin Investment OS quality gate")
    failures = []

    for name, command in CHECKS:
        script_path = _script_path(command)
        if script_path and not script_path.exists():
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
