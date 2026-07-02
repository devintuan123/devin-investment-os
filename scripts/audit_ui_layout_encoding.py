from __future__ import annotations

import ast
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
REPORT_MD = ROOT_DIR / "reports" / "ui_layout_encoding_audit.md"
REPORT_JSON = ROOT_DIR / "reports" / "ui_layout_encoding_issues.json"
SCAN_DIRS = ["app.py", "pages", "modules", "utils", "scripts", "data", "reports"]
TEXT_SUFFIXES = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".toml"}
SKIP_PREFIXES = {"scripts/audit_ui_layout_encoding.py", "scripts/ui_visual_text_snapshot.py","reports/v0_3_validation_report.txt", "reports/v0_5_alerts_zh.log", "reports/v0_5_daily_workflow.log", "reports/v0_5_full_runtime_audit.log", "reports/v0_5_post_deployment_validation.md", "reports/v0_5_quality_gate.log", "reports/v0_5_telegram_zh.log"}
MOJIBAKE_PATTERNS = ["嚙", "�", "癟", "疆", "矇", "疇", "瓊", "癡", "璽", "", "", "", "", "", ""]
RAW_UNICODE_RE = re.compile(r"\\u[0-9a-fA-F]{4}")
OPEN_WITHOUT_ENCODING_RE = re.compile(r"\bopen\s*\([^\n)]*(?:'|\")r?[^\n)]*\)(?![^\n]*encoding\s*=)")
PANDAS_CSV_WITHOUT_ENCODING_RE = re.compile(r"\.((read_csv)|(to_csv))\s*\([^\n)]*\)(?![^\n]*encoding\s*=)")
JSON_DUMP_ASCII_RE = re.compile(r"json\.dumps?\s*\([^\n)]*\)(?![^\n]*ensure_ascii\s*=\s*False)")


def main() -> int:
    issues = []
    for path in iter_files():
        rel = path.relative_to(ROOT_DIR).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            issues.append(issue(rel, "critical", "utf8_decode", str(exc), 0))
            continue
        issues.extend(scan_text(rel, text))
        if path.suffix == ".py":
            issues.extend(scan_python_layout(rel, text))
    write_reports(issues)
    print(REPORT_MD.read_text(encoding="utf-8"))
    return 1 if any(item["severity"] == "critical" for item in issues) else 0


def iter_files():
    for item in SCAN_DIRS:
        path = ROOT_DIR / item
        if path.is_file():
            yield path
        elif path.exists():
            for child in path.rglob("*"):
                rel = child.relative_to(ROOT_DIR).as_posix()
                if child.is_file() and child.suffix.lower() in TEXT_SUFFIXES and rel not in SKIP_PREFIXES:
                    yield child


def scan_text(rel: str, text: str) -> list[dict]:
    issues = []
    for pattern in MOJIBAKE_PATTERNS:
        for match in re.finditer(re.escape(pattern), text):
            issues.append(issue(rel, "critical", "mojibake", f"found {pattern!r}", line_number(text, match.start())))
    for match in RAW_UNICODE_RE.finditer(text):
        issues.append(issue(rel, "critical", "raw_unicode_escape", match.group(0), line_number(text, match.start())))
    if rel.endswith(".py"):
        for number, line in enumerate(text.splitlines(), start=1):
            compact = line.strip()
            if re.search(r"(?<![A-Za-z0-9_])open\(", compact) and "encoding=" not in compact and not compact.startswith("#"):
                issues.append(issue(rel, "warning", "open_without_encoding", compact[:120], number))
            if ("pd.read_csv(" in compact or ".to_csv(" in compact) and "encoding=" not in compact:
                issues.append(issue(rel, "warning", "csv_without_encoding", compact[:120], number))
            if ("json.dumps(" in compact or "json.dump(" in compact) and "ensure_ascii=False" not in compact:
                issues.append(issue(rel, "warning", "json_without_ensure_ascii_false", compact[:120], number))
    return issues


def scan_python_layout(rel: str, text: str) -> list[dict]:
    issues = []
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return [issue(rel, "critical", "syntax_error", str(exc), exc.lineno or 0)]
    set_page_calls = [node for node in ast.walk(tree) if is_call(node, "st", "set_page_config")]
    if set_page_calls and rel != "modules/shared/ui_shell.py":
        issues.append(issue(rel, "critical", "direct_set_page_config", "use modules.shared.ui_shell.configure_page", getattr(set_page_calls[0], "lineno", 0)))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and is_attr(node.func, "dataframe"):
            for kw in node.keywords:
                if kw.arg == "height" and isinstance(kw.value, ast.Constant) and kw.value.value is None:
                    issues.append(issue(rel, "critical", "dataframe_height_none", "st.dataframe height=None", node.lineno))
    return issues


def is_call(node, base: str, attr: str) -> bool:
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == base and node.func.attr == attr


def is_attr(node, attr: str) -> bool:
    return isinstance(node, ast.Attribute) and node.attr == attr


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def issue(file: str, severity: str, kind: str, detail: str, line: int) -> dict:
    return {"file": file, "line": line, "severity": severity, "kind": kind, "detail": detail}


def write_reports(issues: list[dict]) -> None:
    REPORT_MD.parent.mkdir(exist_ok=True)
    payload = {"generated_at": datetime.now(timezone.utc).isoformat(), "issue_count": len(issues), "issues": issues}
    REPORT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = ["# UI Layout and Encoding Audit", "", f"Generated: {payload['generated_at']}", f"Status: {'FAIL' if any(i['severity'] == 'critical' for i in issues) else 'PASS'}", "", "## Issues"]
    if issues:
        for item in issues:
            lines.append(f"- [{item['severity']}] {item['file']}:{item['line']} {item['kind']}: {item['detail']}")
    else:
        lines.append("- none")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
