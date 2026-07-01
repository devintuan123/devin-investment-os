# I18N TODO

All currently visible Streamlit pages use the shared language switch from `utils/ui.py`.

Future work:

- Any new page must call `render_sidebar_language_switch()`.
- Any new visible label must use `t("key")`.
- Any new action label must be mapped in `ACTION_LABEL_KEYS`.
- Any new risk label must be mapped in `RISK_LABEL_KEYS`.

Allowed untranslated items:

- ticker symbols
- provider names
- API names
- URLs
- file paths
- technical dataframe column keys when they are not visible labels
