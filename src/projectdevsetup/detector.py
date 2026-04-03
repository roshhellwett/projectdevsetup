"""
Environment detection helpers.
"""

from __future__ import annotations

import shutil
import subprocess


def is_installed(command: str, version_flag: str = "--version") -> bool:
    """Return True when a command exists and responds to a version probe."""
    if not shutil.which(command):
        return False

    try:
        result = subprocess.run(
            [command, version_flag],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False

    return result.returncode == 0


def check_python() -> bool:
    return any(is_installed(command) for command in ("python3", "python"))


def check_gcc() -> bool:
    return is_installed("gcc")


def check_gpp() -> bool:
    return is_installed("g++")


def check_java() -> bool:
    return is_installed("java", "-version")


def check_node() -> bool:
    return is_installed("node")


def check_npm() -> bool:
    return is_installed("npm")


def check_rust() -> bool:
    return is_installed("rustc")


def check_cargo() -> bool:
    return is_installed("cargo")


def check_go() -> bool:
    return is_installed("go", "version")


def check_vscode() -> bool:
    return bool(shutil.which("code"))


def check_winget() -> bool:
    return is_installed("winget")


def check_brew() -> bool:
    return is_installed("brew")


def check_snap() -> bool:
    return is_installed("snap")


def get_installed_summary() -> dict[str, bool]:
    """Return a summary of supported tools detected on this machine."""
    return {
        "python": check_python(),
        "gcc": check_gcc(),
        "gpp": check_gpp(),
        "java": check_java(),
        "node": check_node(),
        "npm": check_npm(),
        "rust": check_rust(),
        "cargo": check_cargo(),
        "go": check_go(),
        "vscode": check_vscode(),
        "winget": check_winget(),
        "brew": check_brew(),
        "snap": check_snap(),
    }
