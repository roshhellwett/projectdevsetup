from __future__ import annotations

import unittest
from unittest.mock import patch

from projectdevsetup import __main__


class MainTests(unittest.TestCase):
    def test_main_calls_run(self) -> None:
        with patch("projectdevsetup.__main__.run") as run:
            __main__.main()
        run.assert_called_once_with()

    def test_keyboard_interrupt_exits_cleanly(self) -> None:
        with patch("projectdevsetup.__main__.run", side_effect=KeyboardInterrupt), patch(
            "projectdevsetup.__main__.error"
        ) as err:
            with self.assertRaises(SystemExit) as ctx:
                __main__.main()
        self.assertEqual(ctx.exception.code, 0)
        err.assert_called_once()

    def test_eof_error_exits_cleanly(self) -> None:
        with patch("projectdevsetup.__main__.run", side_effect=EOFError), patch(
            "projectdevsetup.__main__.error"
        ) as err:
            with self.assertRaises(SystemExit) as ctx:
                __main__.main()
        self.assertEqual(ctx.exception.code, 1)
        err.assert_called_once()

    def test_unexpected_exception_exits_with_code_1(self) -> None:
        with patch("projectdevsetup.__main__.run", side_effect=RuntimeError("boom")), patch(
            "projectdevsetup.__main__.error"
        ), patch("projectdevsetup.__main__._log_crash"):
            with self.assertRaises(SystemExit) as ctx:
                __main__.main()
        self.assertEqual(ctx.exception.code, 1)

    def test_system_exit_is_reraised(self) -> None:
        with patch("projectdevsetup.__main__.run", side_effect=SystemExit(42)):
            with self.assertRaises(SystemExit) as ctx:
                __main__.main()
        self.assertEqual(ctx.exception.code, 42)


if __name__ == "__main__":
    unittest.main()
