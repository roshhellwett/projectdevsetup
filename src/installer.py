"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

import subprocess
import platform
import os
from pathlib import Path
from src.detector import (
    check_gcc,
    check_gpp,
    check_java,
    check_node,
    check_npm,
    check_rust,
    check_cargo,
    check_go,
    check_python,
)
from src.network import download_file, get_temp_dir
from src.path_manager import add_to_path, verify_in_path
from src.utils.logger import (
    info,
    success,
    error,
    warning,
    already_installed,
    step,
)
from src.utils.os_detect import detect_system, SystemInfo

URLS = {
    "jdk_windows": "https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.exe",
    "jdk_mac_arm": "https://download.oracle.com/java/21/latest/jdk-21_macos-aarch64_bin.dmg",
    "jdk_mac_x64": "https://download.oracle.com/java/21/latest/jdk-21_macos-x64_bin.dmg",
    "node_windows": "https://nodejs.org/dist/latest/node-latest-x86.msi",
    "go_windows": "https://go.dev/dl/go1.22.0.windows-amd64.msi",
    "go_mac": "https://go.dev/dl/go1.22.0.darwin-amd64.pkg",
}


class Installer:
    def __init__(self):
        self.sys_info: SystemInfo = detect_system()

    def install_for_language(self, language: str) -> bool:
        """
        Install all required tools for a given language.
        Returns True if installation succeeded.
        """
        lang = language.lower()
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
        handler = handlers.get(lang)
        if handler:
            return handler()
        error(f"Unknown language: {language}")
        return False

    def _install_python(self) -> bool:
        if check_python():
            already_installed("Python")
            return True
        info("Installing Python...")
        os_name = self.sys_info.os_name
        if os_name == "windows":
            return self._install_python_windows()
        elif os_name == "linux":
            return self._install_via_package_manager(
                ["python3", "python3-pip", "python3-venv"], "Python"
            )
        elif os_name == "mac":
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
            )
            if check_python():
                success("Python installed successfully!")
                return True
        except Exception:
            pass
        self._show_manual_install("Python", "https://www.python.org/downloads/")
        return False

    def _install_gcc(self) -> bool:
        if check_gcc() and check_gpp():
            already_installed("GCC / G++")
            return True
        info("Installing GCC and G++...")
        os_name = self.sys_info.os_name
        if os_name == "windows":
            return self._install_gcc_windows()
        elif os_name == "linux":
            return self._install_via_package_manager(
                ["gcc", "g++", "build-essential"]
                if self.sys_info.package_manager == "apt"
                else ["gcc", "g++"],
                "GCC",
            )
        elif os_name == "mac":
            return self._install_xcode_cli_tools()
        return False

    def _install_gcc_windows(self) -> bool:
        """Install MSYS2 + GCC on Windows."""
        info("Installing MSYS2 (includes GCC for Windows)...")
        tmp = get_temp_dir()
        arch = "x86_64" if self.sys_info.is_64bit else "i686"
        url = (
            f"https://github.com/msys2/msys2-installer/releases/download/"
            f"2024-01-13/msys2-{arch}-20240113.exe"
        )
        installer = tmp / "msys2_installer.exe"
        if not download_file(url, installer, "MSYS2 (GCC)"):
            self._show_manual_install(
                "GCC for Windows (MSYS2)", "https://www.msys2.org/"
            )
            return False
        try:
            subprocess.run(
                [
                    str(installer),
                    "install",
                    "--root",
                    "C:\\msys64",
                    "--confirm-command",
                ],
                timeout=600,
            )
            subprocess.run(
                [
                    "C:\\msys64\\usr\\bin\\pacman.exe",
                    "-S",
                    "--noconfirm",
                    "mingw-w64-x86_64-gcc",
                ],
                timeout=300,
            )
            add_to_path("C:\\msys64\\mingw64\\bin", "GCC")
            if verify_in_path("gcc"):
                success("GCC installed successfully!")
                return True
        except Exception:
            pass
        self._show_manual_install("GCC (MSYS2)", "https://www.msys2.org/")
        return False

    def _install_xcode_cli_tools(self) -> bool:
        """Install Xcode Command Line Tools on Mac (includes GCC)."""
        info("Installing Xcode Command Line Tools (includes GCC)...")
        try:
            subprocess.run(["xcode-select", "--install"], timeout=30)
            warning(
                "A popup appeared asking to install developer tools. "
                "Please click 'Install' and wait for it to finish. "
                "Then run this tool again."
            )
            return False
        except Exception:
            self._show_manual_install(
                "Xcode Command Line Tools", "https://developer.apple.com/xcode/"
            )
            return False

    def _install_java(self) -> bool:
        if check_java():
            already_installed("Java JDK")
            return True
        info("Installing Java JDK 21 LTS...")
        os_name = self.sys_info.os_name
        if os_name == "windows":
            return self._install_java_windows()
        elif os_name == "linux":
            return self._install_via_package_manager(
                ["default-jdk"]
                if self.sys_info.package_manager == "apt"
                else ["java-21-openjdk"],
                "Java JDK",
            )
        elif os_name == "mac":
            return self._install_via_brew("openjdk@21", "Java JDK 21")
        return False

    def _install_java_windows(self) -> bool:
        tmp = get_temp_dir()
        url = URLS["jdk_windows"]
        installer = tmp / "jdk_installer.exe"
        if not download_file(url, installer, "Java JDK 21"):
            self._show_manual_install("Java JDK", "https://adoptium.net/")
            return False
        try:
            subprocess.run([str(installer), "/s"], timeout=300)
            warning(
                "Java JDK installed. "
                "Please restart your terminal for it to be available."
            )
            return True
        except Exception:
            self._show_manual_install("Java JDK", "https://adoptium.net/")
            return False

    def _install_html(self) -> bool:
        success(
            "HTML and CSS do not need any installation! "
            "Just VSCode with Live Server extension is enough."
        )
        return True

    def _install_node(self) -> bool:
        if check_node() and check_npm():
            already_installed("Node.js and npm")
            return True
        info("Installing Node.js (includes npm)...")
        os_name = self.sys_info.os_name
        if os_name == "windows":
            return self._install_node_windows()
        elif os_name == "linux":
            return self._install_node_linux()
        elif os_name == "mac":
            return self._install_via_brew("node", "Node.js")
        return False

    def _install_node_windows(self) -> bool:
        tmp = get_temp_dir()
        arch = "x64" if self.sys_info.is_64bit else "x86"
        url = f"https://nodejs.org/dist/latest/node-latest-{arch}.msi"
        installer = tmp / "node_installer.msi"
        if not download_file(url, installer, "Node.js"):
            self._show_manual_install("Node.js", "https://nodejs.org/")
            return False
        try:
            subprocess.run(["msiexec", "/i", str(installer), "/quiet"], timeout=300)
            if check_node():
                success("Node.js installed successfully!")
                return True
        except Exception:
            pass
        self._show_manual_install("Node.js", "https://nodejs.org/")
        return False

    def _install_node_linux(self) -> bool:
        try:
            setup = subprocess.run(
                [
                    "bash",
                    "-c",
                    "curl -fsSL https://deb.nodesource.com/setup_lts.x"
                    " | sudo -E bash -",
                ],
                timeout=120,
            )
            return self._install_via_package_manager(["nodejs"], "Node.js")
        except Exception:
            return self._install_via_package_manager(["nodejs", "npm"], "Node.js")

    def _install_rust(self) -> bool:
        if check_rust() and check_cargo():
            already_installed("Rust and Cargo")
            return True
        info("Installing Rust via rustup...")
        os_name = self.sys_info.os_name
        if os_name == "windows":
            return self._install_rust_windows()
        else:
            return self._install_rust_unix()

    def _install_rust_windows(self) -> bool:
        tmp = get_temp_dir()
        url = "https://win.rustup.rs/x86_64"
        installer = tmp / "rustup-init.exe"
        if not download_file(url, installer, "Rust (rustup)"):
            self._show_manual_install("Rust", "https://rustup.rs/")
            return False
        try:
            subprocess.run([str(installer), "-y"], timeout=600)
            cargo_bin = Path.home() / ".cargo" / "bin"
            add_to_path(str(cargo_bin), "Rust/Cargo")
            if check_rust():
                success("Rust installed successfully!")
                return True
        except Exception:
            pass
        self._show_manual_install("Rust", "https://rustup.rs/")
        return False

    def _install_rust_unix(self) -> bool:
        try:
            subprocess.run(
                [
                    "bash",
                    "-c",
                    "curl --proto '=https' --tlsv1.2 "
                    "-sSf https://sh.rustup.rs | sh -s -- -y",
                ],
                timeout=600,
            )
            cargo_bin = Path.home() / ".cargo" / "bin"
            add_to_path(str(cargo_bin), "Rust/Cargo")
            if check_rust():
                success("Rust installed successfully!")
                return True
        except Exception:
            pass
        self._show_manual_install("Rust", "https://rustup.rs/")
        return False

    def _install_go(self) -> bool:
        if check_go():
            already_installed("Go")
            return True
        info("Installing Go...")
        os_name = self.sys_info.os_name
        if os_name == "windows":
            return self._install_go_windows()
        elif os_name == "linux":
            return self._install_via_package_manager(["golang-go"], "Go")
        elif os_name == "mac":
            return self._install_via_brew("go", "Go")
        return False

    def _install_go_windows(self) -> bool:
        tmp = get_temp_dir()
        arch = "amd64" if self.sys_info.is_64bit else "386"
        url = f"https://go.dev/dl/go1.22.0.windows-{arch}.msi"
        installer = tmp / "go_installer.msi"
        if not download_file(url, installer, "Go"):
            self._show_manual_install("Go", "https://go.dev/dl/")
            return False
        try:
            subprocess.run(["msiexec", "/i", str(installer), "/quiet"], timeout=300)
            add_to_path("C:\\Go\\bin", "Go")
            if check_go():
                success("Go installed successfully!")
                return True
        except Exception:
            pass
        self._show_manual_install("Go", "https://go.dev/dl/")
        return False

    def _install_via_package_manager(self, packages: list, tool_name: str) -> bool:
        """Install packages using the system package manager."""
        pm = self.sys_info.package_manager
        pkg_commands = {
            "apt": ["sudo", "apt-get", "install", "-y"],
            "pacman": ["sudo", "pacman", "-S", "--noconfirm"],
            "dnf": ["sudo", "dnf", "install", "-y"],
            "yum": ["sudo", "yum", "install", "-y"],
            "zypper": ["sudo", "zypper", "install", "-y"],
            "apk": ["sudo", "apk", "add"],
        }
        cmd_prefix = pkg_commands.get(pm)
        if not cmd_prefix:
            warning(
                f"No supported package manager found to install {tool_name}. "
                "Please install it manually."
            )
            return False
        try:
            if pm == "apt":
                subprocess.run(
                    ["sudo", "apt-get", "update"], capture_output=True, timeout=60
                )
            result = subprocess.run(cmd_prefix + packages, timeout=300)
            if result.returncode == 0:
                success(f"{tool_name} installed successfully!")
                return True
        except subprocess.TimeoutExpired:
            error(
                f"Installation of {tool_name} took too long. "
                "Please try again or install manually."
            )
        except Exception:
            pass
        self._show_manual_install(tool_name, "")
        return False

    def _install_via_brew(self, formula: str, tool_name: str) -> bool:
        """Install via Homebrew on Mac."""
        from src.detector import check_brew

        if not check_brew():
            warning("Homebrew is not installed. Installing Homebrew first...")
            try:
                subprocess.run(
                    [
                        "/bin/bash",
                        "-c",
                        "$(curl -fsSL https://raw.githubusercontent.com/"
                        "Homebrew/install/HEAD/install.sh)",
                    ],
                    timeout=600,
                )
            except Exception:
                self._show_manual_install("Homebrew", "https://brew.sh")
                return False
        try:
            result = subprocess.run(["brew", "install", formula], timeout=300)
            if result.returncode == 0:
                success(f"{tool_name} installed successfully!")
                return True
        except Exception:
            pass
        self._show_manual_install(tool_name, "")
        return False

    def _show_manual_install(self, tool_name: str, url: str):
        """Show a beginner-friendly message for manual install."""
        warning(f"Could not install {tool_name} automatically.")
        if url:
            print(
                f"\n  Please download and install {tool_name} manually:\n"
                f"  {url}\n"
                f"\n  After installing, run this tool again.\n"
            )
            try:
                import webbrowser

                webbrowser.open(url)
            except Exception:
                pass
