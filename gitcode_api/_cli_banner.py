"""ASCII art banner for command-line interface."""

import sys
from functools import lru_cache
from importlib.metadata import metadata
from typing import List, cast

# ANSI Colour Codes
CREDBG = "\033[41m"
CRED = "\033[91m"
CBLU = "\033[94m"
CCYN = "\033[96m"
CGRN = "\033[92m"
CYEL = "\033[41m"
CEND = "\033[0m"

# ASCII Art Banner
BANNER = r"""
   _____ _ _    _____          _                 _____ _____ 
  / ____(_) |  / ____|        | |          /\   |  __ \_   _|
 | |  __ _| |_| |     ___   __| | ___     /  \  | |__) || |  
 | | |_ | | __| |    / _ \ / _` |/ _ \   / /\ \ |  ___/ | |  
 | |__| | | |_| |___| (_) | (_| |  __/  / ____ \| |    _| |_ 
  \_____|_|\__|\_____\___/ \__,_|\___| /_/    \_\_|   |_____|
""".strip("\n")


@lru_cache(maxsize=1)
def format_default_welcome(version: str, build: str) -> str:
    """Colored banner and version line for the no-arguments launcher (plain if not a TTY)."""
    homepage = "https://gitcode-api.readthedocs.io"
    docspage = "https://gitcode-api.readthedocs.io"
    banner = BANNER
    version = f"Ver. {version} (build {build})"
    for project_url in cast(List[str], metadata("gitcode_api").get_all("Project-URL")):
        if project_url.casefold().startswith("homepage"):
            homepage = project_url.split(", ")[1]
    if sys.stdout.isatty():
        homepage = f"{CBLU}{homepage}{CEND}"
        docspage = f"{CBLU}{docspage}{CEND}"
        banner = f"{CRED}{BANNER}{CEND}"
        version = f"{CREDBG}{version}{CEND}"
    return f"{banner}\n  {version}\n  Home Page: {homepage}\n  Docs Page: {docspage}\n\n"
