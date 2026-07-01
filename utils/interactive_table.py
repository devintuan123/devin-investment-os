from __future__ import annotations

from typing import Optional

import pandas as pd
import streamlit as st

from utils.i18n import LANG_ZH, t
from utils.table_i18n import translate_dataframe


NO_COLUMNS = {"No.", "No", "no", "index", "Index", "#", t("no_column")}
FILTER_HINTS = (
    "category",
    "market",
    "action",
    "risk",
    "provider",
    "freshness",
    "status",
    "分類",
    "市場",
    "行動",
    "風險",
    "資料來源",
    "新鮮度",
    "狀態",
)


def render_interactive_table(
    df,
    table_key: str,
    lang: str,
    searchable: bool = True,
    filterable: bool = True,
    sortable: bool = True,
    hide_index: bool = True,
    remove_no_column: bool = True,
    default_sort: Optional[str] = None,
    height: Optional[int] = None,
):
    source = _as_dataframe(df)
    if remove_no_column:
        source = _drop_no_columns(source)

    translated = translate_dataframe(source, lang)
    if translated is None or translated.empty:
        st.info(t("no_data"))
        return translated

    view = translated.copy()
    original_count = len(view)

    with st.container():
        if searchable:
            query = st.text_input(t("search"), key=f"{table_key}_search", placeholder=t("search"))
            if query:
                string_columns = view.select_dtypes(include=["object", "string"]).columns
                if len(string_columns) > 0:
                    mask = view[string_columns].astype(str).apply(lambda column: column.str.contains(query, case=False, na=False))
                    view = view[mask.any(axis=1)]

        if filterable:
            filter_columns = _filter_columns(view)
            if filter_columns:
                with st.expander(t("filter"), expanded=False):
                    for column in filter_columns:
                        values = sorted([str(value) for value in view[column].dropna().unique() if str(value)])
                        if not values or len(values) > 25:
                            continue
                        selected = st.multiselect(str(column), values, key=f"{table_key}_filter_{column}")
                        if selected:
                            view = view[view[column].astype(str).isin(selected)]
                    if st.button(t("reset_filters"), key=f"{table_key}_reset", use_container_width=True):
                        _clear_table_state(table_key)
                        st.rerun()

        if sortable and not view.empty:
            sort_columns = list(view.columns)
            sort_index = _default_sort_index(sort_columns, default_sort)
            sort_cols = st.columns([2, 1])
            sort_column = sort_cols[0].selectbox(t("sort_column"), sort_columns, index=sort_index, key=f"{table_key}_sort_column")
            direction = sort_cols[1].selectbox(t("sort"), [t("ascending"), t("descending")], key=f"{table_key}_sort_direction")
            view = view.sort_values(sort_column, ascending=direction == t("ascending"), na_position="last")

        st.caption(_row_count_label(lang, len(view), original_count))
        st.dataframe(view, use_container_width=True, hide_index=hide_index, height=height)
        return view


def _as_dataframe(df) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame()
    if isinstance(df, pd.DataFrame):
        return df.copy()
    return pd.DataFrame(df)


def _drop_no_columns(df: pd.DataFrame) -> pd.DataFrame:
    columns = [column for column in df.columns if str(column) not in NO_COLUMNS]
    return df[columns].copy()


def _filter_columns(df: pd.DataFrame) -> list:
    columns = []
    for column in df.columns:
        normalized = str(column).lower()
        if any(hint in normalized for hint in FILTER_HINTS) and df[column].nunique(dropna=True) <= 25:
            columns.append(column)
    return columns


def _default_sort_index(columns: list, default_sort: Optional[str]) -> int:
    if default_sort in columns:
        return columns.index(default_sort)
    return 0


def _clear_table_state(table_key: str) -> None:
    for key in list(st.session_state.keys()):
        if str(key).startswith(f"{table_key}_filter_") or str(key) in {f"{table_key}_search", f"{table_key}_sort_column", f"{table_key}_sort_direction"}:
            del st.session_state[key]


def _row_count_label(lang: str, shown: int, total: int) -> str:
    if lang == LANG_ZH:
        return t("showing_rows").format(shown=shown, total=total)
    return t("showing_rows").format(shown=shown, total=total)
