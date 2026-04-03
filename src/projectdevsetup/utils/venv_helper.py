"""
Virtual environment helpers.
"""

from __future__ import annotations

import platform
import subprocess
from pathlib import Path

from projectdevsetup.utils.logger import error, info, success


def create_venv(project_dir: Path) -> bool:
    """Create a Python virtual environment inside the project directory."""
    venv_path = project_dir / ".venv"
    if venv_path.exists():
        success("Virtual environment already exists. Skipping.")
        _show_venv_instructions()
        return True

    info("Creating Python virtual environment (.venv)...")
    for python_cmd in ("python3", "python"):
        try:
            result = subprocess.run(
                [python_cmd, "-m", "venv", str(venv_path)],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
        except Exception:
            continue

        if result.returncode == 0:
            success("Virtual environment created!")
            _create_requirements_txt(project_dir)
            _show_venv_instructions()
            return True

    error("Could not create a virtual environment. Make sure Python and venv support are installed.")
    return False


def _create_requirements_txt(project_dir: Path) -> None:
    req_file = project_dir / "requirements.txt"
    if req_file.exists():
        return
    req_file.write_text(
        "# Add your Python packages here, one per line.\n"
        "# Example:\n"
        "# requests\n"
        "# numpy\n"
        "#\n"
        "# To install all packages, run:\n"
        "# pip install -r requirements.txt\n",
        encoding="utf-8",
    )
    success("requirements.txt created.")


def _show_venv_instructions() -> None:
    activate_cmd = ".venv\\Scripts\\activate" if platform.system().lower() == "windows" else "source .venv/bin/activate"
    print(
        "\n  +---------------------------------------------+\n"
        "  | How to use your virtual environment:        |\n"
        "  |                                             |\n"
        "  | 1. Open your terminal in this folder        |\n"
        f"  | 2. Type: {activate_cmd:<33}|\n"
        "  | 3. You will see (.venv) appear              |\n"
        "  | 4. Install packages: pip install <name>     |\n"
        "  | 5. To deactivate: type deactivate           |\n"
        "  +---------------------------------------------+\n"
    )
