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
        ) as error:
            with self.assertRaises(SystemExit) as ctx:
                __main__.main()
        self.assertEqual(ctx.exception.code, 0)
        error.assert_called_once()

    def test_eof_error_exits_cleanly(self) -> None:
        with patch("projectdevsetup.__main__.run", side_effect=EOFError), patch(
            "projectdevsetup.__main__.error"
        ) as error:
            with self.assertRaises(SystemExit) as ctx:
                __main__.main()
        self.assertEqual(ctx.exception.code, 1)
        error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
