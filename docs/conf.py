import sys
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DOCS_DIR.parent

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DOCS_DIR))

project = "GitCode API"
author = "Hugo Huang"
copyright = "2026, GitCode official team (REST API docs); Hugo Huang (SDK docs)"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

autosummary_generate = True
autodoc_member_order = "bysource"
autodoc_typehints = "signature"
autoclass_content = "both"
add_module_names = False

autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "_downloads"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_title = f"{project} documentation"

html_theme_options = {
    "style_external_links": True,
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "prev_next_buttons_location": "both",
    "style_nav_header_background": "#143d52",
}

pygments_style = "friendly"

language = "en"

nitpicky = False
