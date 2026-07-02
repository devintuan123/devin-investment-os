
from modules.shared.ui_shell import configure_page, render_page_shell
from modules.watchlist import render


configure_page("Watchlist")
lang = render_page_shell()
render(lang)
