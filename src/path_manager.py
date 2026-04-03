"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

import os
import platform
import subprocess
from pathlib import Path
from src.utils.logger import success, warning, info, error


def add_to_path(new_path: str, tool_name: str):
    """
    Add a directory to PATH permanently on all 3 OS.
    Falls back to showing manual instructions if automatic fails.
    """
    os_name = platform.system().lower()

    if os_name == "windows":
        _add_to_path_windows(new_path, tool_name)
    elif os_name in ("linux", "darwin"):
        _add_to_path_unix(new_path, tool_name)
    else:
        _show_manual_path_instructions(new_path, tool_name)


def _add_to_path_windows(new_path: str, tool_name: str):
    """Add to PATH permanently on Windows via registry."""
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
            new_value = current_path + ";" + new_path
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_value)
            winreg.CloseKey(key)
            success(
                f"{tool_name} added to PATH. "
                "Please restart your terminal for this to take effect."
            )
        else:
            success(f"{tool_name} is already in PATH.")
    except PermissionError:
        _show_manual_path_instructions_windows(new_path, tool_name)
    except ImportError:
        _show_manual_path_instructions_windows(new_path, tool_name)
    except Exception:
        _show_manual_path_instructions_windows(new_path, tool_name)


def _add_to_path_unix(new_path: str, tool_name: str):
    """Add to PATH permanently on Linux/Mac via shell profile."""
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

    written = False
    for profile in profiles:
        try:
            if profile.exists():
                content = profile.read_text()
                if new_path not in content:
                    with open(profile, "a") as f:
                        if "fish" in str(profile):
                            f.write(fish_line)
                        else:
                            f.write(export_line)
                    written = True
                    break
        except Exception:
            continue

    if not written:
        try:
            profile = home / ".profile"
            with open(profile, "a") as f:
                f.write(export_line)
            written = True
        except Exception:
            pass

    if written:
        success(
            f"{tool_name} added to PATH. "
            "Please restart your terminal for changes to take effect."
        )
    else:
        _show_manual_path_instructions(new_path, tool_name)


def _show_manual_path_instructions(new_path: str, tool_name: str):
    """Show plain English instructions for adding to PATH manually."""
    warning(
        f"Could not automatically add {tool_name} to PATH. Please follow these steps:"
    )
    print(
        f"\n  Add this line to your terminal config file "
        f"(~/.bashrc or ~/.zshrc):\n"
        f'\n  export PATH="{new_path}:$PATH"\n'
        f"\n  Then close and reopen your terminal.\n"
    )


def _show_manual_path_instructions_windows(new_path: str, tool_name: str):
    """Show plain English instructions for Windows PATH."""
    warning(f"Could not automatically add {tool_name} to PATH.")
    print(
        f"\n  How to add it manually on Windows:\n"
        f"  1. Press Windows key + S, search 'Environment Variables'\n"
        f"  2. Click 'Edit the system environment variables'\n"
        f"  3. Click 'Environment Variables' button\n"
        f"  4. Under 'System variables', find 'Path' and click 'Edit'\n"
        f"  5. Click 'New' and paste this:\n"
        f"     {new_path}\n"
        f"  6. Click OK on all windows\n"
        f"  7. Restart your terminal\n"
    )


def verify_in_path(command: str) -> bool:
    """Verify a command is accessible in PATH after installation."""
    try:
        result = subprocess.run(
            ["where", command]
            if platform.system() == "Windows"
            else ["which", command],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception:
        return False
