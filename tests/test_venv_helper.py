from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from projectdevsetup.utils import venv_helper


class VenvHelperTests(unittest.TestCase):
    def test_create_venv_creates_requirements_file_on_success(self) -> None:
        project_dir = Path("fake-project")
        completed = Mock(returncode=0)
        with patch("projectdevsetup.utils.venv_helper.subprocess.run", return_value=completed), patch(
            "projectdevsetup.utils.venv_helper._show_venv_instructions"
        ), patch.object(Path, "write_text") as write_text:
            self.assertTrue(venv_helper.create_venv(project_dir))
        write_text.assert_called_once()


if __name__ == "__main__":
    unittest.main()
