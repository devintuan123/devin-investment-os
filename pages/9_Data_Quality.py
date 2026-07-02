
from modules.shared.ui_shell import configure_page, render_page_shell
from modules.data_quality import render


configure_page("Data Quality")
lang = render_page_shell()
render(lang)
