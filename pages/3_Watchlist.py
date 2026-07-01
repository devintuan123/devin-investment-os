import streamlit as st

from modules.shared.ui_shell import render_page_shell
from modules.watchlist import render


st.set_page_config(page_title="Watchlist", page_icon="DI", layout="wide")
lang = render_page_shell()
render(lang)
