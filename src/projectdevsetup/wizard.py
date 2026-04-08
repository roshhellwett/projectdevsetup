"""
Interactive beginner-friendly setup flow.
"""

from __future__ import annotations

import sys

from projectdevsetup.installer import Installer
from projectdevsetup.network import check_internet
from projectdevsetup.permissions import assert_not_root, check_admin_windows, check_disk_space
from projectdevsetup.utils.logger import ask, divider, header, info, success, warning, step
from projectdevsetup.vscode import ensure_vscode_installed, install_extensions

LANGUAGES = {
    "1": ("Python", "python"),
    "2": ("C", "c"),
    "3": ("C++", "cpp"),
    "4": ("Java", "java"),
    "5": ("HTML / CSS", "html"),
    "6": ("JavaScript", "javascript"),
    "7": ("Rust", "rust"),
    "8": ("Go", "go"),
    "9": ("All Languages", "all"),
}

_ALL_LANG_KEYS = [key for _, (_, key) in LANGUAGES.items() if key != "all"]


def run() -> None:
    """Run the interactive setup wizard."""
    header()
    _preflight_checks()

    language_name, language_key = _select_language()

    divider()
    info(f"Setting up {language_name} environment...")
    divider()

    installer = Installer()

    if language_key == "all":
        total_steps = len(_ALL_LANG_KEYS) + 2  # N languages + VS Code + extensions
    else:
        total_steps = 3  # install + VS Code + extensions

    current_step = 1

    if language_key == "all":
        for _, (name, lang_key) in LANGUAGES.items():
            if lang_key == "all":
                continue
            step(current_step, total_steps, f"Installing {name}")
            installer.install_for_language(lang_key)
            current_step += 1
    else:
        step(current_step, total_steps, f"Installing {language_name} tools")
        installer.install_for_language(language_key)
        current_step += 1

    step(current_step, total_steps, "Setting up Visual Studio Code")
    vscode_ok = ensure_vscode_installed(installer.sys_info)
    current_step += 1

    step(current_step, total_steps, "Installing VS Code extensions")
    if vscode_ok:
        if language_key == "all":
            for lang_key in _ALL_LANG_KEYS:
                install_extensions(lang_key)
        else:
            install_extensions(language_key)

    divider()
    success("Everything is set up. Happy coding!")
    print(
        "\n  Made with love by Zenith Open Source Projects\n"
        "  https://zenithopensourceprojects.vercel.app\n"
    )


def _preflight_checks() -> None:
    info("Running checks before we start...")
    info("Checking internet connection...")
    if not check_internet():
        _print_no_internet_and_exit()

    success("Internet connection OK.")
    if not check_disk_space(required_gb=2.0):
        raise SystemExit(1)

    assert_not_root()

    if sys.platform.startswith("win"):
        if not check_admin_windows():
            warning(
                "You are not running as administrator. Some installations may fail. "
                "If needed, restart as administrator."
            )
        else:
            success("Administrator rights detected.")

    success("All checks passed. Starting setup...")
    divider()


def _print_no_internet_and_exit() -> None:
    from projectdevsetup.utils.logger import error

    error("No internet connection detected. Please connect to the internet and run this again.")
    raise SystemExit(1)


def _select_language() -> tuple[str, str]:
    print("  Which programming language do you want to set up?\n")
    for num, (name, _) in LANGUAGES.items():
        print(f"  {num}. {name}")
    print()

    while True:
        choice = ask("Enter a number (1-9):").strip()
        if choice in LANGUAGES:
            name, key = LANGUAGES[choice]
            success(f"You selected: {name}")
            return name, key
        warning("Please enter a number between 1 and 9.")
