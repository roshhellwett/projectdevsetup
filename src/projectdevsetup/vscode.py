"""
Visual Studio Code installation and integration helpers.
"""

from __future__ import annotations

import subprocess
import webbrowser

from projectdevsetup.detector import check_brew, check_vscode
from projectdevsetup.network import download_file, get_temp_dir
from projectdevsetup.utils.logger import already_installed, info, success, warning

VSCODE_DOWNLOAD_PAGE = "https://code.visualstudio.com/Download"
VSCODE_WINDOWS_URL = (
    "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
)
VSCODE_LINUX_DEB_URL = (
    "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
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
    """Return True when VS Code is already installed or successfully installed now."""
    if check_vscode():
        already_installed("Visual Studio Code")
        return True

    info("Visual Studio Code is not installed. Attempting to install...")
    if sys_info.os_name == "windows":
        return _install_vscode_windows(sys_info)
    if sys_info.os_name == "linux":
        return _install_vscode_linux(sys_info)
    if sys_info.os_name == "mac":
        return _install_vscode_mac()

    _open_download_page()
    return False


def _install_vscode_windows(sys_info) -> bool:
    if sys_info.package_manager == "winget":
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
                check=False,
            )
            if result.returncode == 0 and check_vscode():
                success("Visual Studio Code installed successfully!")
                return True
        except Exception:
            pass

    installer = get_temp_dir() / "vscode_installer.exe"
    if download_file(VSCODE_WINDOWS_URL, installer, "Visual Studio Code"):
        try:
            subprocess.run(
                [str(installer), "/VERYSILENT", "/MERGETASKS=!runcode"],
                timeout=300,
                check=False,
            )
            if check_vscode():
                success("Visual Studio Code installed successfully!")
                return True
        except Exception:
            pass

    _open_download_page()
    return False


def _install_vscode_linux(sys_info) -> bool:
    if sys_info.package_manager == "apt":
        pkg = get_temp_dir() / "vscode.deb"
        if download_file(VSCODE_LINUX_DEB_URL, pkg, "Visual Studio Code"):
            try:
                subprocess.run(["sudo", "dpkg", "-i", str(pkg)], timeout=120, check=False)
                subprocess.run(
                    ["sudo", "apt-get", "install", "-f", "-y"],
                    timeout=120,
                    check=False,
                )
                if check_vscode():
                    success("Visual Studio Code installed successfully!")
                    return True
            except Exception:
                pass

    if not sys_info.has_display:
        warning(
            "No display detected. This appears to be a server, so VS Code installation is skipped."
        )
        return False

    _open_download_page()
    return False


def _install_vscode_mac() -> bool:
    if check_brew():
        try:
            result = subprocess.run(
                ["brew", "install", "--cask", "visual-studio-code"],
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )
            if result.returncode == 0 and check_vscode():
                success("Visual Studio Code installed successfully!")
                return True
        except Exception:
            pass

    _open_download_page()
    return False


def _open_download_page() -> None:
    warning(
        "Could not install VS Code automatically. Opening the download page in your browser..."
    )
    print(
        "\n  Please download and install VS Code from:\n"
        f"  {VSCODE_DOWNLOAD_PAGE}\n"
        "\n  After installing, run this command again.\n"
    )
    try:
        webbrowser.open(VSCODE_DOWNLOAD_PAGE)
    except Exception:
        pass


def install_extensions(language: str) -> bool:
    """Install the recommended VS Code extensions for a language."""
    if not check_vscode():
        warning("VS Code is not installed. Skipping extension installation.")
        return False

    exts = EXTENSIONS.get(language.lower(), [])
    if not exts:
        return True

    all_success = True
    for ext in exts:
        info(f"Installing VS Code extension: {ext}")
        try:
            result = subprocess.run(
                ["code", "--install-extension", ext, "--force"],
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
        except Exception:
            result = None

        if result is not None and result.returncode == 0:
            success(f"Extension {ext} installed.")
            continue

        warning(
            "Could not install the extension automatically.\n"
            "  Please install it manually in VS Code:\n"
            "  1. Open VS Code\n"
            "  2. Press Ctrl+Shift+X\n"
            f"  3. Search for: {ext}\n"
            "  4. Click Install\n"
        )
        all_success = False

    return all_success

