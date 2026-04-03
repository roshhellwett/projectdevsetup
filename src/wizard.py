"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

import re
import sys
from pathlib import Path
from src.utils.logger import (
    header,
    info,
    success,
    error,
    warning,
    divider,
    step,
    ask,
)
from src.utils.os_detect import detect_system
from src.network import check_internet
from src.permissions import (
    check_disk_space,
    assert_not_root,
    handle_no_admin_windows,
)
from src.detector import get_installed_summary
from src.installer import Installer
from src.vscode import (
    ensure_vscode_installed,
    install_extensions,
    open_in_vscode,
)
from src.utils.venv_helper import create_venv

LANGUAGES = {
    "1": ("Python", "python", ".py"),
    "2": ("C", "c", ".c"),
    "3": ("C++", "cpp", ".cpp"),
    "4": ("Java", "java", ".java"),
    "5": ("HTML / CSS", "html", ".html"),
    "6": ("JavaScript", "javascript", ".js"),
    "7": ("Rust", "rust", ".rs"),
    "8": ("Go", "go", ".go"),
    "9": ("All Languages", "all", ""),
}

TEMPLATE_MAP = {
    "python": "hello.py",
    "c": "hello.c",
    "cpp": "hello.cpp",
    "java": "Hello.java",
    "html": "hello.html",
    "javascript": "hello.js",
    "rust": "hello.rs",
    "go": "hello.go",
}


def run():
    """Main entry point for the wizard."""
    header()

    _preflight_checks()

    language_name, language_key = _select_language()

    file_name = _get_file_name(language_key)

    output_dir = _get_output_dir(file_name)

    divider()
    info(f"Setting up {language_name} environment...")
    divider()

    installer = Installer()
    sys_info = installer.sys_info

    total_steps = 4
    current_step = 1

    if language_key == "all":
        for key, (name, lang_key, _) in LANGUAGES.items():
            if lang_key != "all":
                step(current_step, total_steps, f"Installing {name}")
                installer.install_for_language(lang_key)
                current_step += 1
    else:
        step(current_step, total_steps, f"Installing {language_name} tools")
        installer.install_for_language(language_key)
        current_step += 1

    step(current_step, total_steps, "Setting up Visual Studio Code")
    vscode_ok = ensure_vscode_installed(sys_info)
    current_step += 1

    step(current_step, total_steps, "Installing VSCode extensions")
    if vscode_ok:
        if language_key == "all":
            for key, (name, lang_key, _) in LANGUAGES.items():
                if lang_key != "all":
                    install_extensions(lang_key)
        else:
            install_extensions(language_key)
    current_step += 1

    step(current_step, total_steps, "Creating your starter file")
    created_files = []
    if language_key == "all":
        for key, (name, lang_key, ext) in LANGUAGES.items():
            if lang_key != "all":
                f = _create_starter_file(lang_key, "hello", output_dir)
                if f:
                    created_files.append(f)
    else:
        f = _create_starter_file(language_key, file_name, output_dir)
        if f:
            created_files.append(f)

    if language_key in ("python", "all"):
        create_venv(output_dir)

    if vscode_ok and created_files:
        open_in_vscode(created_files[0])

    divider()
    success("Everything is set up! Happy coding!")
    success(f"Your files are in: {output_dir}")
    print(
        f"\n  Made with love by Zenith Open Source Projects\n"
        f"  https://zenithopensourceprojects.vercel.app\n"
    )


def _preflight_checks():
    """Run all pre-flight checks before doing anything."""
    info("Running checks before we start...")

    info("Checking internet connection...")
    if not check_internet():
        error(
            "No internet connection detected. "
            "Please connect to the internet and run this again."
        )
        sys.exit(1)
    success("Internet connection OK.")

    if not check_disk_space(required_gb=2.0):
        sys.exit(1)

    assert_not_root()

    import platform

    if platform.system() == "Windows":
        from src.permissions import check_admin_windows

        if not check_admin_windows():
            warning(
                "You are not running as administrator. "
                "Some installations may fail. "
                "If needed, restart as administrator."
            )
        else:
            success("Administrator rights detected.")

    success("All checks passed. Starting setup...")
    divider()


def _select_language() -> tuple:
    """Show language menu and get user selection."""
    print("  Which programming language do you want to set up?\n")
    for num, (name, _, _) in LANGUAGES.items():
        print(f"  {num}. {name}")
    print()

    while True:
        choice = ask("Enter a number (1-9):").strip()
        if choice in LANGUAGES:
            name, key, _ = LANGUAGES[choice]
            success(f"You selected: {name}")
            return name, key
        else:
            warning("Please enter a number between 1 and 9.")


def _get_file_name(language_key: str) -> str:
    """Ask the user for their starter file name."""
    if language_key == "all":
        return "hello"

    lang_ext = ""
    for num, (name, key, ext) in LANGUAGES.items():
        if key == language_key:
            lang_ext = ext
            break

    print()
    info(f"What do you want to name your file? (without extension)")
    info(f"Example: if you type 'hello', your file will be 'hello{lang_ext}'")
    print()

    while True:
        name = ask("File name:").strip()
        if not name:
            warning("Please enter a file name.")
            continue
        clean = re.sub(r"[^\w\-]", "_", name)
        if clean != name:
            warning(
                f"Special characters removed. "
                f"Your file will be named: {clean}{lang_ext}"
            )
        if clean:
            return clean
        warning("Please enter a valid file name.")


def _get_output_dir(file_name: str) -> Path:
    """Create and return the output directory for the project."""
    output = Path.home() / "projectdevsetup_projects" / file_name
    output.mkdir(parents=True, exist_ok=True)
    return output


def _create_starter_file(
    language_key: str, file_name: str, output_dir: Path
) -> Path | None:
    """
    Copy the correct template to the output directory
    with the user's chosen file name.
    """
    template_name = TEMPLATE_MAP.get(language_key)
    if not template_name:
        return None

    suffix = Path(template_name).suffix

    if language_key == "java":
        class_name = file_name.capitalize()
        out_file = output_dir / f"{class_name}{suffix}"
        template_content = (
            f"// Hello, World! — Java\n"
            f"// projectdevsetup by Zenith Open Source Projects\n\n"
            f"public class {class_name} {{\n"
            f"    public static void main(String[] args) {{\n"
            f'        System.out.println("Hello, World!");\n'
            f"    }}\n"
            f"}}\n"
        )
        out_file.write_text(template_content)
    else:
        out_file = output_dir / f"{file_name}{suffix}"
        try:
            template_path = Path(__file__).parent / "templates" / template_name
            out_file.write_text(template_path.read_text())
        except Exception:
            out_file.write_text(f"// Your {language_key} starter file\n")

    success(f"Created: {out_file}")
    return out_file
