
from modules.shared.ui_shell import configure_page, render_page_shell
from modules.history import render


configure_page("History")
lang = render_page_shell()
render(lang)
