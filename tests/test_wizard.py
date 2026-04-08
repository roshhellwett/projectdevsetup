from __future__ import annotations

import unittest
from unittest.mock import patch

from projectdevsetup import wizard


class SelectLanguageTests(unittest.TestCase):
    def test_valid_selection_returns_name_and_key(self) -> None:
        for num, (name, key) in wizard.LANGUAGES.items():
            with patch("projectdevsetup.wizard.ask", return_value=num):
                result_name, result_key = wizard._select_language()
            self.assertEqual(result_name, name)
            self.assertEqual(result_key, key)

    def test_invalid_then_valid_selection(self) -> None:
        with patch("projectdevsetup.wizard.ask", side_effect=["0", "abc", "1"]):
            name, key = wizard._select_language()
        self.assertEqual(name, "Python")
        self.assertEqual(key, "python")


class PreflightTests(unittest.TestCase):
    def test_preflight_exits_without_internet(self) -> None:
        with patch("projectdevsetup.wizard.check_internet", return_value=False):
            with self.assertRaises(SystemExit) as ctx:
                wizard._preflight_checks()
        self.assertEqual(ctx.exception.code, 1)

    def test_preflight_exits_on_insufficient_disk_space(self) -> None:
        with patch("projectdevsetup.wizard.check_internet", return_value=True), \
             patch("projectdevsetup.wizard.check_disk_space", return_value=False):
            with self.assertRaises(SystemExit) as ctx:
                wizard._preflight_checks()
        self.assertEqual(ctx.exception.code, 1)


class RunFlowTests(unittest.TestCase):
    def _make_fake_installer(self):
        return type(
            "FakeInstaller",
            (),
            {
                "__init__": lambda self: setattr(self, "sys_info", object()),
                "install_for_language": lambda self, language: True,
            },
        )

    def test_run_single_language_flow(self) -> None:
        fake_installer = self._make_fake_installer()

        with patch("projectdevsetup.wizard._preflight_checks"), patch(
            "projectdevsetup.wizard._select_language", return_value=("Python", "python")
        ), patch(
            "projectdevsetup.wizard.Installer", fake_installer
        ), patch(
            "projectdevsetup.wizard.ensure_vscode_installed", return_value=True
        ) as ensure_vscode, patch(
            "projectdevsetup.wizard.install_extensions"
        ) as install_ext:
            wizard.run()

        ensure_vscode.assert_called_once()
        install_ext.assert_called_once_with("python")

    def test_run_all_languages_flow(self) -> None:
        fake_installer = self._make_fake_installer()
        installed_langs: list[str] = []

        original_install = fake_installer.install_for_language

        def tracking_install(self_inst, lang):
            installed_langs.append(lang)
            return True

        fake_installer.install_for_language = tracking_install

        with patch("projectdevsetup.wizard._preflight_checks"), patch(
            "projectdevsetup.wizard._select_language", return_value=("All Languages", "all")
        ), patch(
            "projectdevsetup.wizard.Installer", fake_installer
        ), patch(
            "projectdevsetup.wizard.ensure_vscode_installed", return_value=True
        ), patch(
            "projectdevsetup.wizard.install_extensions"
        ) as install_ext:
            wizard.run()

        # Should have installed all 8 individual languages
        self.assertEqual(len(installed_langs), 8)
        self.assertNotIn("all", installed_langs)
        # Extensions installed for each language
        self.assertEqual(install_ext.call_count, 8)

    def test_run_skips_extensions_when_vscode_not_available(self) -> None:
        fake_installer = self._make_fake_installer()

        with patch("projectdevsetup.wizard._preflight_checks"), patch(
            "projectdevsetup.wizard._select_language", return_value=("Go", "go")
        ), patch(
            "projectdevsetup.wizard.Installer", fake_installer
        ), patch(
            "projectdevsetup.wizard.ensure_vscode_installed", return_value=False
        ), patch(
            "projectdevsetup.wizard.install_extensions"
        ) as install_ext:
            wizard.run()

        install_ext.assert_not_called()


class LanguageConstantsTests(unittest.TestCase):
    def test_all_lang_keys_excludes_all(self) -> None:
        self.assertNotIn("all", wizard._ALL_LANG_KEYS)
        self.assertEqual(len(wizard._ALL_LANG_KEYS), 8)

    def test_languages_has_nine_entries(self) -> None:
        self.assertEqual(len(wizard.LANGUAGES), 9)


if __name__ == "__main__":
    unittest.main()
