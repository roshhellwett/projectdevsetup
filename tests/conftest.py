"""Shared test fixtures and helpers."""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import MagicMock


@dataclass
class FakeSystemInfo:
    """Lightweight stand-in for SystemInfo used everywhere in tests."""

    os_name: str = "windows"
    os_version: str = "10.0.22631"
    architecture: str = "amd64"
    distro: str = ""
    distro_version: str = ""
    package_manager: str = "winget"
    is_64bit: bool = True
    is_arm: bool = False
    has_sudo: bool = False
    has_display: bool = True


def make_completed_process(returncode: int = 0, stdout: str = "", stderr: str = "") -> MagicMock:
    """Return a mock that behaves like subprocess.CompletedProcess."""
    cp = MagicMock()
    cp.returncode = returncode
    cp.stdout = stdout
    cp.stderr = stderr
    return cp
