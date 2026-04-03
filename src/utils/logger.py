"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

import sys
from colorama import Fore, Style, init

init(autoreset=True)


def _safe_print(message: str):
    """Print with UTF-8 encoding fix for Windows."""
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode("ascii", "replace").decode("ascii"))


def info(message: str):
    """Blue info message."""
    _safe_print(f"{Fore.CYAN}[projectdevsetup]{Style.RESET_ALL} {message}")


def success(message: str):
    """Green success message."""
    _safe_print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")


def warning(message: str):
    """Yellow warning message."""
    _safe_print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")


def error(message: str):
    """Red error message in plain English. Never show raw exceptions."""
    _safe_print(f"{Fore.RED}[X] {message}{Style.RESET_ALL}")


def step(number: int, total: int, message: str):
    """Shows progress like: [2/5] Installing GCC..."""
    _safe_print(f"{Fore.BLUE}[{number}/{total}]{Style.RESET_ALL} {message}...")


def header():
    """Print the welcome banner."""
    _safe_print(f"""
{Fore.CYAN}{"=" * 60}
  projectdevsetup - Zenith Open Source Projects
  Automatic Developer Environment Setup for Beginners
{"=" * 60}{Style.RESET_ALL}
""")


def already_installed(tool: str):
    """Tell user a tool is already installed - skip it."""
    _safe_print(
        f"{Fore.GREEN}[OK] {tool} is already installed. Skipping.{Style.RESET_ALL}"
    )


def ask(prompt: str) -> str:
    """Prompt the user for input with consistent styling."""
    return input(f"{Fore.YELLOW}>>  {prompt}{Style.RESET_ALL} ")


def divider():
    _safe_print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")
