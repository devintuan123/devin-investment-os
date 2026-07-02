
from modules.shared.ui_shell import configure_page, render_page_shell
from modules.macro import render


configure_page("Macro Dashboard")
lang = render_page_shell()
render(lang)
