"""
Network helpers for downloads and connectivity checks.
"""

from __future__ import annotations

import tempfile
import urllib.error
import urllib.request
from pathlib import Path

from projectdevsetup.utils.logger import error, info, warning


def check_internet() -> bool:
    """Return True when at least one well-known host is reachable."""
    for host in (
        "https://www.google.com",
        "https://www.cloudflare.com",
        "https://www.microsoft.com",
    ):
        try:
            urllib.request.urlopen(host, timeout=5)
            return True
        except Exception:
            continue
    return False


def download_file(
    url: str, destination: Path, description: str, retries: int = 3
) -> bool:
    """Download a file with simple retry logic and progress output."""
    destination.parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, retries + 1):
        try:
            info(f"Downloading {description}... (attempt {attempt}/{retries})")

            def progress_hook(count: int, block_size: int, total_size: int) -> None:
                if total_size <= 0:
                    return
                percent = min(int(count * block_size * 100 / total_size), 100)
                print(f"\r  Progress: {percent}%   ", end="", flush=True)

            urllib.request.urlretrieve(url, str(destination), reporthook=progress_hook)
            print()
            return True
        except urllib.error.URLError:
            warning(
                f"Download attempt {attempt} failed. Checking your internet connection..."
            )
            if not check_internet():
                error(
                    "No internet connection detected. Please connect to the internet and try again."
                )
                return False
        except Exception:
            warning(f"Download attempt {attempt} failed. Retrying...")

    error(
        f"Could not download {description} after {retries} attempts. "
        "Please check your internet connection and try again."
    )
    return False


def get_temp_dir() -> Path:
    """Return a stable temp directory used by the installer."""
    tmp = Path(tempfile.gettempdir()) / "projectdevsetup"
    tmp.mkdir(parents=True, exist_ok=True)
    return tmp
