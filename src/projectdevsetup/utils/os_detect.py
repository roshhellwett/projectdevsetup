"""
Operating system detection helpers.
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from dataclasses import dataclass


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
    raw_os = platform.system().lower()
    arch = platform.machine().lower()
    is_arm = arch in ("arm64", "aarch64", "armv7l", "armv6l")
    is_64bit = sys.maxsize > 2**32

    os_name = "unknown"
    os_version = ""
    distro = ""
    distro_version = ""
    package_manager = "none"
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


def _detect_linux_distro() -> tuple[str, str]:
    try:
        with open("/etc/os-release", encoding="utf-8") as file_obj:
            lines = file_obj.read().lower().splitlines()
    except Exception:
        return "unknown", ""

    name = "unknown"
    version = ""
    for line in lines:
        if line.startswith("id="):
            name = line.split("=", 1)[1].strip().strip('"')
        elif line.startswith("version_id="):
            version = line.split("=", 1)[1].strip().strip('"')
    return name, version


def _detect_linux_package_manager() -> str:
    for manager in ("apt", "pacman", "dnf", "yum", "zypper", "apk"):
        if _command_exists(manager):
            return manager
    return "none"


def _detect_windows_package_manager() -> str:
    if _command_exists("winget"):
        return "winget"
    if _command_exists("choco"):
        return "choco"
    return "none"


def _command_exists(cmd: str) -> bool:
    try:
        result = subprocess.run(
            ["where", cmd] if platform.system() == "Windows" else ["which", cmd],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception:
        return False
    return result.returncode == 0


def _check_sudo() -> bool:
    try:
        result = subprocess.run(
            ["sudo", "-n", "true"],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception:
        return False
    return result.returncode == 0


def _check_display() -> bool:
    return bool(
        os.environ.get("DISPLAY")
        or os.environ.get("WAYLAND_DISPLAY")
        or platform.system() != "Linux"
    )
