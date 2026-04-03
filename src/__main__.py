"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

import sys
from src.wizard import run
from src.utils.logger import error


def main():
    try:
        run()
    except KeyboardInterrupt:
        print("\n")
        error(
            "Setup cancelled by user. Run 'python -m projectdevsetup' to start again."
        )
        sys.exit(0)
    except Exception as e:
        error(
            "Something unexpected went wrong. "
            "Please report this issue at:\n"
            "  https://github.com/zenith-open-source/projectdevsetup/issues"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
