import streamlit as st

from modules.shared.ui_shell import render_page_shell
from modules.sector_heat import render


st.set_page_config(page_title="Sector Heat / Capital Rotation", page_icon="DI", layout="wide")
lang = render_page_shell()
render(lang)
