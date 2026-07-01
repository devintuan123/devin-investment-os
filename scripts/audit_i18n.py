from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
TARGETS = [ROOT_DIR / "app.py", *sorted((ROOT_DIR / "pages").glob("*.py"))]
STREAMLIT_NAMES = {
    "title",
    "header",
    "subheader",
    "markdown",
    "write",
    "caption",
    "info",
    "warning",
    "error",
    "success",
    "metric",
    "button",
    "selectbox",
    "radio",
    "checkbox",
    "tabs",
    "expander",
    "text_area",
    "number_input",
    "page_link",
}
IGNORED_PATTERNS = [
    re.compile(r"^[A-Z0-9.^=/ _:%-]+$"),
    re.compile(r"^https?://"),
    re.compile(r"^pages/.*\\.py$"),
    re.compile(r"^#[0-9A-Fa-f]{3,6}$"),
    re.compile(r"^[\\-•]+$"),
    re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$"),
]
IGNORED_VALUES = {
    "DI",
    "TWSE",
    "n/a",
    "dynamic",
    "wide",
    "text",
    "streamlit",
    "Devin Investment OS test message.",
}


def main() -> int:
    findings = []
    ignored = []
    for path in TARGETS:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not _is_streamlit_call(node.func):
                continue
            for text_node in _literal_strings(node):
                value = text_node.value.strip()
                if not value:
                    continue
                record = (path.relative_to(ROOT_DIR), text_node.lineno, value)
                if _is_ignored(value):
                    ignored.append(record)
                else:
                    findings.append(record)

    if ignored:
        print("Ignored i18n audit exceptions:")
        for path, line, value in ignored[:80]:
            print(f"- {path}:{line}: {value}")

    if findings:
        print("Suspicious hard-coded UI strings:")
        for path, line, value in findings:
            print(f"- {path}:{line}: {value}")
        return 1

    print("i18n audit passed.")
    return 0


def _is_streamlit_call(func: ast.AST) -> bool:
    if isinstance(func, ast.Attribute):
        if func.attr not in STREAMLIT_NAMES:
            return False
        return _root_name(func) == "st"
    return False


def _root_name(node: ast.AST) -> str | None:
    current = node
    while isinstance(current, ast.Attribute):
        current = current.value
    return current.id if isinstance(current, ast.Name) else None


def _literal_strings(node: ast.Call) -> list[ast.Constant]:
    strings = []
    for arg in list(node.args) + [kw.value for kw in node.keywords if kw.arg not in {"language"}]:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            strings.append(arg)
    return strings


def _is_ignored(value: str) -> bool:
    if value in IGNORED_VALUES:
        return True
    if "{" in value and "}" in value:
        return True
    if value.startswith("<") or value.startswith(".") or value.startswith("["):
        return True
    return any(pattern.match(value) for pattern in IGNORED_PATTERNS)


if __name__ == "__main__":
    raise SystemExit(main())
