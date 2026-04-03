"""
Permission and disk-space checks.
"""

from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path

from projectdevsetup.utils.logger import error, warning


def check_admin_windows() -> bool:
    """Return True when the current Windows process is elevated."""
    try:
        import ctypes

        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def check_sudo_linux() -> bool:
    """Return True when sudo is available without a password prompt."""
    try:
        result = subprocess.run(
            ["sudo", "-n", "true"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except Exception:
        return False
    return result.returncode == 0


def check_disk_space(required_gb: float = 2.0, path: Path | None = None) -> bool:
    """Ensure enough disk space exists on the target drive."""
    try:
        import shutil

        target = path or Path.home()
        _, _, free = shutil.disk_usage(target)
        free_gb = free / (1024**3)
    except Exception:
        return True

    if free_gb < required_gb:
        error(
            f"Not enough disk space. You have {free_gb:.1f}GB free but we need at least {required_gb}GB. "
            "Please free up some space and try again."
        )
        return False
    return True


def assert_not_root() -> bool:
    """Warn when running as root on Linux."""
    if platform.system() != "Linux":
        return True
    try:
        if os.geteuid() == 0:
            warning(
                "You are running as root. This is not recommended. Please run as a normal user. "
                "Use sudo only when prompted."
            )
            return False
    except AttributeError:
        pass
    return True


def handle_no_admin_windows() -> None:
    error("Administrator rights are needed to install developer tools on Windows.")
    print(
        "\n  How to fix this:\n"
        "  1. Close this window\n"
        "  2. Find your terminal (Command Prompt or PowerShell)\n"
        "  3. Right-click on it\n"
        "  4. Click 'Run as administrator'\n"
        "  5. Run the command again\n"
    )


def handle_no_sudo_linux() -> None:
    warning(
        "Some installations need sudo (admin) access. You may be asked for your password during setup. "
        "This is normal and safe."
    )
