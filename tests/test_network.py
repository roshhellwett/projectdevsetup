from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from projectdevsetup import network


class CheckInternetTests(unittest.TestCase):
    def test_returns_true_when_first_host_reachable(self) -> None:
        with patch("projectdevsetup.network.urllib.request.urlopen") as urlopen:
            urlopen.return_value = MagicMock()
            self.assertTrue(network.check_internet())
        urlopen.assert_called_once()

    def test_returns_true_when_second_host_reachable(self) -> None:
        side_effects = [ConnectionError, MagicMock()]
        with patch("projectdevsetup.network.urllib.request.urlopen", side_effect=side_effects):
            self.assertTrue(network.check_internet())

    def test_returns_false_when_all_hosts_fail(self) -> None:
        with patch("projectdevsetup.network.urllib.request.urlopen", side_effect=ConnectionError):
            self.assertFalse(network.check_internet())


class DownloadFileTests(unittest.TestCase):
    def test_successful_download_returns_true(self) -> None:
        with patch("projectdevsetup.network.urllib.request.urlretrieve"), \
             patch("projectdevsetup.network.socket.getdefaulttimeout", return_value=None), \
             patch("projectdevsetup.network.socket.setdefaulttimeout"):
            result = network.download_file(
                "https://example.com/file.exe",
                Path("/tmp/test/file.exe"),
                "Test File",
            )
        self.assertTrue(result)

    def test_retries_on_failure(self) -> None:
        import urllib.error

        with patch(
            "projectdevsetup.network.urllib.request.urlretrieve",
            side_effect=[urllib.error.URLError("fail"), None],
        ), patch("projectdevsetup.network.check_internet", return_value=True), \
           patch("projectdevsetup.network.socket.getdefaulttimeout", return_value=None), \
           patch("projectdevsetup.network.socket.setdefaulttimeout"):
            result = network.download_file(
                "https://example.com/file.exe",
                Path("/tmp/test/file.exe"),
                "Test File",
                retries=2,
            )
        self.assertTrue(result)

    def test_returns_false_after_all_retries_fail(self) -> None:
        with patch(
            "projectdevsetup.network.urllib.request.urlretrieve",
            side_effect=Exception("fail"),
        ), patch("projectdevsetup.network.socket.getdefaulttimeout", return_value=None), \
           patch("projectdevsetup.network.socket.setdefaulttimeout"):
            result = network.download_file(
                "https://example.com/file.exe",
                Path("/tmp/test/file.exe"),
                "Test File",
                retries=2,
            )
        self.assertFalse(result)

    def test_returns_false_on_no_internet_during_retry(self) -> None:
        import urllib.error

        with patch(
            "projectdevsetup.network.urllib.request.urlretrieve",
            side_effect=urllib.error.URLError("fail"),
        ), patch("projectdevsetup.network.check_internet", return_value=False), \
           patch("projectdevsetup.network.socket.getdefaulttimeout", return_value=None), \
           patch("projectdevsetup.network.socket.setdefaulttimeout"):
            result = network.download_file(
                "https://example.com/file.exe",
                Path("/tmp/test/file.exe"),
                "Test File",
            )
        self.assertFalse(result)

    def test_keyboard_interrupt_is_reraised(self) -> None:
        with patch(
            "projectdevsetup.network.urllib.request.urlretrieve",
            side_effect=KeyboardInterrupt,
        ), patch("projectdevsetup.network.socket.getdefaulttimeout", return_value=None), \
           patch("projectdevsetup.network.socket.setdefaulttimeout"):
            with self.assertRaises(KeyboardInterrupt):
                network.download_file(
                    "https://example.com/file.exe",
                    Path("/tmp/test/file.exe"),
                    "Test File",
                )


class GetTempDirTests(unittest.TestCase):
    def test_returns_path_ending_with_projectdevsetup(self) -> None:
        tmp = network.get_temp_dir()
        self.assertEqual(tmp.name, "projectdevsetup")
        self.assertTrue(tmp.exists())


if __name__ == "__main__":
    unittest.main()
