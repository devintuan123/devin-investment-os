from __future__ import annotations

import importlib
import json
from pathlib import Path
import sys
import traceback

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
REPORT_DIR = ROOT_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

from scripts.send_daily_report import build_daily_report
from utils.i18n import LANG_EN, LANG_ZH, set_lang, t, translate_term, translate_text
from utils.indicators import market_indicators
from utils.interactive_table import _valid_dataframe_height
from utils.fred_provider import get_macro_series_snapshot
from utils.market_data import get_market_proxy_snapshot
from utils.market_regime import calculate_market_regime
from utils.portfolio_engine import calculate_position_values
from utils.portfolio_store import load_portfolio, load_transactions
from utils.table_i18n import translate_dataframe


PAGES = {
    "Home": "modules.home",
    "Macro Dashboard": "modules.macro",
    "Portfolio": "modules.portfolio",
    "Watchlist": "modules.watchlist",
    "Asset Scores": "modules.asset_scores",
    "Daily Playbook": "modules.daily_playbook",
    "Data Quality": "modules.data_quality",
    "Settings": "modules.settings",
    "History": "modules.history",
    "Buy Zones": "modules.buy_zones",
    "Sector Heat / Capital Rotation": "modules.sector_heat",
}
NAV_KEYS = ["home", "macro_dashboard", "portfolio", "watchlist", "asset_scores", "daily_playbook", "data_quality", "settings", "history", "buy_zones", "sector_heat_page"]
FORBIDDEN_ZH = [
    "Liquidity",
    "Sentiment",
    "Breadth",
    "Defensive",
    "Mixed",
    "Constructive",
    "Risk controls should take priority.",
    "Signals are mixed; confirmation matters.",
    "Trend and momentum are supportive.",
    "led 5D momentum",
    "lagged",
    "current_price",
    "buy_zone_low",
    "buy_zone_high",
    "trim_zone",
    "stop_level",
    "priority",
    "Potential Buy Zone - verify quote",
    "Extended / Do not chase",
    "Healthy trend / Hold",
    "Pullback watch",
    "Broken trend / Avoid",
    "Connected",
    "Not configured",
    "Delayed / uncertain",
]
RAW_INDEX_COLUMNS = {"No.", "No", "no", "index", "Index", "#", "Unnamed: 0"}


def main() -> int:
    issues: list[dict] = []
    checks: list[str] = []

    _check_pages_import(issues, checks)
    _check_navigation(issues, checks)
    _check_home_components(issues, checks)
    _check_tables(issues, checks)
    _check_macro_data_sections(issues, checks)
    _check_macro_runtime_text(issues, checks)
    _check_daily_and_telegram_text(issues, checks)
    _check_portfolio_runtime(issues, checks)
    _check_height_guard(issues, checks)

    critical = [issue for issue in issues if issue["severity"] == "critical"]
    _write_reports(checks, issues)
    if critical:
        print(f"FAIL full runtime audit: {len(critical)} critical issue(s)")
        for issue in critical:
            print(f"- {issue['area']}: {issue['message']}")
        return 1
    print("PASS full runtime audit")
    return 0


def _check_pages_import(issues: list[dict], checks: list[str]) -> None:
    for label, module_name in PAGES.items():
        for lang in (LANG_ZH, LANG_EN):
            set_lang(lang)
            try:
                module = importlib.import_module(module_name)
                if not hasattr(module, "render"):
                    _issue(issues, "critical", label, f"{module_name} lacks render(lang)")
                checks.append(f"{label} import/render symbol ok in {lang}")
            except Exception:
                _issue(issues, "critical", label, traceback.format_exc())


def _check_navigation(issues: list[dict], checks: list[str]) -> None:
    set_lang(LANG_ZH)
    zh_nav = "\n".join(t(key) for key in NAV_KEYS)
    _check_forbidden(issues, "zh navigation", zh_nav)
    checks.append("zh navigation labels generated")
    set_lang(LANG_EN)
    en_nav = "\n".join(t(key) for key in NAV_KEYS)
    for expected in ["Home", "Macro Dashboard", "Portfolio", "Watchlist", "Sector Heat / Capital Rotation"]:
        if expected not in en_nav:
            _issue(issues, "critical", "en navigation", f"Missing {expected}")
    checks.append("en navigation labels generated")


def _check_home_components(issues: list[dict], checks: list[str]) -> None:
    set_lang(LANG_ZH)
    regime = calculate_market_regime()
    required = ["US Market", "US Tech", "Taiwan", "Crypto", "Gold", "Macro", "Volatility", "Liquidity", "Sentiment", "Breadth"]
    missing = [name for name in required if name not in regime["components"]]
    if missing:
        _issue(issues, "critical", "home components", "Missing components: " + ", ".join(missing))
    translated = "\n".join(translate_term(name) for name in regime["components"])
    _check_forbidden(issues, "home components zh", translated)
    checks.append("home component list includes required market buckets")


