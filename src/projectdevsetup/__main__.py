"""
Command-line entry point for projectdevsetup.
"""

from __future__ import annotations

from projectdevsetup.utils.logger import error
from projectdevsetup.wizard import run


def main() -> None:
    try:
        run()
    except KeyboardInterrupt:
        print()
        error("Setup cancelled by user. Run 'projectdevsetup' to start again.")
        raise SystemExit(0)
    except SystemExit:
        raise
    except Exception:
        error(
            "Something unexpected went wrong. Please report this issue at:\n"
            "  https://github.com/zenith-open-source/projectdevsetup/issues"
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
