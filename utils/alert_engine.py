from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from utils.buy_zone_engine import score_buy_zones
from utils.data import ROOT_DIR
from utils.i18n import LANG_EN, LANG_ZH, set_lang, t, translate_action_label, translate_regime
from utils.market_data import safe_fetch_with_fallback
from utils.market_regime import calculate_market_regime
from utils.portfolio_engine import calculate_position_values, load_portfolio
from utils.sector_heat_engine import calculate_theme_heat_score
from utils.telegram import send_telegram_message


ALERT_RULES_PATH = ROOT_DIR / "data" / "alert_rules.yaml"
ALERT_STATE_PATH = ROOT_DIR / "data" / "alert_state.json"

DEFAULT_ALERT_RULES = {
    "alerts": {
        "market_score_below": {"enabled": True, "threshold": 40},
        "market_score_above": {"enabled": True, "threshold": 75},
        "regime_changed": {"enabled": True},
        "vix_above": {"enabled": True, "threshold": 25},
        "btc_breakout_or_breakdown": {"enabled": True},
        "buy_zone_entered": {"enabled": True},
        "portfolio_drift_exceeded": {"enabled": True, "threshold": 8},
        "sector_heat_spike": {"enabled": True, "threshold": 85},
        "taiwan_quote_stale_warning": {"enabled": True},
    },
    "delivery": {"telegram_enabled": True, "suppress_duplicate_hours": 12, "decision_support_only": True},
}


def load_alert_rules() -> dict:
    rules = DEFAULT_ALERT_RULES.copy()
    if not ALERT_RULES_PATH.exists():
        return rules
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(ALERT_RULES_PATH.read_text(encoding="utf-8")) or {}
        if isinstance(loaded, dict):
            rules.update(loaded)
    except Exception:
        pass
    return rules


def evaluate_alerts() -> list[dict]:
    rules = load_alert_rules()
    alert_rules = rules.get("alerts", {})
    regime = calculate_market_regime()
    alerts: list[dict] = []
    score = float(regime.get("market_score", 0) or 0)
    if _enabled(alert_rules, "market_score_below") and score <= _threshold(alert_rules, "market_score_below", 40):
        alerts.append(_alert("market_score_below", "Market score below threshold", score))
    if _enabled(alert_rules, "market_score_above") and score >= _threshold(alert_rules, "market_score_above", 75):
        alerts.append(_alert("market_score_above", "Market score above threshold", score))
    if _enabled(alert_rules, "regime_changed") and _previous_regime() not in {"", regime.get("market_regime")}:
        alerts.append(_alert("regime_changed", f"Regime changed to {regime.get('market_regime')}", regime.get("market_regime")))
    if _enabled(alert_rules, "vix_above"):
        vix = safe_fetch_with_fallback("^VIX", 0).get("price", 0)
        if float(vix or 0) >= _threshold(alert_rules, "vix_above", 25):
            alerts.append(_alert("vix_above", "VIX above threshold", vix))
    if _enabled(alert_rules, "btc_breakout_or_breakdown"):
        btc = safe_fetch_with_fallback("BTC-USD", 0).get("price", 0)
        if float(btc or 0) > 125000 or float(btc or 0) < 80000:
            alerts.append(_alert("btc_breakout_or_breakdown", "BTC breakout or breakdown reference", btc))
    if _enabled(alert_rules, "buy_zone_entered"):
        for row in score_buy_zones():
            if row.get("strategy_action") in {"Potential buy zone", "Consider gradual allocation", "DCA only"}:
                alerts.append(_alert("buy_zone_entered", f"{row['ticker']} entered {row['strategy_action']}", row.get("latest_price")))
                break
    if _enabled(alert_rules, "portfolio_drift_exceeded"):
        positions = calculate_position_values(load_portfolio())
        drift = float(positions["drift"].abs().max()) if not positions.empty else 0
        if drift >= _threshold(alert_rules, "portfolio_drift_exceeded", 8):
            alerts.append(_alert("portfolio_drift_exceeded", "Portfolio drift exceeded threshold", round(drift, 2)))
    if _enabled(alert_rules, "sector_heat_spike"):
        heat = calculate_theme_heat_score()
        if not heat.empty and float(heat["heat_score"].max()) >= _threshold(alert_rules, "sector_heat_spike", 85):
            row = heat.iloc[0]
            alert = _alert("sector_heat_spike", f"{row['theme']} heat spike", int(row["heat_score"]))
            alert["theme_zh"] = row.get("theme_zh", row["theme"])
            alerts.append(alert)
    if _enabled(alert_rules, "taiwan_quote_stale_warning"):
        alerts.append(_alert("taiwan_quote_stale_warning", "Taiwan yfinance quotes are delayed reference only", "verify broker quote"))
    return suppress_duplicate_alerts(alerts)


