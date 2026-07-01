from __future__ import annotations

import ast
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
TARGETS = [ROOT_DIR / "app.py", *sorted((ROOT_DIR / "pages").glob("*.py"))]
TABLE_CALLS = {"dataframe", "table"}
WRITE_NAMES = {"df", "view", "rows", "positions", "portfolio", "scores"}


def main() -> int:
    findings = []
    for path in TARGETS:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not _is_streamlit_call(node.func):
                continue
            call_name = node.func.attr
            segment = ast.get_source_segment(source, node) or ""
            if call_name in TABLE_CALLS:
                findings.append((path.relative_to(ROOT_DIR), node.lineno, call_name, segment.strip()))
            if call_name == "write" and _looks_like_dataframe_write(node):
                findings.append((path.relative_to(ROOT_DIR), node.lineno, call_name, segment.strip()))

    if findings:
        print("Table i18n audit failed:")
        for path, line, call_name, segment in findings:
            print(f"- {path}:{line}: st.{call_name} should use render_interactive_table: {segment}")
        return 1

    print("table i18n audit passed.")
    return 0


def _is_streamlit_call(func: ast.AST) -> bool:
    return isinstance(func, ast.Attribute) and _root_name(func) == "st"


def _root_name(node: ast.AST) -> str | None:
    current = node
    while isinstance(current, ast.Attribute):
        current = current.value
    return current.id if isinstance(current, ast.Name) else None


def _looks_like_dataframe_write(node: ast.Call) -> bool:
    if not node.args:
        return False
    first = node.args[0]
    if isinstance(first, ast.Name) and first.id in WRITE_NAMES:
        return True
    if isinstance(first, ast.Subscript) and isinstance(first.value, ast.Name) and first.value.id in WRITE_NAMES:
        return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())
