from __future__ import annotations

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
MODULES = ["home", "macro", "portfolio", "watchlist", "asset_scores", "daily_playbook", "data_quality", "settings", "history", "buy_zones", "sector_heat"]
SHARED = ["ui_shell.py", "tables.py", "labels.py"]
PAGES = [ROOT_DIR / "app.py", *sorted((ROOT_DIR / "pages").glob("*.py"))]


def main() -> int:
    findings = []
    modules_dir = ROOT_DIR / "modules"
    if not modules_dir.exists():
        findings.append("modules/ is missing")
    for name in MODULES:
        path = modules_dir / name / "__init__.py"
        if not path.exists():
            findings.append(f"Missing module: modules/{name}/__init__.py")
        elif "def render(lang: str)" not in path.read_text(encoding="utf-8"):
            findings.append(f"Module lacks render(lang: str): {path.relative_to(ROOT_DIR)}")
    for filename in SHARED:
        if not (modules_dir / "shared" / filename).exists():
            findings.append(f"Missing shared helper: modules/shared/{filename}")
    for page in PAGES:
        if page.name == "8_TradingView_Alerts.py":
            continue
        source = page.read_text(encoding="utf-8")
        non_empty = [line for line in source.splitlines() if line.strip() and not line.strip().startswith("#")]
        if len(non_empty) > 12:
            findings.append(f"Page wrapper too large: {page.relative_to(ROOT_DIR)} has {len(non_empty)} non-empty lines")
        if "render_page_shell" not in source or "render(lang)" not in source:
            findings.append(f"Page does not use module shell: {page.relative_to(ROOT_DIR)}")

    if findings:
        print("FAIL modular pages gate")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PASS modular pages gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
