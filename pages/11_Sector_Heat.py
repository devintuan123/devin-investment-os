
from modules.shared.ui_shell import configure_page, render_page_shell
from modules.sector_heat import render


configure_page("Sector Heat / Capital Rotation")
lang = render_page_shell()
render(lang)
