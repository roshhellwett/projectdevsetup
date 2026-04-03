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


if __name__ == "__main__":
    unittest.main()
