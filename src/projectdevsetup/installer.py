"""
Tool installer orchestration.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from projectdevsetup.detector import (
    check_brew,
    check_cargo,
    check_gcc,
    check_go,
    check_gpp,
    check_java,
    check_node,
    check_npm,
    check_python,
    check_rust,
)
from projectdevsetup.network import download_file, get_temp_dir
from projectdevsetup.path_manager import add_to_path, verify_in_path
from projectdevsetup.utils.logger import already_installed, error, info, success, warning
from projectdevsetup.utils.os_detect import SystemInfo, detect_system

URLS = {
    "jdk_windows": "https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.exe",
    "node_windows": "https://nodejs.org/dist/latest/node-latest-x64.msi",
    "go_windows": "https://go.dev/dl/go1.22.0.windows-amd64.msi",
}


class Installer:
    """Install beginner tooling for a selected language."""

    def __init__(self) -> None:
        self.sys_info: SystemInfo = detect_system()

    def install_for_language(self, language: str) -> bool:
        handlers = {
            "python": self._install_python,
            "c": self._install_gcc,
            "cpp": self._install_gcc,
            "java": self._install_java,
            "html": self._install_html,
            "javascript": self._install_node,
            "rust": self._install_rust,
            "go": self._install_go,
        }
        handler = handlers.get(language.lower())
        if handler is None:
            error(f"Unknown language: {language}")
            return False
        return handler()

    def _install_python(self) -> bool:
        if check_python():
            already_installed("Python")
            return True

        info("Installing Python...")
        if self.sys_info.os_name == "windows":
            return self._install_python_windows()
        if self.sys_info.os_name == "linux":
            return self._install_via_package_manager(
                ["python3", "python3-pip", "python3-venv"], "Python"
            )
        if self.sys_info.os_name == "mac":
            return self._install_via_brew("python3", "Python")
        return False

    def _install_python_windows(self) -> bool:
        tmp = get_temp_dir()
        arch = "amd64" if self.sys_info.is_64bit else "win32"
        url = f"https://www.python.org/ftp/python/3.12.0/python-3.12.0-{arch}.exe"
        installer = tmp / "python_installer.exe"
        if not download_file(url, installer, "Python"):
            return False

        try:
            subprocess.run(
                [
                    str(installer),
                    "/quiet",
                    "InstallAllUsers=1",
                    "PrependPath=1",
                    "Include_test=0",
                ],
                timeout=300,
                check=False,
            )
        except Exception:
            self._show_manual_install("Python", "https://www.python.org/downloads/")
            return False

        if check_python():
            success("Python installed successfully!")
            return True

        self._show_manual_install("Python", "https://www.python.org/downloads/")
        return False

    def _install_gcc(self) -> bool:
        if check_gcc() and check_gpp():
            already_installed("GCC / G++")
            return True

        info("Installing GCC and G++...")
        if self.sys_info.os_name == "windows":
            return self._install_gcc_windows()
        if self.sys_info.os_name == "linux":
            packages = (
                ["gcc", "g++", "build-essential"]
                if self.sys_info.package_manager == "apt"
                else ["gcc", "g++"]
            )
            return self._install_via_package_manager(packages, "GCC")
        if self.sys_info.os_name == "mac":
            return self._install_xcode_cli_tools()
        return False

    def _install_gcc_windows(self) -> bool:
        info("Installing MSYS2 (includes GCC for Windows)...")
        tmp = get_temp_dir()
        arch = "x86_64" if self.sys_info.is_64bit else "i686"
        url = (
            "https://github.com/msys2/msys2-installer/releases/download/"
            f"2024-01-13/msys2-{arch}-20240113.exe"
        )
        installer = tmp / "msys2_installer.exe"
        if not download_file(url, installer, "MSYS2 (GCC)"):
            self._show_manual_install("GCC for Windows (MSYS2)", "https://www.msys2.org/")
            return False

        try:
            subprocess.run(
                [str(installer), "install", "--root", "C:\\msys64", "--confirm-command"],
                timeout=600,
                check=False,
            )
            subprocess.run(
                [
                    "C:\\msys64\\usr\\bin\\pacman.exe",
                    "-S",
                    "--noconfirm",
                    "mingw-w64-x86_64-gcc",
                ],
                timeout=300,
                check=False,
            )
            add_to_path("C:\\msys64\\mingw64\\bin", "GCC")
        except Exception:
            self._show_manual_install("GCC (MSYS2)", "https://www.msys2.org/")
            return False

        if verify_in_path("gcc"):
            success("GCC installed successfully!")
            return True

        self._show_manual_install("GCC (MSYS2)", "https://www.msys2.org/")
        return False

    def _install_xcode_cli_tools(self) -> bool:
        info("Installing Xcode Command Line Tools (includes GCC)...")
        try:
            subprocess.run(["xcode-select", "--install"], timeout=30, check=False)
        except Exception:
            self._show_manual_install(
                "Xcode Command Line Tools", "https://developer.apple.com/xcode/"
            )
            return False

        warning(
            "A popup appeared asking to install developer tools. Please click 'Install' "
            "and wait for it to finish, then run this tool again."
        )
        return False

    def _install_java(self) -> bool:
        if check_java():
            already_installed("Java JDK")
            return True

        info("Installing Java JDK 21 LTS...")
        if self.sys_info.os_name == "windows":
            return self._install_java_windows()
        if self.sys_info.os_name == "linux":
            packages = (
                ["default-jdk"]
                if self.sys_info.package_manager == "apt"
                else ["java-21-openjdk"]
            )
            return self._install_via_package_manager(packages, "Java JDK")
        if self.sys_info.os_name == "mac":
            return self._install_via_brew("openjdk@21", "Java JDK 21")
        return False

    def _install_java_windows(self) -> bool:
        installer = get_temp_dir() / "jdk_installer.exe"
        if not download_file(URLS["jdk_windows"], installer, "Java JDK 21"):
            self._show_manual_install("Java JDK", "https://adoptium.net/")
            return False

        try:
            subprocess.run([str(installer), "/s"], timeout=300, check=False)
        except Exception:
            self._show_manual_install("Java JDK", "https://adoptium.net/")
            return False

        warning("Java JDK installed. Please restart your terminal for it to be available.")
        return True

    def _install_html(self) -> bool:
        success("HTML and CSS do not need any installation. VS Code with Live Server is enough.")
        return True

    def _install_node(self) -> bool:
        if check_node() and check_npm():
            already_installed("Node.js and npm")
            return True

        info("Installing Node.js (includes npm)...")
        if self.sys_info.os_name == "windows":
            return self._install_node_windows()
        if self.sys_info.os_name == "linux":
            return self._install_node_linux()
        if self.sys_info.os_name == "mac":
            return self._install_via_brew("node", "Node.js")
        return False

    def _install_node_windows(self) -> bool:
        installer = get_temp_dir() / "node_installer.msi"
        if not download_file(URLS["node_windows"], installer, "Node.js"):
            self._show_manual_install("Node.js", "https://nodejs.org/")
            return False

        try:
            subprocess.run(["msiexec", "/i", str(installer), "/quiet"], timeout=300, check=False)
        except Exception:
            self._show_manual_install("Node.js", "https://nodejs.org/")
            return False

        if check_node():
            success("Node.js installed successfully!")
            return True

        self._show_manual_install("Node.js", "https://nodejs.org/")
        return False

    def _install_node_linux(self) -> bool:
        try:
            subprocess.run(
                [
                    "bash",
                    "-c",
                    "curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -",
                ],
                timeout=120,
                check=False,
            )
        except Exception:
            pass
        return self._install_via_package_manager(["nodejs", "npm"], "Node.js")

    def _install_rust(self) -> bool:
        if check_rust() and check_cargo():
            already_installed("Rust and Cargo")
            return True

        info("Installing Rust via rustup...")
        if self.sys_info.os_name == "windows":
            return self._install_rust_windows()
        return self._install_rust_unix()

    def _install_rust_windows(self) -> bool:
        installer = get_temp_dir() / "rustup-init.exe"
        if not download_file("https://win.rustup.rs/x86_64", installer, "Rust (rustup)"):
            self._show_manual_install("Rust", "https://rustup.rs/")
            return False

        try:
            subprocess.run([str(installer), "-y"], timeout=600, check=False)
            add_to_path(str(Path.home() / ".cargo" / "bin"), "Rust/Cargo")
        except Exception:
            self._show_manual_install("Rust", "https://rustup.rs/")
            return False

        if check_rust():
            success("Rust installed successfully!")
            return True

        self._show_manual_install("Rust", "https://rustup.rs/")
        return False

    def _install_rust_unix(self) -> bool:
        try:
            subprocess.run(
                [
                    "bash",
                    "-c",
                    "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y",
                ],
                timeout=600,
                check=False,
            )
            add_to_path(str(Path.home() / ".cargo" / "bin"), "Rust/Cargo")
        except Exception:
            self._show_manual_install("Rust", "https://rustup.rs/")
            return False

        if check_rust():
            success("Rust installed successfully!")
            return True

        self._show_manual_install("Rust", "https://rustup.rs/")
        return False

    def _install_go(self) -> bool:
        if check_go():
            already_installed("Go")
            return True

        info("Installing Go...")
        if self.sys_info.os_name == "windows":
            return self._install_go_windows()
        if self.sys_info.os_name == "linux":
            return self._install_via_package_manager(["golang-go"], "Go")
        if self.sys_info.os_name == "mac":
            return self._install_via_brew("go", "Go")
        return False

    def _install_go_windows(self) -> bool:
        installer = get_temp_dir() / "go_installer.msi"
        if not download_file(URLS["go_windows"], installer, "Go"):
            self._show_manual_install("Go", "https://go.dev/dl/")
            return False

        try:
            subprocess.run(["msiexec", "/i", str(installer), "/quiet"], timeout=300, check=False)
            add_to_path("C:\\Go\\bin", "Go")
        except Exception:
            self._show_manual_install("Go", "https://go.dev/dl/")
            return False

        if check_go():
            success("Go installed successfully!")
            return True

        self._show_manual_install("Go", "https://go.dev/dl/")
        return False

    def _install_via_package_manager(self, packages: list[str], tool_name: str) -> bool:
        pkg_commands = {
            "apt": ["sudo", "apt-get", "install", "-y"],
            "pacman": ["sudo", "pacman", "-S", "--noconfirm"],
            "dnf": ["sudo", "dnf", "install", "-y"],
            "yum": ["sudo", "yum", "install", "-y"],
            "zypper": ["sudo", "zypper", "install", "-y"],
            "apk": ["sudo", "apk", "add"],
        }
        cmd_prefix = pkg_commands.get(self.sys_info.package_manager)
        if not cmd_prefix:
            warning(
                f"No supported package manager found to install {tool_name}. Please install it manually."
            )
            return False

        try:
            if self.sys_info.package_manager == "apt":
                subprocess.run(
                    ["sudo", "apt-get", "update"],
                    capture_output=True,
                    timeout=60,
                    check=False,
                )
            result = subprocess.run(cmd_prefix + packages, timeout=300, check=False)
        except subprocess.TimeoutExpired:
            error(f"Installation of {tool_name} took too long. Please try again or install manually.")
            return False
        except Exception:
            self._show_manual_install(tool_name, "")
            return False

        if result.returncode == 0:
            success(f"{tool_name} installed successfully!")
            return True

        self._show_manual_install(tool_name, "")
        return False

    def _install_via_brew(self, formula: str, tool_name: str) -> bool:
        if not check_brew():
            warning("Homebrew is not installed. Installing Homebrew first...")
            try:
                subprocess.run(
                    [
                        "/bin/bash",
                        "-c",
                        "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)",
                    ],
                    timeout=600,
                    check=False,
                )
            except Exception:
                self._show_manual_install("Homebrew", "https://brew.sh")
                return False

        try:
            result = subprocess.run(["brew", "install", formula], timeout=300, check=False)
        except Exception:
            self._show_manual_install(tool_name, "")
            return False

        if result.returncode == 0:
            success(f"{tool_name} installed successfully!")
            return True

        self._show_manual_install(tool_name, "")
        return False

    def _show_manual_install(self, tool_name: str, url: str) -> None:
        warning(f"Could not install {tool_name} automatically.")
        if url:
            print(
                f"\n  Please download and install {tool_name} manually:\n"
                f"  {url}\n"
                "\n  After installing, run this tool again.\n"
            )
