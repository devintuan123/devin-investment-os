from __future__ import annotations

import ast
from pathlib import Path
import sys

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.i18n import LANG_ZH, TRANSLATIONS, set_lang, t, translate_term
from utils.table_i18n import translate_dataframe


REQUIRED_TERMS_PATH = ROOT_DIR / "data" / "i18n_required_terms.yaml"
NAV_FORBIDDEN = ["Home", "Macro Dashboard", "Portfolio", "Watchlist", "Asset Scores", "Daily Playbook", "Data Quality", "Settings", "History", "Buy Zones"]
COMPONENT_FORBIDDEN = ["US Market", "US Tech", "Taiwan", "Crypto", "Gold", "Macro", "Volatility"]
HEADER_FORBIDDEN = ["symbol", "ticker", "latest_price", "action_label", "risk_label", "freshness_status", "provider", "confidence", "target_weight", "current_weight", "drift", "buy_zone_1", "buy_zone_2", "buy_zone_3", "No."]
CELL_FORBIDDEN = COMPONENT_FORBIDDEN + [
    "Potential Buy Zone - verify quote",
    "Extended / Do not chase",
    "Healthy trend / Hold",
    "Pullback watch",
    "Broken trend / Avoid",
    "Connected",
    "Not configured",
    "Delayed / uncertain",
]
STREAMLIT_VISIBLE_CALLS = {"title", "header", "subheader", "markdown", "metric", "button", "tabs", "expander"}


def main() -> int:
    set_lang(LANG_ZH)
    findings = []
    required_terms = _load_required_terms()
    zh_values = set(TRANSLATIONS[LANG_ZH].values())

    for english, chinese in required_terms.items():
        if not chinese:
            findings.append(("required_terms", english, "Missing required Traditional Chinese translation."))
        if english in {"US Market", "US Tech", "Taiwan", "Taiwan Market", "Crypto", "Gold", "Macro", "Volatility"} and translate_term(english) == english:
            findings.append(("required_terms", english, "Missing term mapping in translate_term()."))
        if english in NAV_FORBIDDEN and chinese not in zh_values:
            findings.append(("navigation_terms", english, "Navigation translation not present in zh mapping."))

    nav_output = "\n".join(t(key) for key in ["home", "macro_dashboard", "portfolio", "watchlist", "asset_scores", "daily_playbook", "data_quality", "settings", "history", "buy_zones"])
    _check_forbidden(findings, "navigation_output", nav_output, NAV_FORBIDDEN)

    component_output = "\n".join(translate_term(term) for term in COMPONENT_FORBIDDEN)
    _check_forbidden(findings, "component_output", component_output, COMPONENT_FORBIDDEN)

    sample = pd.DataFrame(
        [
            {
                "symbol": "SPY",
                "ticker": "2330.TW",
                "latest_price": 100,
                "action_label": "Potential Buy Zone - verify quote",
                "risk_label": "High",
                "freshness_status": "Delayed / uncertain",
                "provider": "yfinance",
                "confidence": 70,
                "target_weight": 40,
                "current_weight": 35,
                "drift": -5,
                "buy_zone_1": 95,
                "buy_zone_2": 90,
                "buy_zone_3": 85,
                "category": "US Market",
                "status": "Connected",
                "warning": "Verify broker quote before actual trading.",
            }
        ]
    )
    translated = translate_dataframe(sample, LANG_ZH)
    for column in translated.columns:
        if str(column) in HEADER_FORBIDDEN:
            findings.append(("table_headers", str(column), "Forbidden untranslated table header."))
    _check_forbidden(findings, "table_cells", translated.to_string(index=False), CELL_FORBIDDEN)

    for path in [ROOT_DIR / "app.py", *sorted((ROOT_DIR / "pages").glob("*.py"))]:
        _scan_source(path, findings)

    if findings:
        print("FAIL i18n hard gate")
        for location, term, suggestion in findings:
            print(f"- {location}: {term}")
            print(f"  suggested translation key: {suggestion}")
        return 1

    print("PASS i18n hard gate")
    return 0


def _load_required_terms() -> dict[str, str]:
    terms = {}
    for line in REQUIRED_TERMS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.strip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        terms[key.strip()] = value.strip()
    return terms


def _check_forbidden(findings: list, location: str, output: str, forbidden_terms: list[str]) -> None:
    for term in forbidden_terms:
        if term in output:
            findings.append((location, term, f"Translate or map '{term}' in zh output."))


def _scan_source(path: Path, findings: list) -> None:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr not in STREAMLIT_VISIBLE_CALLS:
            continue
        for child in ast.walk(node):
            if isinstance(child, ast.Constant) and isinstance(child.value, str):
                value = child.value
                for term in NAV_FORBIDDEN + COMPONENT_FORBIDDEN:
                    if term == value:
                        findings.append((f"{path.relative_to(ROOT_DIR)}:{child.lineno}", term, f"Use t(...) or translate_term(...) for '{term}'."))


if __name__ == "__main__":
    raise SystemExit(main())
