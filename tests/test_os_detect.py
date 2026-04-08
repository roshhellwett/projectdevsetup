from __future__ import annotations

import unittest
from unittest.mock import MagicMock, mock_open, patch

from projectdevsetup.utils.os_detect import (
    SystemInfo,
    _check_display,
    _check_sudo,
    _command_exists,
    _detect_linux_distro,
    _detect_linux_package_manager,
    _detect_windows_package_manager,
    detect_system,
)


class DetectSystemTests(unittest.TestCase):
    def test_detect_windows(self) -> None:
        with patch("projectdevsetup.utils.os_detect.platform.system", return_value="Windows"), \
             patch("projectdevsetup.utils.os_detect.platform.machine", return_value="AMD64"), \
             patch("projectdevsetup.utils.os_detect.platform.version", return_value="10.0.22631"), \
             patch("projectdevsetup.utils.os_detect.sys.maxsize", 2**63), \
             patch("projectdevsetup.utils.os_detect._detect_windows_package_manager", return_value="winget"):
            info = detect_system()
        self.assertEqual(info.os_name, "windows")
        self.assertTrue(info.is_64bit)
        self.assertFalse(info.is_arm)
        self.assertEqual(info.package_manager, "winget")

    def test_detect_linux(self) -> None:
        with patch("projectdevsetup.utils.os_detect.platform.system", return_value="Linux"), \
             patch("projectdevsetup.utils.os_detect.platform.machine", return_value="x86_64"), \
             patch("projectdevsetup.utils.os_detect.sys.maxsize", 2**63), \
             patch("projectdevsetup.utils.os_detect._detect_linux_distro", return_value=("ubuntu", "22.04")), \
             patch("projectdevsetup.utils.os_detect._detect_linux_package_manager", return_value="apt"), \
             patch("projectdevsetup.utils.os_detect._check_sudo", return_value=True), \
             patch("projectdevsetup.utils.os_detect._check_display", return_value=True):
            info = detect_system()
        self.assertEqual(info.os_name, "linux")
        self.assertEqual(info.distro, "ubuntu")
        self.assertEqual(info.package_manager, "apt")
        self.assertTrue(info.has_sudo)

    def test_detect_mac(self) -> None:
        with patch("projectdevsetup.utils.os_detect.platform.system", return_value="Darwin"), \
             patch("projectdevsetup.utils.os_detect.platform.machine", return_value="arm64"), \
             patch("projectdevsetup.utils.os_detect.platform.mac_ver", return_value=("14.0", ("", "", ""), "")), \
             patch("projectdevsetup.utils.os_detect.sys.maxsize", 2**63), \
             patch("projectdevsetup.utils.os_detect._command_exists", return_value=True), \
             patch("projectdevsetup.utils.os_detect._check_sudo", return_value=False):
            info = detect_system()
        self.assertEqual(info.os_name, "mac")
        self.assertTrue(info.is_arm)
        self.assertEqual(info.package_manager, "brew")

    def test_detect_arm_architectures(self) -> None:
        for arch in ("arm64", "aarch64", "armv7l", "armv6l"):
            with patch("projectdevsetup.utils.os_detect.platform.system", return_value="Windows"), \
                 patch("projectdevsetup.utils.os_detect.platform.machine", return_value=arch), \
                 patch("projectdevsetup.utils.os_detect.platform.version", return_value=""), \
                 patch("projectdevsetup.utils.os_detect.sys.maxsize", 2**63), \
                 patch("projectdevsetup.utils.os_detect._detect_windows_package_manager", return_value="none"):
                info = detect_system()
            self.assertTrue(info.is_arm, f"Failed for {arch}")

    def test_unknown_os(self) -> None:
        with patch("projectdevsetup.utils.os_detect.platform.system", return_value="FruitOS"), \
             patch("projectdevsetup.utils.os_detect.platform.machine", return_value="x86_64"), \
             patch("projectdevsetup.utils.os_detect.sys.maxsize", 2**63):
            info = detect_system()
        self.assertEqual(info.os_name, "unknown")


class DetectLinuxDistroTests(unittest.TestCase):
    def test_parses_os_release(self) -> None:
        content = 'ID=ubuntu\nVERSION_ID="22.04"\nNAME="Ubuntu"\n'
        with patch("builtins.open", mock_open(read_data=content)):
            distro, version = _detect_linux_distro()
        self.assertEqual(distro, "ubuntu")
        self.assertEqual(version, "22.04")

    def test_handles_missing_file(self) -> None:
        with patch("builtins.open", side_effect=FileNotFoundError):
            distro, version = _detect_linux_distro()
        self.assertEqual(distro, "unknown")
        self.assertEqual(version, "")


class DetectPackageManagerTests(unittest.TestCase):
    def test_detects_apt(self) -> None:
        with patch("projectdevsetup.utils.os_detect._command_exists", side_effect=lambda c: c == "apt"):
            self.assertEqual(_detect_linux_package_manager(), "apt")

    def test_detects_pacman(self) -> None:
        def exists(cmd):
            return cmd == "pacman"
        with patch("projectdevsetup.utils.os_detect._command_exists", side_effect=exists):
            self.assertEqual(_detect_linux_package_manager(), "pacman")

    def test_returns_none_when_nothing_found(self) -> None:
        with patch("projectdevsetup.utils.os_detect._command_exists", return_value=False):
            self.assertEqual(_detect_linux_package_manager(), "none")

    def test_detect_winget(self) -> None:
        with patch("projectdevsetup.utils.os_detect._command_exists", side_effect=lambda c: c == "winget"):
            self.assertEqual(_detect_windows_package_manager(), "winget")

    def test_detect_choco(self) -> None:
        def exists(cmd):
            return cmd == "choco"
        with patch("projectdevsetup.utils.os_detect._command_exists", side_effect=exists):
            self.assertEqual(_detect_windows_package_manager(), "choco")


class CommandExistsTests(unittest.TestCase):
    def test_returns_true_on_success(self) -> None:
        cp = MagicMock(returncode=0)
        with patch("projectdevsetup.utils.os_detect.subprocess.run", return_value=cp):
            self.assertTrue(_command_exists("python"))

    def test_returns_false_on_failure(self) -> None:
        cp = MagicMock(returncode=1)
        with patch("projectdevsetup.utils.os_detect.subprocess.run", return_value=cp):
            self.assertFalse(_command_exists("nonexistent"))

    def test_returns_false_on_exception(self) -> None:
        with patch("projectdevsetup.utils.os_detect.subprocess.run", side_effect=FileNotFoundError):
            self.assertFalse(_command_exists("nonexistent"))


class CheckDisplayTests(unittest.TestCase):
    def test_returns_true_with_display_env(self) -> None:
        with patch.dict("os.environ", {"DISPLAY": ":0"}), \
             patch("projectdevsetup.utils.os_detect.platform.system", return_value="Linux"):
            self.assertTrue(_check_display())

    def test_returns_true_on_non_linux(self) -> None:
        with patch.dict("os.environ", {}, clear=True), \
             patch("projectdevsetup.utils.os_detect.platform.system", return_value="Windows"):
            self.assertTrue(_check_display())


if __name__ == "__main__":
    unittest.main()
