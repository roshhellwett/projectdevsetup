from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from projectdevsetup import wizard


class WizardTests(unittest.TestCase):
    def test_get_file_name_sanitizes_special_characters(self) -> None:
        with patch("projectdevsetup.wizard.ask", side_effect=["my file!"]):
            self.assertEqual(wizard._get_file_name("python"), "my_file_")

    def test_create_python_starter_file_uses_template(self) -> None:
        output_dir = Path("fake-output")
        with patch.object(Path, "read_text", return_value='print("Hello, World!")') as read_text, patch.object(
            Path, "write_text"
        ) as write_text:
            created = wizard._create_starter_file("python", "hello", output_dir)
        self.assertEqual(created, output_dir / "hello.py")
        read_text.assert_called_once()
        write_text.assert_called_once_with('print("Hello, World!")', encoding="utf-8")

    def test_create_java_starter_file_uses_class_name(self) -> None:
        output_dir = Path("fake-output")
        with patch.object(Path, "write_text") as write_text:
            created = wizard._create_starter_file("java", "my_first_app", output_dir)
        self.assertEqual(created.name, "MyFirstApp.java")
        self.assertIn("public class MyFirstApp", write_text.call_args.args[0])

    def test_preflight_exits_without_internet(self) -> None:
        with patch("projectdevsetup.wizard.check_internet", return_value=False):
            with self.assertRaises(SystemExit) as ctx:
                wizard._preflight_checks()
        self.assertEqual(ctx.exception.code, 1)

    def test_run_python_flow_completes_happy_path(self) -> None:
        fake_installer = type(
            "FakeInstaller",
            (),
            {
                "__init__": lambda self: setattr(self, "sys_info", object()),
                "install_for_language": lambda self, language: True,
            },
        )
        created_file = Path("fake-output/hello.py")

        with patch("projectdevsetup.wizard._preflight_checks"), patch(
            "projectdevsetup.wizard._select_language", return_value=("Python", "python")
        ), patch(
            "projectdevsetup.wizard._get_file_name", return_value="hello"
        ), patch(
            "projectdevsetup.wizard._get_output_dir", return_value=Path("fake-output")
        ), patch(
            "projectdevsetup.wizard._create_starter_file", return_value=created_file
        ) as create_file, patch(
            "projectdevsetup.wizard.Installer", fake_installer
        ), patch(
            "projectdevsetup.wizard.ensure_vscode_installed", return_value=True
        ) as ensure_vscode, patch(
            "projectdevsetup.wizard.install_extensions"
        ) as install_extensions, patch(
            "projectdevsetup.wizard.create_venv"
        ) as create_venv, patch(
            "projectdevsetup.wizard.open_in_vscode"
        ) as open_in_vscode:
            wizard.run()

        create_file.assert_called_once_with("python", "hello", Path("fake-output"))
        ensure_vscode.assert_called_once()
        install_extensions.assert_called_once_with("python")
        create_venv.assert_called_once_with(Path("fake-output"))
        open_in_vscode.assert_called_once_with(created_file)


if __name__ == "__main__":
    unittest.main()
