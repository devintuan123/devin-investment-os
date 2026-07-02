from __future__ import annotations

import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def main() -> int:
    findings = []
    required = [
        ROOT_DIR / "scripts" / "create_daily_snapshot.py",
        ROOT_DIR / "utils" / "snapshot_store.py",
        ROOT_DIR / "data" / "snapshots",
    ]
    for path in required:
        if not path.exists():
            findings.append(f"Missing {path.relative_to(ROOT_DIR)}")
    history = (ROOT_DIR / "modules" / "history" / "__init__.py").read_text(encoding="utf-8")
    if "snapshot_store" not in history:
        findings.append("History page does not reference snapshot_store")
    for path in (ROOT_DIR / "data" / "snapshots").glob("*.json"):
        text = path.read_text(encoding="utf-8")
        if any(term in text.lower() for term in ["api_key", "secret", "token", "password"]):
            findings.append(f"Snapshot may contain secret-like field: {path.name}")
        try:
            json.loads(text)
        except json.JSONDecodeError:
            findings.append(f"Snapshot is not valid JSON: {path.name}")
    if findings:
        print("FAIL snapshot gate")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PASS snapshot gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
