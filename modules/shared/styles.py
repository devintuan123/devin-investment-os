from __future__ import annotations

import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
            html, body, [class*="css"], .stApp {
                font-family: "Noto Sans TC", "Microsoft JhengHei", "PingFang TC", "Arial Unicode MS", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }
            .block-container {
                max-width: 1440px;
                padding-top: 1.25rem;
                padding-bottom: 2rem;
            }
            [data-testid="stMetric"] {
                border: 1px solid rgba(148, 163, 184, 0.35);
                border-radius: 0.75rem;
                padding: 0.85rem;
                background: rgba(248, 250, 252, 0.72);
                overflow-wrap: anywhere;
            }
            [data-testid="stMetricLabel"], [data-testid="stMetricValue"], p, li, span, div {
                overflow-wrap: anywhere;
                word-break: break-word;
            }
            div[data-testid="stDataFrame"] {
                width: 100%;
                overflow-x: auto;
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.35rem;
                flex-wrap: wrap;
            }
            @media (max-width: 768px) {
                .block-container {
                    padding-left: 0.8rem;
                    padding-right: 0.8rem;
                }
                h1 {font-size: 1.65rem;}
                h2 {font-size: 1.25rem;}
                h3 {font-size: 1.05rem;}
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
