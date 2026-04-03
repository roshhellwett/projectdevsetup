"""
PATH management helpers.
"""

from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path

from projectdevsetup.utils.logger import success, warning


def add_to_path(new_path: str, tool_name: str) -> None:
    """Attempt to persistently add a tool directory to PATH."""
    os_name = platform.system().lower()
    if os_name == "windows":
        _add_to_path_windows(new_path, tool_name)
    elif os_name in ("linux", "darwin"):
        _add_to_path_unix(new_path, tool_name)
    else:
        _show_manual_path_instructions(new_path, tool_name)


def _add_to_path_windows(new_path: str, tool_name: str) -> None:
    try:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            0,
            winreg.KEY_ALL_ACCESS,
        )
        current_path, _ = winreg.QueryValueEx(key, "Path")
        if new_path.lower() not in current_path.lower():
            winreg.SetValueEx(
                key,
                "Path",
                0,
                winreg.REG_EXPAND_SZ,
                current_path + ";" + new_path,
            )
        winreg.CloseKey(key)
        success(
            f"{tool_name} added to PATH. Please restart your terminal for this to take effect."
        )
    except Exception:
        _show_manual_path_instructions_windows(new_path, tool_name)


def _add_to_path_unix(new_path: str, tool_name: str) -> None:
    home = Path.home()
    shell = os.environ.get("SHELL", "")
    if "zsh" in shell:
        profiles = [home / ".zshrc", home / ".zprofile"]
    elif "fish" in shell:
        profiles = [home / ".config" / "fish" / "config.fish"]
    else:
        profiles = [home / ".bashrc", home / ".bash_profile", home / ".profile"]

    export_line = f'\nexport PATH="{new_path}:$PATH"\n'
    fish_line = f'\nset -gx PATH "{new_path}" $PATH\n'

    for profile in profiles:
        try:
            if profile.exists():
                content = profile.read_text(encoding="utf-8")
                if new_path in content:
                    success(
                        f"{tool_name} is already configured in PATH. Restart your terminal if needed."
                    )
                    return
            else:
                profile.parent.mkdir(parents=True, exist_ok=True)

            with profile.open("a", encoding="utf-8") as file_obj:
                file_obj.write(fish_line if "fish" in str(profile) else export_line)
            success(
                f"{tool_name} added to PATH. Please restart your terminal for changes to take effect."
            )
            return
        except Exception:
            continue

    _show_manual_path_instructions(new_path, tool_name)


def _show_manual_path_instructions(new_path: str, tool_name: str) -> None:
    warning(f"Could not automatically add {tool_name} to PATH. Please follow these steps:")
    print(
        "\n  Add this line to your terminal config file (~/.bashrc or ~/.zshrc):\n"
        f'\n  export PATH="{new_path}:$PATH"\n'
        "\n  Then close and reopen your terminal.\n"
    )


def _show_manual_path_instructions_windows(new_path: str, tool_name: str) -> None:
    warning(f"Could not automatically add {tool_name} to PATH.")
    print(
        "\n  How to add it manually on Windows:\n"
        "  1. Press Windows key + S, search 'Environment Variables'\n"
        "  2. Click 'Edit the system environment variables'\n"
        "  3. Click 'Environment Variables' button\n"
        "  4. Under 'System variables', find 'Path' and click 'Edit'\n"
        "  5. Click 'New' and paste this:\n"
        f"     {new_path}\n"
        "  6. Click OK on all windows\n"
        "  7. Restart your terminal\n"
    )


def verify_in_path(command: str) -> bool:
    """Verify a command is discoverable on PATH."""
    try:
        result = subprocess.run(
            ["where", command] if platform.system() == "Windows" else ["which", command],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception:
        return False
    return result.returncode == 0
