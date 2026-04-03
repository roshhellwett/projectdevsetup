"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

import subprocess
import platform
import webbrowser
import os
from pathlib import Path
from projectdevsetup.detector import check_vscode
from projectdevsetup.network import download_file, get_temp_dir
from projectdevsetup.utils.logger import (
    info,
    success,
    error,
    warning,
    already_installed,
)
from projectdevsetup.utils.os_detect import detect_system

VSCODE_DOWNLOAD_PAGE = "https://code.visualstudio.com/Download"

VSCODE_WINDOWS_URL = (
    "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
)
VSCODE_LINUX_DEB_URL = (
    "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
)
VSCODE_LINUX_RPM_URL = (
    "https://code.visualstudio.com/sha/download?build=stable&os=linux-rpm-x64"
)
VSCODE_MAC_URL = (
    "https://code.visualstudio.com/sha/download?build=stable&os=darwin-universal"
)

EXTENSIONS = {
    "python": ["ms-python.python", "ms-python.pylance"],
    "c": ["ms-vscode.cpptools"],
    "cpp": ["ms-vscode.cpptools"],
    "java": ["vscjava.vscode-java-pack"],
    "html": ["ritwickdey.liveserver", "esbenp.prettier-vscode"],
    "javascript": ["dbaeumer.vscode-eslint", "esbenp.prettier-vscode"],
    "rust": ["rust-lang.rust-analyzer"],
    "go": ["golang.go"],
}


def ensure_vscode_installed(sys_info) -> bool:
    """
    Make sure VSCode is installed.
    Returns True if VSCode is available after this function runs.
    """
    if check_vscode():
        already_installed("Visual Studio Code")
        return True

    info("Visual Studio Code is not installed. Attempting to install...")

    if sys_info.os_name == "windows":
        return _install_vscode_windows(sys_info)
    elif sys_info.os_name == "linux":
        return _install_vscode_linux(sys_info)
    elif sys_info.os_name == "mac":
        return _install_vscode_mac(sys_info)
    else:
        _open_download_page()
        return False


def _install_vscode_windows(sys_info) -> bool:
    """Try winget first, then direct download, then browser fallback."""
    if sys_info.package_manager == "winget":
        info("Installing VSCode via winget...")
        try:
            result = subprocess.run(
                [
                    "winget",
                    "install",
                    "--id",
                    "Microsoft.VisualStudioCode",
                    "--silent",
                    "--accept-package-agreements",
                    "--accept-source-agreements",
                ],
                capture_output=True,
                text=True,
                timeout=300,
            )
            if result.returncode == 0 and check_vscode():
                success("Visual Studio Code installed successfully!")
                return True
        except Exception:
            pass

    if sys_info.package_manager == "choco":
        info("Installing VSCode via Chocolatey...")
        try:
            result = subprocess.run(
                ["choco", "install", "vscode", "-y"],
                capture_output=True,
                text=True,
                timeout=300,
            )
            if result.returncode == 0 and check_vscode():
                success("Visual Studio Code installed successfully!")
                return True
        except Exception:
            pass

    info("Downloading VSCode installer directly...")
    tmp = get_temp_dir()
    installer = tmp / "vscode_installer.exe"
    if download_file(VSCODE_WINDOWS_URL, installer, "Visual Studio Code"):
        try:
            info("Running VSCode installer silently...")
            subprocess.run(
                [str(installer), "/VERYSILENT", "/MERGETASKS=!runcode"], timeout=300
            )
            if check_vscode():
                success("Visual Studio Code installed successfully!")
                return True
        except Exception:
            pass

    _open_download_page()
    return False


def _install_vscode_linux(sys_info) -> bool:
    """Try snap, then apt/rpm repo, then browser fallback."""
    if sys_info.package_manager != "none" and _try_snap_install():
        return True

    if sys_info.package_manager == "apt":
        if _try_apt_vscode():
            return True

    if sys_info.package_manager in ("dnf", "yum"):
        if _try_rpm_vscode(sys_info.package_manager):
            return True

    if sys_info.package_manager == "apt":
        tmp = get_temp_dir()
        pkg = tmp / "vscode.deb"
        if download_file(VSCODE_LINUX_DEB_URL, pkg, "Visual Studio Code"):
            try:
                subprocess.run(["sudo", "dpkg", "-i", str(pkg)], timeout=120)
                subprocess.run(["sudo", "apt-get", "install", "-f", "-y"], timeout=120)
                if check_vscode():
                    success("Visual Studio Code installed successfully!")
                    return True
            except Exception:
                pass

    if not sys_info.has_display:
        warning(
            "No display detected. This appears to be a server. "
            "VSCode cannot be installed on a headless server. "
            "Skipping VSCode installation."
        )
        return False

    _open_download_page()
    return False


