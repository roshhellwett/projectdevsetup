"""
@project  projectdevsetup
@org      Zenith Open Source Projects
@license  MIT License
"""

import urllib.request
import urllib.error
import os
import tempfile
from pathlib import Path
from projectdevsetup.utils.logger import info, error, warning


def check_internet() -> bool:
    """
    Check if internet is available.
    Tries to reach multiple hosts in case one is down.
    """
    hosts = [
        "https://www.google.com",
        "https://www.cloudflare.com",
        "https://www.microsoft.com",
    ]
    for host in hosts:
        try:
            urllib.request.urlopen(host, timeout=5)
            return True
        except Exception:
            continue
    return False


def download_file(
    url: str, destination: Path, description: str, retries: int = 3
) -> bool:
    """
    Download a file with retry logic and progress indication.
    Returns True on success, False on failure.
    Shows beginner-friendly messages throughout.
    """
    for attempt in range(1, retries + 1):
        try:
            info(f"Downloading {description}... (attempt {attempt}/{retries})")

            def progress_hook(count, block_size, total_size):
                if total_size > 0:
                    percent = min(int(count * block_size * 100 / total_size), 100)
                    print(f"\r  Progress: {percent}%   ", end="", flush=True)

            urllib.request.urlretrieve(url, str(destination), reporthook=progress_hook)
            print()
            return True

        except urllib.error.URLError:
            warning(
                f"Download attempt {attempt} failed. "
                f"Checking your internet connection..."
            )
            if not check_internet():
                error(
                    "No internet connection detected. "
                    "Please connect to the internet and try again."
                )
                return False
        except Exception as e:
            warning(f"Download attempt {attempt} failed. Retrying...")

    error(
        f"Could not download {description} after {retries} attempts. "
        "Please check your internet connection and try again."
    )
    return False


def get_temp_dir() -> Path:
    """Return a safe temp directory for downloads."""
    tmp = Path(tempfile.gettempdir()) / "projectdevsetup"
    tmp.mkdir(parents=True, exist_ok=True)
    return tmp
