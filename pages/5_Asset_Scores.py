
from modules.shared.ui_shell import configure_page, render_page_shell
from modules.asset_scores import render


configure_page("Asset Scores")
lang = render_page_shell()
render(lang)
