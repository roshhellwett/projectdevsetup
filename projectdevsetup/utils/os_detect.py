"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

import platform
import subprocess
import sys
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SystemInfo:
    os_name: str
    os_version: str
    architecture: str
    distro: str
    distro_version: str
    package_manager: str
    is_64bit: bool
    is_arm: bool
    has_sudo: bool
    has_display: bool


def detect_system() -> SystemInfo:
    """Detect all system information needed for setup decisions."""
    raw_os = platform.system().lower()
    arch = platform.machine().lower()
    is_arm = arch in ("arm64", "aarch64", "armv7l", "armv6l")
    is_64bit = sys.maxsize > 2**32

    os_name = ""
    os_version = ""
    distro = ""
    distro_version = ""
    package_manager = ""
    has_sudo = False
    has_display = True

    if raw_os == "windows":
        os_name = "windows"
        os_version = platform.version()
        package_manager = _detect_windows_package_manager()

    elif raw_os == "linux":
        os_name = "linux"
        distro, distro_version = _detect_linux_distro()
        package_manager = _detect_linux_package_manager()
        has_sudo = _check_sudo()
        has_display = _check_display()

    elif raw_os == "darwin":
        os_name = "mac"
        os_version = platform.mac_ver()[0]
        package_manager = "brew" if _command_exists("brew") else "none"
        has_sudo = _check_sudo()

    else:
        os_name = "unknown"

    return SystemInfo(
        os_name=os_name,
        os_version=os_version,
        architecture=arch,
        distro=distro,
        distro_version=distro_version,
        package_manager=package_manager,
        is_64bit=is_64bit,
        is_arm=is_arm,
        has_sudo=has_sudo,
        has_display=has_display,
    )


def _detect_linux_distro() -> tuple:
    """Detect Linux distribution name and version."""
    try:
        with open("/etc/os-release") as f:
            lines = f.read().lower()
        name = ""
        version = ""
        for line in lines.splitlines():
            if line.startswith("id="):
                name = line.split("=")[1].strip().strip('"')
            if line.startswith("version_id="):
                version = line.split("=")[1].strip().strip('"')
        return name, version
    except Exception:
        return "unknown", ""


def _detect_linux_package_manager() -> str:
    """Return the available package manager on Linux."""
    managers = ["apt", "pacman", "dnf", "yum", "zypper", "apk"]
    for mgr in managers:
        if _command_exists(mgr):
            return mgr
    return "none"


def _detect_windows_package_manager() -> str:
    """Return available package manager on Windows."""
    if _command_exists("winget"):
        return "winget"
    if _command_exists("choco"):
        return "choco"
    return "none"


def _command_exists(cmd: str) -> bool:
    """Check if a shell command exists on this system."""
    try:
        result = subprocess.run(
            ["where", cmd] if platform.system() == "Windows" else ["which", cmd],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception:
        return False


def _check_sudo() -> bool:
    """Check if sudo is available on Linux/Mac."""
    try:
        result = subprocess.run(["sudo", "-n", "true"], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def _check_display() -> bool:
    """Check if a display is available (for headless Linux detection)."""
    return bool(
        os.environ.get("DISPLAY")
        or os.environ.get("WAYLAND_DISPLAY")
        or platform.system() != "Linux"
    )
