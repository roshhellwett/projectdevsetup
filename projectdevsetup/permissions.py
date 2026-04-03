"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

import os
import platform
import subprocess
from projectdevsetup.utils.logger import error, warning


def check_admin_windows() -> bool:
    """Check if running as administrator on Windows."""
    try:
        import ctypes

        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def check_sudo_linux() -> bool:
    """Check if sudo is available without password on Linux/Mac."""
    try:
        result = subprocess.run(
            ["sudo", "-n", "true"], capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def check_disk_space(required_gb: float = 2.0) -> bool:
    """
    Check if there is enough disk space.
    Default: require at least 2GB free.
    """
    try:
        import shutil

        total, used, free = shutil.disk_usage("/")
        free_gb = free / (1024**3)
        if free_gb < required_gb:
            error(
                f"Not enough disk space. "
                f"You have {free_gb:.1f}GB free but we need "
                f"at least {required_gb}GB. "
                f"Please free up some space and try again."
            )
            return False
        return True
    except Exception:
        return True


def assert_not_root() -> bool:
    """
    Warn if running as root on Linux.
    Running pip packages as root is not recommended.
    """
    if platform.system() == "Linux":
        try:
            if os.geteuid() == 0:
                warning(
                    "You are running as root. This is not recommended. "
                    "Please run as a normal user. "
                    "Use sudo only when prompted."
                )
                return False
        except AttributeError:
            pass
    return True


def handle_no_admin_windows():
    """Tell Windows user exactly how to get admin rights."""
    error("Administrator rights are needed to install developer tools on Windows.")
    print(
        "\n  How to fix this:\n"
        "  1. Close this window\n"
        "  2. Find your terminal (Command Prompt or PowerShell)\n"
        "  3. Right-click on it\n"
        "  4. Click 'Run as administrator'\n"
        "  5. Run the command again\n"
    )


def handle_no_sudo_linux():
    """Tell Linux user exactly how to handle sudo."""
    warning(
        "Some installations need sudo (admin) access. "
        "You may be asked for your password during setup. "
        "This is normal and safe."
    )
