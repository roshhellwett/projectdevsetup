"""
Console logging helpers.
"""

from __future__ import annotations

from colorama import Fore, Style, init

init(autoreset=True)


def _safe_print(message: str) -> None:
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode("ascii", "replace").decode("ascii"))


def info(message: str) -> None:
    _safe_print(f"{Fore.CYAN}[projectdevsetup]{Style.RESET_ALL} {message}")


def success(message: str) -> None:
    _safe_print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")


def warning(message: str) -> None:
    _safe_print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")


def error(message: str) -> None:
    _safe_print(f"{Fore.RED}[X] {message}{Style.RESET_ALL}")


def step(number: int, total: int, message: str) -> None:
    _safe_print(f"{Fore.BLUE}[{number}/{total}]{Style.RESET_ALL} {message}...")


def header() -> None:
    _safe_print(
        f"""
{Fore.CYAN}{"=" * 60}
  projectdevsetup - Zenith Open Source Projects
  Automatic Developer Environment Setup for Beginners
{"=" * 60}{Style.RESET_ALL}
"""
    )


def already_installed(tool: str) -> None:
    _safe_print(f"{Fore.GREEN}[OK] {tool} is already installed. Skipping.{Style.RESET_ALL}")


def ask(prompt: str) -> str:
    return input(f"{Fore.YELLOW}>>  {prompt}{Style.RESET_ALL} ")


def divider() -> None:
    _safe_print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")