def _check_tables(issues: list[dict], checks: list[str]) -> None:
    sample = pd.DataFrame(
        [
            {
                "symbol": "SPY",
                "name": "SPDR S&P 500",
                "category": "US Market",
                "market": "US",
                "value": 100,
                "position_value": 100,
                "current_weight": 10,
                "target_weight": 15,
                "drift": -5,
                "target_drift": -5,
                "current_drift": -4,
                "allocation_drift": -3,
                "drift_abs": 5,
                "drift_pct": -5,
                "current_price": 100,
                "buy_zone_low": 90,
                "buy_zone_high": 95,
                "trim_zone": 120,
                "stop_level": 80,
                "priority": "High",
                "action_label": "Potential Buy Zone - verify quote",
                "risk_label": "High",
                "freshness_status": "Delayed / uncertain",
                "provider": "yfinance",
                "No.": 1,
            }
        ]
    )
    set_lang(LANG_ZH)
    translated = translate_dataframe(sample.drop(columns=["No."]), LANG_ZH)
    if len(set(map(str, translated.columns))) != len(translated.columns):
        _issue(issues, "critical", "table columns", "Translated columns are not unique.")
    if any(column in RAW_INDEX_COLUMNS for column in translated.columns):
        _issue(issues, "critical", "table columns", "Useless index/No. column visible.")
    _check_forbidden(issues, "translated sample dataframe", translated.to_string(index=False))
    checks.append("zh translated sample dataframe has unique translated columns")
    set_lang(LANG_EN)
    translated_en = translate_dataframe(sample.drop(columns=["No."]), LANG_EN)
    if len(set(map(str, translated_en.columns))) != len(translated_en.columns):
        _issue(issues, "critical", "table columns en", "Translated EN columns are not unique.")
    checks.append("en translated sample dataframe has unique translated columns")


def _check_macro_runtime_text(issues: list[dict], checks: list[str]) -> None:
    set_lang(LANG_ZH)
    lines = []
    for section, payload in market_indicators().items():
        lines.extend([translate_term(section), translate_term(payload["status"]), translate_text(payload["explanation"]), translate_text(payload["what_changed"])])
    output = "\n".join(lines)
    _check_forbidden(issues, "macro runtime zh", output)
    checks.append("macro indicator runtime text translated in zh")


def _check_macro_data_sections(issues: list[dict], checks: list[str]) -> None:
    source = (ROOT_DIR / "modules" / "macro" / "__init__.py").read_text(encoding="utf-8")
    for label, token in {
        "FRED Raw Data": "fred_raw_data",
        "Market Proxy Data": "market_proxy_data",
        "Score Diagnostics": "score_diagnostics",
        "Missing Data Warnings": "macro_missing_data_warning",
    }.items():
        if token not in source:
            _issue(issues, "critical", "macro data sections", f"Missing {label} section")
    fred = get_macro_series_snapshot()
    proxies = get_market_proxy_snapshot()
    if fred.empty:
        _issue(issues, "critical", "macro data sections", "FRED diagnostics are empty")
    if proxies.empty:
        _issue(issues, "critical", "macro data sections", "Market proxy diagnostics are empty")
    valid_fred = bool(not fred.empty and (~fred["missing"].fillna(False).astype(bool)).any())
    visible_fred_warning = "macro_missing_data_warning" in source
    valid_proxy = bool(not proxies.empty and (~proxies["missing"].fillna(False).astype(bool)).any())
    visible_proxy_warning = "macro_missing_data_warning" in source
    if not (valid_fred or visible_fred_warning):
        _issue(issues, "critical", "macro data sections", "FRED missing without visible warning")
    if not (valid_proxy or visible_proxy_warning):
        _issue(issues, "critical", "macro data sections", "yfinance missing without visible warning")
    regime = calculate_market_regime()
    fallback_rows = [row for row in regime.get("score_diagnostics", []) if row.get("fallback_used")]
    if fallback_rows and not any("fallback" in str(warning).lower() for warning in regime.get("warnings", [])):
        _issue(issues, "critical", "macro data sections", "Fallback scores are not surfaced in top-level warnings")
    if fallback_rows and regime.get("confidence_score", 100) >= 75:
        _issue(issues, "critical", "macro data sections", "Fallback scores still show high confidence")
    checks.append("macro raw data sections and fallback visibility audited")


def _check_daily_and_telegram_text(issues: list[dict], checks: list[str]) -> None:
    set_lang(LANG_ZH)
    report = build_daily_report(LANG_ZH)
    _check_forbidden(issues, "telegram zh", report)
    checks.append("telegram zh dry-run text audited")
    set_lang(LANG_EN)
    report_en = build_daily_report(LANG_EN)
    if "Sector Heat / Capital Rotation" not in report_en:
        _issue(issues, "critical", "telegram en", "Sector heat missing from EN report")
    checks.append("telegram en dry-run text audited")


def _check_portfolio_runtime(issues: list[dict], checks: list[str]) -> None:
    try:
        portfolio = load_portfolio()
        positions = calculate_position_values(portfolio)
        load_transactions()
        translate_dataframe(positions, LANG_ZH)
        checks.append("portfolio load/value/translate ok")
    except Exception:
        _issue(issues, "critical", "portfolio runtime", traceback.format_exc())


def _check_height_guard(issues: list[dict], checks: list[str]) -> None:
    if _valid_dataframe_height(None) is not None:
        _issue(issues, "critical", "table height", "height=None is not filtered")
    if _valid_dataframe_height(400) != 400:
        _issue(issues, "critical", "table height", "positive int height rejected")
    if _valid_dataframe_height("content") != "content":
        _issue(issues, "critical", "table height", "content height rejected")
    checks.append("dataframe height guard ok")


def _check_forbidden(issues: list[dict], area: str, text: str) -> None:
    for term in FORBIDDEN_ZH:
        if term in text:
            _issue(issues, "critical", area, f"Forbidden zh-visible English term: {term}")


def _issue(issues: list[dict], severity: str, area: str, message: str) -> None:
    issues.append({"severity": severity, "area": area, "message": message})


def _write_reports(checks: list[str], issues: list[dict]) -> None:
    (REPORT_DIR / "full_runtime_audit_issues.json").write_text(json.dumps(issues, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Full Runtime Audit", "", "## Checks", *[f"- {check}" for check in checks], "", "## Issues"]
    if issues:
        lines.extend([f"- **{issue['severity']}** `{issue['area']}`: {issue['message']}" for issue in issues])
    else:
        lines.append("- None")
    (REPORT_DIR / "full_runtime_audit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
