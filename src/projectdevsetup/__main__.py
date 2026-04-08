"""
Command-line entry point for projectdevsetup.
"""

from __future__ import annotations

import traceback

from projectdevsetup.network import get_temp_dir
from projectdevsetup.utils.logger import error
from projectdevsetup.wizard import run


def main() -> None:
    try:
        run()
    except KeyboardInterrupt:
        print()
        error("Setup cancelled by user. Run 'projectdevsetup' to start again.")
        raise SystemExit(0)
    except EOFError:
        error(
            "No interactive input was received. Run 'projectdevsetup' in an interactive terminal "
            "and follow the prompts."
        )
        raise SystemExit(1)
    except SystemExit:
        raise
    except Exception:
        _log_crash()
        error(
            "Something unexpected went wrong. Please report this issue at:\n"
            "  https://github.com/zenith-open-source/projectdevsetup/issues"
        )
        raise SystemExit(1)


def _log_crash() -> None:
    """Write the full traceback to a log file for debugging."""
    try:
        log_file = get_temp_dir() / "crash.log"
        with log_file.open("a", encoding="utf-8") as fh:
            fh.write("\n--- crash ---\n")
            traceback.print_exc(file=fh)
        error(f"Crash details saved to: {log_file}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
