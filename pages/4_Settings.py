
from modules.shared.ui_shell import configure_page, render_page_shell
from modules.settings import render


configure_page("Settings")
lang = render_page_shell()
render(lang)
