from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import pandas as pd

from utils.i18n import LANG_EN, LANG_ZH, set_lang, t, translate_action_label, translate_regime, translate_term
from utils.market_regime import calculate_market_regime
from utils.watchlist_scoring import score_watchlist
from utils.portfolio_engine import calculate_position_values, load_portfolio, portfolio_health_score
from utils.buy_zone_engine import score_buy_zones
from utils.sector_heat_engine import calculate_theme_heat_score
from utils.provider_status import active_provider_rows, future_disabled_provider_rows
from utils.snapshot_store import load_latest_snapshot

SNAPSHOTS = {LANG_ZH: ROOT_DIR / "reports" / "ui_snapshot_zh.md", LANG_EN: ROOT_DIR / "reports" / "ui_snapshot_en.md"}
BAD_ZH_PATTERNS = ["嚙", "�", "癟", "疆", "矇", "疇", "瓊", "癡", "璽", "", "", "", "", "", ""]
RAW_UNICODE_RE = re.compile(r"\\u[0-9a-fA-F]{4}")


def main() -> int:
    failures = []
    for lang, path in SNAPSHOTS.items():
        set_lang(lang)
        content = build_snapshot(lang)
        path.parent.mkdir(exist_ok=True)
        path.write_text(content, encoding="utf-8")
        if not content.strip():
            failures.append(f"{path.name} is empty")
        if lang == LANG_ZH:
            for pattern in BAD_ZH_PATTERNS:
                if pattern in content:
                    failures.append(f"{path.name} contains mojibake pattern {pattern!r}")
            if RAW_UNICODE_RE.search(content):
                failures.append(f"{path.name} contains raw unicode escape")
            if "??" in content:
                failures.append(f"{path.name} contains repeated question marks")
    for path in SNAPSHOTS.values():
        print(path.read_text(encoding="utf-8")[:4000])
    if failures:
        print("UI visual/text snapshot failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("UI visual/text snapshot passed.")
    return 0


def build_snapshot(lang: str) -> str:
    regime = calculate_market_regime()
    watchlist = pd.DataFrame(score_watchlist()).head(3)
    positions = calculate_position_values(load_portfolio()).head(3)
    health = portfolio_health_score(load_portfolio())
    buy_zones = pd.DataFrame(score_buy_zones()).head(3)
    sector_heat = calculate_theme_heat_score().head(3)
    latest_snapshot = load_latest_snapshot()
    lines = ["# Devin Investment OS UI Snapshot", "", f"Generated: {datetime.now(timezone.utc).isoformat()}", f"Language: {lang}", ""]
    page(lines, t("home"), [t("market_score"), t("market_regime"), t("today_action"), t("data_confidence"), t("market_components")], [f"{t('market_score')}: {regime['market_score']}/100", f"{t('market_regime')}: {translate_regime(regime['market_regime'])}", f"{t('portfolio_health')}: {health['score']}/100"], pd.DataFrame(regime.get("score_diagnostics", [])).head(3))
    page(lines, t("macro_dashboard"), [t("score_diagnostics"), t("raw_data"), t("source"), t("latest_timestamp")], [f"{translate_term(name)} {score}/100" for name, score in regime.get("components", {}).items()], pd.DataFrame(regime.get("score_diagnostics", [])).head(3))
    page(lines, t("portfolio"), [t("portfolio_health"), t("positions"), t("target_allocation")], [str(health)], positions)
    page(lines, t("watchlist"), [t("ticker"), t("latest_price"), t("trend_score"), t("risk_label")], [], watchlist)
    page(lines, t("buy_zones"), [t("buy_zone_1"), t("buy_zone_2"), t("buy_zone_3"), t("strategy_action")], [], buy_zones)
    page(lines, t("sector_heat_page"), [t("heat_score"), t("rotation_score"), t("proxy_heat_warning")], [], sector_heat)
    page(lines, t("daily_playbook"), [t("market_regime_summary"), t("top_positive_drivers"), t("top_negative_drivers"), t("broker_warning")], regime.get("warnings", [])[:4], pd.DataFrame(regime.get("provider_quality", [])).head(4))
    page(lines, t("history"), [t("latest_snapshot"), t("snapshot_trend")], [str(latest_snapshot.get("timestamp", t("no_snapshots"))) if latest_snapshot else t("no_snapshots")], pd.DataFrame([latest_snapshot]) if latest_snapshot else pd.DataFrame())
    page(lines, t("data_quality"), [t("active_providers"), t("disabled_providers")], [], pd.DataFrame(active_provider_rows() + future_disabled_provider_rows()))
    page(lines, t("settings"), [t("api_configuration"), t("safety_status"), t("security_notes")], [t("read_only_notice")], pd.DataFrame(active_provider_rows()))
    page(lines, t("asset_scores"), [t("decision_scoring"), t("score"), t("warning")], [t("broker_warning")], pd.DataFrame(regime.get("score_diagnostics", [])).head(3))
    page(lines, t("tv_alerts"), [t("tv_alerts"), t("alerts_caption")], [t("read_only_notice")], pd.DataFrame())
    return "\n".join(lines) + "\n"


def page(lines: list[str], title: str, headers: list[str], metrics: list[str], table: pd.DataFrame) -> None:
    lines.append(f"## {title}")
    lines.append("Headers: " + ", ".join(str(item) for item in headers if item))
    if metrics:
        lines.append("Metrics / warnings:")
        lines.extend(f"- {item}" for item in metrics if item)
    if table is not None and not table.empty:
        lines.append("Table columns: " + ", ".join(str(column) for column in table.columns))
        lines.append(table.head(3).to_csv(index=False))
    else:
        lines.append("Table columns: none")
    lines.append("")


if __name__ == "__main__":
    raise SystemExit(main())
