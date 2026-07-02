from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
CHECKS = [
    [sys.executable, "scripts/audit_ui_layout_encoding.py"],
    [sys.executable, "scripts/ui_visual_text_snapshot.py"],
]


def main() -> int:
    failures = []
    for command in CHECKS:
        print("[RUN] " + " ".join(command[1:]))
        result = subprocess.run(command, cwd=ROOT_DIR, text=True, capture_output=True, encoding="utf-8", errors="replace")
        if result.stdout:
            print(result.stdout.rstrip())
        if result.stderr:
            print(result.stderr.rstrip())
        if result.returncode != 0:
            failures.append(" ".join(command[1:]))
    if failures:
        print("UI layout/encoding gate failed: " + ", ".join(failures))
        return 1
    print("UI layout/encoding gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
