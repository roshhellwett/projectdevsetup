"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

import subprocess
import platform
from pathlib import Path
from projectdevsetup.utils.logger import info, success, warning, error


def create_venv(project_dir: Path) -> bool:
    """
    Create a Python virtual environment inside the project directory.
    Shows beginner-friendly instructions on how to use it.
    Returns True on success.
    """
    venv_path = project_dir / ".venv"

    if venv_path.exists():
        success("Virtual environment already exists. Skipping.")
        _show_venv_instructions(venv_path)
        return True

    info("Creating Python virtual environment (.venv)...")
    try:
        result = subprocess.run(
            ["python3", "-m", "venv", str(venv_path)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            result = subprocess.run(
                ["python", "-m", "venv", str(venv_path)],
                capture_output=True,
                text=True,
                timeout=60,
            )
        if result.returncode == 0:
            success("Virtual environment created!")
            _create_requirements_txt(project_dir)
            _show_venv_instructions(venv_path)
            return True
        else:
            error(
                "Could not create virtual environment. "
                "Make sure Python is properly installed."
            )
            return False
    except Exception:
        error(
            "Failed to create virtual environment. "
            "Please make sure python3-venv is installed."
        )
        return False


def _create_requirements_txt(project_dir: Path):
    """Create an empty requirements.txt with instructions."""
    req_file = project_dir / "requirements.txt"
    if not req_file.exists():
        req_file.write_text(
            "# Add your Python packages here, one per line.\n"
            "# Example:\n"
            "# requests\n"
            "# numpy\n"
            "#\n"
            "# To install all packages, run:\n"
            "# pip install -r requirements.txt\n"
        )
        success("requirements.txt created.")


def _show_venv_instructions(venv_path: Path):
    """Show beginner-friendly venv activation instructions."""
    os_name = platform.system().lower()

    if os_name == "windows":
        activate_cmd = f".venv\\Scripts\\activate"
    else:
        activate_cmd = "source .venv/bin/activate"

    print(f"""
  ┌─────────────────────────────────────────────┐
  │  How to use your virtual environment:       │
  │                                             │
  │  1. Open your terminal in this folder      │
  │  2. Type: {activate_cmd:<35} │
  │  3. You will see (.venv) appear             │
  │  4. Install packages: pip install <name>   │
  │  5. To deactivate: type deactivate          │
  └─────────────────────────────────────────────┘
""")
