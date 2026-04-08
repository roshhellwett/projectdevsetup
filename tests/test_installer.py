from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from projectdevsetup.installer import Installer


class InstallForLanguageTests(unittest.TestCase):
    def setUp(self) -> None:
        with patch("projectdevsetup.installer.detect_system") as detect:
            detect.return_value = MagicMock(os_name="windows", package_manager="winget", is_64bit=True)
            self.installer = Installer()

    def test_unknown_language_returns_false(self) -> None:
        self.assertFalse(self.installer.install_for_language("brainfuck"))

    def test_dispatches_to_correct_handler(self) -> None:
        lang_to_check = {
            "python": "_install_python",
            "c": "_install_gcc",
            "cpp": "_install_gcc",
            "java": "_install_java",
            "html": "_install_html",
            "javascript": "_install_node",
            "rust": "_install_rust",
            "go": "_install_go",
        }
        for lang, method_name in lang_to_check.items():
            with patch.object(self.installer, method_name, return_value=True) as handler:
                result = self.installer.install_for_language(lang)
            self.assertTrue(result, f"Failed for {lang}")
            handler.assert_called_once()

    def test_case_insensitive_language(self) -> None:
        with patch.object(self.installer, "_install_python", return_value=True) as handler:
            result = self.installer.install_for_language("Python")
        self.assertTrue(result)
        handler.assert_called_once()


class InstallPythonTests(unittest.TestCase):
    def test_skips_if_already_installed(self) -> None:
        with patch("projectdevsetup.installer.detect_system") as detect:
            detect.return_value = MagicMock(os_name="windows")
            installer = Installer()
        with patch("projectdevsetup.installer.check_python", return_value=True):
            self.assertTrue(installer._install_python())


class InstallGccTests(unittest.TestCase):
    def test_skips_if_both_installed(self) -> None:
        with patch("projectdevsetup.installer.detect_system") as detect:
            detect.return_value = MagicMock(os_name="linux", package_manager="apt")
            installer = Installer()
        with patch("projectdevsetup.installer.check_gcc", return_value=True), \
             patch("projectdevsetup.installer.check_gpp", return_value=True):
            self.assertTrue(installer._install_gcc())


class InstallHtmlTests(unittest.TestCase):
    def test_html_always_succeeds(self) -> None:
        with patch("projectdevsetup.installer.detect_system") as detect:
            detect.return_value = MagicMock(os_name="windows")
            installer = Installer()
        self.assertTrue(installer._install_html())


class InstallNodeTests(unittest.TestCase):
    def test_skips_if_both_installed(self) -> None:
        with patch("projectdevsetup.installer.detect_system") as detect:
            detect.return_value = MagicMock(os_name="windows")
            installer = Installer()
        with patch("projectdevsetup.installer.check_node", return_value=True), \
             patch("projectdevsetup.installer.check_npm", return_value=True):
            self.assertTrue(installer._install_node())


class InstallRustTests(unittest.TestCase):
    def test_skips_if_both_installed(self) -> None:
        with patch("projectdevsetup.installer.detect_system") as detect:
            detect.return_value = MagicMock(os_name="windows")
            installer = Installer()
        with patch("projectdevsetup.installer.check_rust", return_value=True), \
             patch("projectdevsetup.installer.check_cargo", return_value=True):
            self.assertTrue(installer._install_rust())


class InstallGoTests(unittest.TestCase):
    def test_skips_if_installed(self) -> None:
        with patch("projectdevsetup.installer.detect_system") as detect:
            detect.return_value = MagicMock(os_name="windows")
            installer = Installer()
        with patch("projectdevsetup.installer.check_go", return_value=True):
            self.assertTrue(installer._install_go())


class InstallJavaTests(unittest.TestCase):
    def test_skips_if_installed(self) -> None:
        with patch("projectdevsetup.installer.detect_system") as detect:
            detect.return_value = MagicMock(os_name="windows")
            installer = Installer()
        with patch("projectdevsetup.installer.check_java", return_value=True):
            self.assertTrue(installer._install_java())


class ShowManualInstallTests(unittest.TestCase):
    def test_show_manual_install_with_url(self) -> None:
        with patch("projectdevsetup.installer.detect_system") as detect:
            detect.return_value = MagicMock()
            installer = Installer()
        # Should not raise
        installer._show_manual_install("Test Tool", "https://example.com")

    def test_show_manual_install_without_url(self) -> None:
        with patch("projectdevsetup.installer.detect_system") as detect:
            detect.return_value = MagicMock()
            installer = Installer()
        installer._show_manual_install("Test Tool", "")


if __name__ == "__main__":
    unittest.main()
