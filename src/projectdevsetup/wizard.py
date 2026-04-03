"""
Interactive beginner-friendly setup flow.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from projectdevsetup.installer import Installer
from projectdevsetup.network import check_internet
from projectdevsetup.permissions import assert_not_root, check_admin_windows, check_disk_space
from projectdevsetup.utils.logger import ask, divider, header, info, success, warning, step
from projectdevsetup.utils.venv_helper import create_venv
from projectdevsetup.vscode import ensure_vscode_installed, install_extensions, open_in_vscode

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

PACKAGE_ROOT = Path(__file__).resolve().parent


def run() -> None:
    """Run the interactive setup wizard."""
    header()
    _preflight_checks()

    language_name, language_key = _select_language()
    file_name = _get_file_name(language_key)
    output_dir = _get_output_dir(file_name)

    divider()
    info(f"Setting up {language_name} environment...")
    divider()

    installer = Installer()
    total_steps = 4
    current_step = 1

    if language_key == "all":
        for _, (name, lang_key, _) in LANGUAGES.items():
            if lang_key == "all":
                continue
            step(current_step, total_steps, f"Installing {name}")
            installer.install_for_language(lang_key)
            current_step += 1
    else:
        step(current_step, total_steps, f"Installing {language_name} tools")
        installer.install_for_language(language_key)
        current_step += 1

    step(current_step, total_steps, "Setting up Visual Studio Code")
    vscode_ok = ensure_vscode_installed(installer.sys_info)
    current_step += 1

    step(current_step, total_steps, "Installing VS Code extensions")
    if vscode_ok:
        if language_key == "all":
            for _, (_, lang_key, _) in LANGUAGES.items():
                if lang_key != "all":
                    install_extensions(lang_key)
        else:
            install_extensions(language_key)
    current_step += 1

    step(current_step, total_steps, "Creating your starter file")
    created_files: list[Path] = []
    if language_key == "all":
        for _, (_, lang_key, _) in LANGUAGES.items():
            if lang_key == "all":
                continue
            created = _create_starter_file(lang_key, "hello", output_dir)
            if created is not None:
                created_files.append(created)
    else:
        created = _create_starter_file(language_key, file_name, output_dir)
        if created is not None:
            created_files.append(created)

    if language_key in ("python", "all"):
        create_venv(output_dir)

    if vscode_ok and created_files:
        open_in_vscode(created_files[0])

    divider()
    success("Everything is set up. Happy coding!")
    success(f"Your files are in: {output_dir}")
    print(
        "\n  Made with love by Zenith Open Source Projects\n"
        "  https://zenithopensourceprojects.vercel.app\n"
    )


def _preflight_checks() -> None:
    info("Running checks before we start...")
    info("Checking internet connection...")
    if not check_internet():
        _print_no_internet_and_exit()

    success("Internet connection OK.")
    if not check_disk_space(required_gb=2.0):
        raise SystemExit(1)

    assert_not_root()

    if sys.platform.startswith("win"):
        if not check_admin_windows():
            warning(
                "You are not running as administrator. Some installations may fail. "
                "If needed, restart as administrator."
            )
        else:
            success("Administrator rights detected.")

    success("All checks passed. Starting setup...")
    divider()


def _print_no_internet_and_exit() -> None:
    from projectdevsetup.utils.logger import error

    error("No internet connection detected. Please connect to the internet and run this again.")
    raise SystemExit(1)


def _select_language() -> tuple[str, str]:
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
        warning("Please enter a number between 1 and 9.")


def _get_file_name(language_key: str) -> str:
    if language_key == "all":
        return "hello"

    lang_ext = next(ext for _, (_, key, ext) in LANGUAGES.items() if key == language_key)
    print()
    info("What do you want to name your file? (without extension)")
    info(f"Example: if you type 'hello', your file will be 'hello{lang_ext}'")
    print()

    while True:
        name = ask("File name:").strip()
        if not name:
            warning("Please enter a file name.")
            continue

        clean = re.sub(r"[^\w\-]", "_", name)
        if clean != name:
            warning(f"Special characters removed. Your file will be named: {clean}{lang_ext}")
        if clean:
            return clean
        warning("Please enter a valid file name.")


def _get_output_dir(file_name: str) -> Path:
    output = Path.home() / "projectdevsetup_projects" / file_name
    output.mkdir(parents=True, exist_ok=True)
    return output


def _create_starter_file(language_key: str, file_name: str, output_dir: Path) -> Path | None:
    template_name = TEMPLATE_MAP.get(language_key)
    if template_name is None:
        return None

    suffix = Path(template_name).suffix
    if language_key == "java":
        class_name = "".join(part.capitalize() for part in file_name.split("_")) or "Hello"
        out_file = output_dir / f"{class_name}{suffix}"
        out_file.write_text(
            "// Hello, World! - Java\n"
            "// projectdevsetup by Zenith Open Source Projects\n\n"
            f"public class {class_name} {{\n"
            "    public static void main(String[] args) {\n"
            '        System.out.println("Hello, World!");\n'
            "    }\n"
            "}\n",
            encoding="utf-8",
        )
        success(f"Created: {out_file}")
        return out_file

    out_file = output_dir / f"{file_name}{suffix}"
    template_path = PACKAGE_ROOT / "templates" / template_name
    out_file.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")
    success(f"Created: {out_file}")
    return out_file
