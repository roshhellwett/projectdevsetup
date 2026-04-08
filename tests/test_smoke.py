"""
End-to-end smoke tests that simulate a real user picking every menu option.
These tests exercise the full wizard flow for each language choice (1-9),
plus invalid input handling, ensuring no crashes and correct step progression.
"""

from __future__ import annotations

import io
import sys
import unittest
from unittest.mock import MagicMock, patch, call

from projectdevsetup.wizard import run, _select_language, _preflight_checks, LANGUAGES


class SmokeTestEveryMenuOption(unittest.TestCase):
    """Simulate a real user selecting every single menu option (1-9)."""

    def _run_with_choice(self, choice: str):
        """Run the full wizard with a given menu choice, all installs mocked."""
        name, key = LANGUAGES[choice]

        fake_sys_info = MagicMock()
        fake_installer_instance = MagicMock()
        fake_installer_instance.sys_info = fake_sys_info
        fake_installer_instance.install_for_language = MagicMock(return_value=True)
        fake_installer_cls = MagicMock(return_value=fake_installer_instance)

        with patch("projectdevsetup.wizard._preflight_checks"), \
             patch("projectdevsetup.wizard._select_language", return_value=(name, key)), \
             patch("projectdevsetup.wizard.Installer", fake_installer_cls), \
             patch("projectdevsetup.wizard.ensure_vscode_installed", return_value=True) as vscode_mock, \
             patch("projectdevsetup.wizard.install_extensions") as ext_mock:
            # Should not raise
            run()

        return fake_installer_instance, vscode_mock, ext_mock

    def test_option_1_python(self) -> None:
        installer, vscode, ext = self._run_with_choice("1")
        installer.install_for_language.assert_called_once_with("python")
        vscode.assert_called_once()
        ext.assert_called_once_with("python")

    def test_option_2_c(self) -> None:
        installer, vscode, ext = self._run_with_choice("2")
        installer.install_for_language.assert_called_once_with("c")
        ext.assert_called_once_with("c")

    def test_option_3_cpp(self) -> None:
        installer, vscode, ext = self._run_with_choice("3")
        installer.install_for_language.assert_called_once_with("cpp")
        ext.assert_called_once_with("cpp")

    def test_option_4_java(self) -> None:
        installer, vscode, ext = self._run_with_choice("4")
        installer.install_for_language.assert_called_once_with("java")
        ext.assert_called_once_with("java")

    def test_option_5_html(self) -> None:
        installer, vscode, ext = self._run_with_choice("5")
        installer.install_for_language.assert_called_once_with("html")
        ext.assert_called_once_with("html")

    def test_option_6_javascript(self) -> None:
        installer, vscode, ext = self._run_with_choice("6")
        installer.install_for_language.assert_called_once_with("javascript")
        ext.assert_called_once_with("javascript")

    def test_option_7_rust(self) -> None:
        installer, vscode, ext = self._run_with_choice("7")
        installer.install_for_language.assert_called_once_with("rust")
        ext.assert_called_once_with("rust")

    def test_option_8_go(self) -> None:
        installer, vscode, ext = self._run_with_choice("8")
        installer.install_for_language.assert_called_once_with("go")
        ext.assert_called_once_with("go")

    def test_option_9_all_languages(self) -> None:
        installer, vscode, ext = self._run_with_choice("9")
        # Should install all 8 individual languages
        self.assertEqual(installer.install_for_language.call_count, 8)
        called_langs = [c.args[0] for c in installer.install_for_language.call_args_list]
        self.assertNotIn("all", called_langs)
        self.assertIn("python", called_langs)
        self.assertIn("c", called_langs)
        self.assertIn("cpp", called_langs)
        self.assertIn("java", called_langs)
        self.assertIn("html", called_langs)
        self.assertIn("javascript", called_langs)
        self.assertIn("rust", called_langs)
        self.assertIn("go", called_langs)
        # Extensions for all 8
        self.assertEqual(ext.call_count, 8)


