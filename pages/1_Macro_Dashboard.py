import streamlit as st

from modules.shared.ui_shell import render_page_shell
from modules.macro import render


st.set_page_config(page_title="Macro Dashboard", page_icon="DI", layout="wide")
lang = render_page_shell()
render(lang)
