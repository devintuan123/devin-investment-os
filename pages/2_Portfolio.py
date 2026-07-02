
from modules.shared.ui_shell import configure_page, render_page_shell
from modules.portfolio import render


configure_page("Portfolio")
lang = render_page_shell()
render(lang)