def _try_snap_install() -> bool:
    """Try installing VSCode via snap."""
    try:
        subprocess.run(
            ["sudo", "systemctl", "start", "snapd"], capture_output=True, timeout=30
        )
        result = subprocess.run(
            ["sudo", "snap", "install", "code", "--classic"],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0 and check_vscode():
            success("Visual Studio Code installed successfully via snap!")
            return True
    except Exception:
        pass
    return False


def _try_apt_vscode() -> bool:
    """Add Microsoft apt repo and install VSCode."""
    try:
        commands = [
            ["sudo", "apt-get", "install", "-y", "wget", "gpg", "apt-transport-https"],
            [
                "bash",
                "-c",
                "wget -qO- https://packages.microsoft.com/keys/microsoft.asc"
                " | gpg --dearmor > /tmp/microsoft.gpg",
            ],
            [
                "sudo",
                "install",
                "-D",
                "-o",
                "root",
                "-g",
                "root",
                "-m",
                "644",
                "/tmp/microsoft.gpg",
                "/etc/apt/keyrings/packages.microsoft.gpg",
            ],
            [
                "bash",
                "-c",
                'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/'
                "packages.microsoft.gpg] https://packages.microsoft.com/"
                'repos/code stable main" | sudo tee '
                "/etc/apt/sources.list.d/vscode.list",
            ],
            ["sudo", "apt-get", "update"],
            ["sudo", "apt-get", "install", "-y", "code"],
        ]
        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                return False
        if check_vscode():
            success("Visual Studio Code installed successfully!")
            return True
    except Exception:
        pass
    return False


def _try_rpm_vscode(pkg_manager: str) -> bool:
    """Install VSCode on Fedora/CentOS via rpm repo."""
    try:
        commands = [
            [
                "sudo",
                "rpm",
                "--import",
                "https://packages.microsoft.com/keys/microsoft.asc",
            ],
            [
                "bash",
                "-c",
                'echo -e "[code]\nname=Visual Studio Code\n'
                "baseurl=https://packages.microsoft.com/yumrepos/vscode\n"
                "enabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com"
                '/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo',
            ],
            ["sudo", pkg_manager, "install", "-y", "code"],
        ]
        for cmd in commands:
            subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if check_vscode():
            success("Visual Studio Code installed successfully!")
            return True
    except Exception:
        pass
    return False


def _install_vscode_mac(sys_info) -> bool:
    """Try homebrew, then direct download, then browser fallback."""
    from projectdevsetup.detector import check_brew

    if check_brew():
        info("Installing VSCode via Homebrew...")
        try:
            result = subprocess.run(
                ["brew", "install", "--cask", "visual-studio-code"],
                capture_output=True,
                text=True,
                timeout=300,
            )
            if result.returncode == 0 and check_vscode():
                success("Visual Studio Code installed successfully!")
                return True
        except Exception:
            pass

    info("Homebrew not found. Installing Homebrew first...")
    try:
        brew_install = subprocess.run(
            [
                "/bin/bash",
                "-c",
                "$(curl -fsSL https://raw.githubusercontent.com/"
                "Homebrew/install/HEAD/install.sh)",
            ],
            timeout=600,
        )
        if brew_install.returncode == 0:
            subprocess.run(
                ["brew", "install", "--cask", "visual-studio-code"], timeout=300
            )
            if check_vscode():
                success("Visual Studio Code installed successfully!")
                return True
    except Exception:
        pass

    _open_download_page()
    return False


def _open_download_page():
    """Open the VSCode download page in the user's browser."""
    warning(
        "Could not install VSCode automatically. "
        "Opening the download page in your browser..."
    )
    print(
        "\n  Please download and install VSCode from:\n"
        f"  {VSCODE_DOWNLOAD_PAGE}\n"
        "\n  After installing, run this command again.\n"
    )
    try:
        webbrowser.open(VSCODE_DOWNLOAD_PAGE)
    except Exception:
        pass


def install_extensions(language: str) -> bool:
    """
    Install VSCode extensions for a given language.
    Returns True if all installed successfully.
    """
    if not check_vscode():
        warning("VSCode is not installed. Skipping extension installation.")
        return False

    exts = EXTENSIONS.get(language.lower(), [])
    if not exts:
        return True

    all_success = True
    for ext in exts:
        info(f"Installing VSCode extension: {ext}")
        for attempt in range(1, 4):
            try:
                result = subprocess.run(
                    ["code", "--install-extension", ext, "--force"],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if result.returncode == 0:
                    success(f"Extension {ext} installed.")
                    break
                else:
                    if attempt == 3:
                        warning(
                            f"Could not install extension {ext} "
                            "automatically.\n"
                            f"  Please install it manually in VSCode:\n"
                            f"  1. Open VSCode\n"
                            f"  2. Press Ctrl+Shift+X\n"
                            f"  3. Search for: {ext}\n"
                            f"  4. Click Install\n"
                        )
                        all_success = False
            except Exception:
                if attempt == 3:
                    all_success = False
    return all_success


def open_in_vscode(file_path: Path):
    """Open a specific file in VSCode."""
    if not check_vscode():
        warning("VSCode is not available. Please open your file manually.")
        return
    try:
        info(f"Opening {file_path.name} in VSCode...")
        subprocess.Popen(["code", str(file_path)])
        success(f"VSCode opened with {file_path.name}!")
    except Exception:
        warning(
            f"Could not open VSCode automatically. "
            f"Please open this file manually:\n"
            f"  {file_path}"
        )
