from __future__ import annotations

import shutil
import unittest
from unittest.mock import MagicMock, patch

from projectdevsetup import permissions


class CheckAdminWindowsTests(unittest.TestCase):
    def test_returns_bool(self) -> None:
        result = permissions.check_admin_windows()
        self.assertIsInstance(result, bool)

    def test_returns_false_on_exception(self) -> None:
        with patch("builtins.__import__", side_effect=ImportError):
            result = permissions.check_admin_windows()
        self.assertIsInstance(result, bool)


class CheckSudoLinuxTests(unittest.TestCase):
    def test_returns_true_when_sudo_available(self) -> None:
        cp = MagicMock(returncode=0)
        with patch("projectdevsetup.permissions.subprocess.run", return_value=cp):
            self.assertTrue(permissions.check_sudo_linux())

    def test_returns_false_when_sudo_fails(self) -> None:
        cp = MagicMock(returncode=1)
        with patch("projectdevsetup.permissions.subprocess.run", return_value=cp):
            self.assertFalse(permissions.check_sudo_linux())

    def test_returns_false_on_exception(self) -> None:
        with patch("projectdevsetup.permissions.subprocess.run", side_effect=FileNotFoundError):
            self.assertFalse(permissions.check_sudo_linux())


class CheckDiskSpaceTests(unittest.TestCase):
    def test_returns_true_when_enough_space(self) -> None:
        usage = (100 * 1024**3, 50 * 1024**3, 50 * 1024**3)  # 50GB free
        with patch.object(shutil, "disk_usage", return_value=usage):
            self.assertTrue(permissions.check_disk_space(required_gb=2.0))

    def test_returns_false_when_not_enough_space(self) -> None:
        usage = (100 * 1024**3, 99 * 1024**3, 1 * 1024**3)  # 1GB free
        with patch.object(shutil, "disk_usage", return_value=usage):
            self.assertFalse(permissions.check_disk_space(required_gb=2.0))

    def test_returns_true_on_exception(self) -> None:
        """Falls back to True if disk usage can't be determined (safe default)."""
        with patch.object(shutil, "disk_usage", side_effect=OSError):
            self.assertTrue(permissions.check_disk_space())


class AssertNotRootTests(unittest.TestCase):
    def test_returns_true_on_non_linux(self) -> None:
        with patch("projectdevsetup.permissions.platform.system", return_value="Windows"):
            self.assertTrue(permissions.assert_not_root())

    def test_warns_when_root_on_linux(self) -> None:
        with patch("projectdevsetup.permissions.platform.system", return_value="Linux"), \
             patch("projectdevsetup.permissions.os.geteuid", create=True, return_value=0):
            self.assertFalse(permissions.assert_not_root())

    def test_returns_true_when_not_root_on_linux(self) -> None:
        with patch("projectdevsetup.permissions.platform.system", return_value="Linux"), \
             patch("projectdevsetup.permissions.os.geteuid", create=True, return_value=1000):
            self.assertTrue(permissions.assert_not_root())


class HandleNoAdminWindowsTests(unittest.TestCase):
    def test_does_not_raise(self) -> None:
        # Should just print messages, not raise
        permissions.handle_no_admin_windows()

    
class HandleNoSudoLinuxTests(unittest.TestCase):
    def test_does_not_raise(self) -> None:
        permissions.handle_no_sudo_linux()


if __name__ == "__main__":
    unittest.main()