class SmokeTestInvalidInput(unittest.TestCase):
    """Test that invalid menu input is rejected and re-prompted."""

    def test_rejects_zero(self) -> None:
        with patch("projectdevsetup.wizard.ask", side_effect=["0", "1"]):
            name, key = _select_language()
        self.assertEqual(key, "python")

    def test_rejects_ten(self) -> None:
        with patch("projectdevsetup.wizard.ask", side_effect=["10", "2"]):
            name, key = _select_language()
        self.assertEqual(key, "c")

    def test_rejects_text(self) -> None:
        with patch("projectdevsetup.wizard.ask", side_effect=["hello", "python", "3"]):
            name, key = _select_language()
        self.assertEqual(key, "cpp")

    def test_rejects_empty(self) -> None:
        with patch("projectdevsetup.wizard.ask", side_effect=["", " ", "4"]):
            name, key = _select_language()
        self.assertEqual(key, "java")

    def test_rejects_negative(self) -> None:
        with patch("projectdevsetup.wizard.ask", side_effect=["-1", "5"]):
            name, key = _select_language()
        self.assertEqual(key, "html")

    def test_rejects_special_characters(self) -> None:
        with patch("projectdevsetup.wizard.ask", side_effect=["@#$", "6"]):
            name, key = _select_language()
        self.assertEqual(key, "javascript")


class SmokeTestVSCodeNotAvailable(unittest.TestCase):
    """Ensure the flow still completes when VS Code is not installed."""

    def test_flow_completes_without_vscode(self) -> None:
        name, key = LANGUAGES["1"]

        fake_installer_instance = MagicMock()
        fake_installer_instance.sys_info = MagicMock()
        fake_installer_instance.install_for_language = MagicMock(return_value=True)
        fake_installer_cls = MagicMock(return_value=fake_installer_instance)

        with patch("projectdevsetup.wizard._preflight_checks"), \
             patch("projectdevsetup.wizard._select_language", return_value=(name, key)), \
             patch("projectdevsetup.wizard.Installer", fake_installer_cls), \
             patch("projectdevsetup.wizard.ensure_vscode_installed", return_value=False), \
             patch("projectdevsetup.wizard.install_extensions") as ext_mock:
            run()  # Should complete without crash

        # Extensions should NOT be called when VS Code failed
        ext_mock.assert_not_called()


class SmokeTestInstallerFailure(unittest.TestCase):
    """Ensure the flow continues even when an installer returns False."""

    def test_flow_continues_after_install_failure(self) -> None:
        name, key = LANGUAGES["7"]  # Rust

        fake_installer_instance = MagicMock()
        fake_installer_instance.sys_info = MagicMock()
        fake_installer_instance.install_for_language = MagicMock(return_value=False)
        fake_installer_cls = MagicMock(return_value=fake_installer_instance)

        with patch("projectdevsetup.wizard._preflight_checks"), \
             patch("projectdevsetup.wizard._select_language", return_value=(name, key)), \
             patch("projectdevsetup.wizard.Installer", fake_installer_cls), \
             patch("projectdevsetup.wizard.ensure_vscode_installed", return_value=True), \
             patch("projectdevsetup.wizard.install_extensions"):
            run()  # Should NOT crash even though install "failed"


class SmokeTestPreflightChecks(unittest.TestCase):
    """Ensure preflight check failures are handled."""

    def test_no_internet_exits(self) -> None:
        with patch("projectdevsetup.wizard.check_internet", return_value=False):
            with self.assertRaises(SystemExit) as ctx:
                _preflight_checks()
        self.assertEqual(ctx.exception.code, 1)

    def test_no_disk_space_exits(self) -> None:
        with patch("projectdevsetup.wizard.check_internet", return_value=True), \
             patch("projectdevsetup.wizard.check_disk_space", return_value=False):
            with self.assertRaises(SystemExit) as ctx:
                _preflight_checks()
        self.assertEqual(ctx.exception.code, 1)

    def test_preflight_passes_with_everything_ok(self) -> None:
        with patch("projectdevsetup.wizard.check_internet", return_value=True), \
             patch("projectdevsetup.wizard.check_disk_space", return_value=True), \
             patch("projectdevsetup.wizard.assert_not_root", return_value=True), \
             patch("projectdevsetup.wizard.sys") as mock_sys:
            mock_sys.platform = "linux"  # Avoid Windows admin check
            _preflight_checks()  # Should not raise


class SmokeTestKeyboardInterrupt(unittest.TestCase):
    """Ensure Ctrl+C is handled cleanly at the entry point."""

    def test_ctrl_c_during_run(self) -> None:
        from projectdevsetup.__main__ import main
        with patch("projectdevsetup.__main__.run", side_effect=KeyboardInterrupt):
            with self.assertRaises(SystemExit) as ctx:
                main()
        self.assertEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
