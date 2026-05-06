"""ASCII art banner for command-line interface."""

import sys
from functools import lru_cache

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
def format_default_welcome(version: str) -> str:
    """Colored banner and version line for the no-arguments launcher (plain if not a TTY)."""
    if sys.stdout.isatty():
        return f"{CRED}{BANNER}{CEND}\n{CBLU}  Ver. {version}{CEND}\n\n"
    return f"{BANNER}\n  Ver. {version}\n\n"
