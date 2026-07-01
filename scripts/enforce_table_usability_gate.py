from __future__ import annotations

import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
TARGETS = [ROOT_DIR / "app.py", *sorted((ROOT_DIR / "pages").glob("*.py"))]
FORBIDDEN_CALLS = ("st.table(", "st.dataframe(", "st.write(df", "st.write(view", "st.data_editor(")
ALLOWLIST_MARKERS = ("Editable CSV editor",)
NO_COLUMN_PATTERN = re.compile(r"[\"'](?:No\.|No|no|index|Index|#)[\"']")


def main() -> int:
    findings = []
    for path in TARGETS:
        lines = path.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            if any(call in line for call in FORBIDDEN_CALLS):
                previous = lines[line_number - 2] if line_number >= 2 else ""
                if "st.data_editor(" in line and any(marker in previous for marker in ALLOWLIST_MARKERS):
                    continue
                findings.append((path.relative_to(ROOT_DIR), line_number, line.strip(), "Use render_interactive_table(...) or document an editor allowlist."))
            if NO_COLUMN_PATTERN.search(line) and "NO_COLUMNS" not in line and "t(\"no\")" not in line and "t('no')" not in line:
                findings.append((path.relative_to(ROOT_DIR), line_number, line.strip(), "Remove useless No./index display columns."))

    if findings:
        print("FAIL table usability gate")
        for path, line_number, line, suggestion in findings:
            print(f"- {path}:{line_number}: {line}")
            print(f"  suggested replacement: {suggestion}")
        return 1

    print("PASS table usability gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
