from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from projectdevsetup import detector


class IsInstalledTests(unittest.TestCase):
    def test_returns_false_when_command_not_found(self) -> None:
        with patch("projectdevsetup.detector.shutil.which", return_value=None):
            self.assertFalse(detector.is_installed("nonexistent"))

    def test_returns_true_when_command_succeeds(self) -> None:
        cp = MagicMock(returncode=0)
        with patch("projectdevsetup.detector.shutil.which", return_value="/usr/bin/gcc"), \
             patch("projectdevsetup.detector.subprocess.run", return_value=cp):
            self.assertTrue(detector.is_installed("gcc"))

    def test_returns_false_when_version_probe_fails(self) -> None:
        cp = MagicMock(returncode=1)
        with patch("projectdevsetup.detector.shutil.which", return_value="/usr/bin/gcc"), \
             patch("projectdevsetup.detector.subprocess.run", return_value=cp):
            self.assertFalse(detector.is_installed("gcc"))

    def test_returns_false_on_timeout(self) -> None:
        import subprocess
        with patch("projectdevsetup.detector.shutil.which", return_value="/usr/bin/gcc"), \
             patch("projectdevsetup.detector.subprocess.run", side_effect=subprocess.TimeoutExpired("gcc", 10)):
            self.assertFalse(detector.is_installed("gcc"))

    def test_returns_false_on_file_not_found(self) -> None:
        with patch("projectdevsetup.detector.shutil.which", return_value="/usr/bin/gcc"), \
             patch("projectdevsetup.detector.subprocess.run", side_effect=FileNotFoundError):
            self.assertFalse(detector.is_installed("gcc"))

    def test_custom_version_flag(self) -> None:
        cp = MagicMock(returncode=0)
        with patch("projectdevsetup.detector.shutil.which", return_value="/usr/bin/java"), \
             patch("projectdevsetup.detector.subprocess.run", return_value=cp) as run_mock:
            self.assertTrue(detector.is_installed("java", "-version"))
        run_mock.assert_called_once()
        args = run_mock.call_args[0][0]
        self.assertEqual(args, ["java", "-version"])


class CheckFunctionTests(unittest.TestCase):
    def test_check_python_tries_python3_first(self) -> None:
        with patch("projectdevsetup.detector.is_installed", side_effect=[True]) as mock:
            self.assertTrue(detector.check_python())
        mock.assert_called_once_with("python3")

    def test_check_python_falls_back_to_python(self) -> None:
        with patch("projectdevsetup.detector.is_installed", side_effect=[False, True]):
            self.assertTrue(detector.check_python())

    def test_check_python_returns_false_when_neither_found(self) -> None:
        with patch("projectdevsetup.detector.is_installed", side_effect=[False, False]):
            self.assertFalse(detector.check_python())

    def test_check_java_uses_dash_version(self) -> None:
        with patch("projectdevsetup.detector.is_installed", return_value=True) as mock:
            self.assertTrue(detector.check_java())
        mock.assert_called_once_with("java", "-version")

    def test_check_go_uses_version_subcommand(self) -> None:
        with patch("projectdevsetup.detector.is_installed", return_value=True) as mock:
            self.assertTrue(detector.check_go())
        mock.assert_called_once_with("go", "version")

    def test_check_vscode_uses_shutil_which(self) -> None:
        with patch("projectdevsetup.detector.shutil.which", return_value="/usr/bin/code"):
            self.assertTrue(detector.check_vscode())
        with patch("projectdevsetup.detector.shutil.which", return_value=None):
            self.assertFalse(detector.check_vscode())


class GetInstalledSummaryTests(unittest.TestCase):
    def test_returns_dict_with_expected_keys(self) -> None:
        with patch("projectdevsetup.detector.is_installed", return_value=False), \
             patch("projectdevsetup.detector.shutil.which", return_value=None):
            summary = detector.get_installed_summary()
        expected_keys = {
            "python", "gcc", "gpp", "java", "node", "npm",
            "rust", "cargo", "go", "vscode", "winget", "brew", "snap",
        }
        self.assertEqual(set(summary.keys()), expected_keys)

    def test_all_values_are_booleans(self) -> None:
        with patch("projectdevsetup.detector.is_installed", return_value=False), \
             patch("projectdevsetup.detector.shutil.which", return_value=None):
            summary = detector.get_installed_summary()
        for value in summary.values():
            self.assertIsInstance(value, bool)


if __name__ == "__main__":
    unittest.main()