def format_alerts(lang: str = LANG_ZH, alerts: list[dict] | None = None) -> str:
    set_lang(lang)
    alerts = evaluate_alerts() if alerts is None else alerts
    if not alerts:
        return f"{t('active_alerts')}: {t('no_alerts')}"
    lines = [f"{t('active_alerts')} ({len(alerts)})"]
    for alert in alerts:
        message = alert["message"]
        value = alert.get("value")
        if lang == LANG_ZH:
            message = _translate_alert_message(message)
            if alert.get("type") == "sector_heat_spike":
                message = f"{alert.get('theme_zh', message)} \u71b1\u5ea6\u5347\u9ad8"
            if str(value) == "verify broker quote":
                value = t("verify_broker_quote")
        lines.append(f"- {message}: {value}")
    lines.append(t("read_only_notice"))
    lines.append(t("broker_warning"))
    return "\n".join(lines)


def send_alerts_if_needed(lang: str = LANG_ZH, dry_run: bool = True) -> bool:
    alerts = evaluate_alerts()
    message = format_alerts(lang, alerts)
    if dry_run:
        print(message)
        _store_state(alerts, sent=False)
        return True
    sent = send_telegram_message(message)
    if sent:
        _store_state(alerts, sent=True)
    return sent


def suppress_duplicate_alerts(alerts: list[dict]) -> list[dict]:
    state = _load_state()
    sent = state.get("sent", {})
    cutoff = datetime.now(timezone.utc) - timedelta(hours=int(load_alert_rules().get("delivery", {}).get("suppress_duplicate_hours", 12)))
    fresh = []
    for alert in alerts:
        previous = sent.get(alert["dedupe_key"])
        if not previous or datetime.fromisoformat(previous) < cutoff:
            fresh.append(alert)
    return fresh


def _store_state(alerts: list[dict], sent: bool) -> None:
    state = _load_state()
    state["last_regime"] = calculate_market_regime().get("market_regime")
    if sent:
        state.setdefault("sent", {})
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for alert in alerts:
            state["sent"][alert["dedupe_key"]] = now
    ALERT_STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _load_state() -> dict:
    if not ALERT_STATE_PATH.exists():
        return {"last_regime": "", "sent": {}}
    try:
        return json.loads(ALERT_STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"last_regime": "", "sent": {}}


def _previous_regime() -> str:
    return str(_load_state().get("last_regime", ""))


def _enabled(rules: dict, name: str) -> bool:
    return bool(rules.get(name, {}).get("enabled", False))


def _threshold(rules: dict, name: str, default: int) -> float:
    return float(rules.get(name, {}).get("threshold", default))


def _alert(alert_type: str, message: str, value) -> dict:
    return {
        "type": alert_type,
        "message": message,
        "value": value,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "dedupe_key": f"{alert_type}:{message}",
    }


def _translate_alert_message(message: str) -> str:
    replacements = {
        "Market score below threshold": "市場分數低於門檻",
        "Market score above threshold": "市場分數高於門檻",
        "VIX above threshold": "VIX 高於門檻",
        "BTC breakout or breakdown reference": "BTC 突破或跌破參考",
        "Portfolio drift exceeded threshold": "投資組合偏離超過門檻",
        "Taiwan yfinance quotes are delayed reference only": "台股 yfinance 報價僅為延遲參考",
    }
    if message.startswith("Regime changed to "):
        return f"市場狀態轉為 {translate_regime(message.replace('Regime changed to ', ''))}"
    if " entered " in message:
        symbol, action = message.split(" entered ", 1)
        return f"{symbol} 進入 {translate_action_label(action)}"
    if message.endswith(" heat spike"):
        return message.replace(" heat spike", " 熱度升高")
    return replacements.get(message, message)
