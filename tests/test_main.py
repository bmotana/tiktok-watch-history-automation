import unittest
from unittest.mock import Mock, patch

from main import extract_link_and_next
from scripts.link_processing import LinkProcessor


class TestExtractLinkAndNext(unittest.TestCase):
    @patch("main.time.sleep")
    @patch("main.pyperclip.paste", return_value="https://example.com/not-a-tiktok-link")
    @patch("scripts.link_processing.requests.head")
    def test_skips_invalid_clipboard_url_and_advances_history(
        self, head, paste, sleep
    ):
        controller = Mock()
        video_downloader = Mock()
        link_processor = LinkProcessor()

        extract_link_and_next(controller, video_downloader, link_processor)

        head.assert_not_called()
        video_downloader.get_link.assert_not_called()
        video_downloader.download_video.assert_not_called()
        controller.swipe_up.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
