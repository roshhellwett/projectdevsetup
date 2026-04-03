"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

import subprocess
import platform
import shutil
from src.utils.logger import already_installed, info


def is_installed(command: str, version_flag: str = "--version") -> bool:
    """
    Check if a command-line tool is installed and working.
    Returns True if tool exists and responds to version flag.
    """
    try:
        if not shutil.which(command):
            return False
        result = subprocess.run(
            [command, version_flag], capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def check_python() -> bool:
    cmds = ["python3", "python"]
    for cmd in cmds:
        if is_installed(cmd):
            return True
    return False


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
    """Check if VSCode (code command) is available."""
    return bool(shutil.which("code"))


def check_winget() -> bool:
    return is_installed("winget", "--version")


def check_brew() -> bool:
    return is_installed("brew", "--version")


def check_snap() -> bool:
    return is_installed("snap", "--version")


def get_installed_summary() -> dict:
    """Return a full summary of what is installed."""
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
