
from modules.shared.ui_shell import configure_page, render_page_shell
from modules.buy_zones import render


configure_page("Buy Zones")
lang = render_page_shell()
render(lang)
