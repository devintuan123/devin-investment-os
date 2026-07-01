# I18N Audit Report

## Pages audited

- `app.py`
- `pages/1_Macro_Dashboard.py`
- `pages/2_Portfolio.py`
- `pages/3_Watchlist.py`
- `pages/4_Settings.py`
- `pages/5_Asset_Scores.py`
- `pages/6_Daily_Playbook.py`
- `pages/7_History.py`
- `pages/8_TradingView_Alerts.py`
- `pages/9_Data_Quality.py`
- `pages/10_Buy_Zones.py`

## Files changed

- `utils/i18n.py`
- `utils/ui.py`
- all visible Streamlit page files listed above
- `scripts/audit_i18n.py`
- `scripts/ui_text_snapshot.py`

## Remaining known exceptions

The audit intentionally allows:

- ticker symbols
- provider names such as yfinance, Binance, FRED, Telegram, TWSE
- URLs, file paths, and Streamlit page paths
- code identifiers and dataframe column keys
- compact chart/table labels produced from data

## Translation rule

Every new visible UI string must go through `utils/i18n.py`.

Use:

- `t("key")` for labels, headings, buttons, captions, and warnings
- `translate_action_label(label)` for action labels
- `translate_risk_label(label)` for risk labels
- `translate_regime(label)` for market regime labels

## How to add new translation keys

1. Add the English key/value to `TRANSLATIONS[LANG_EN]`.
2. Add the Traditional Chinese key/value to `TRANSLATIONS[LANG_ZH]`.
3. Use `t("key")` in page code.
4. Run `python scripts/audit_i18n.py`.
5. Run `python scripts/ui_text_snapshot.py`.
