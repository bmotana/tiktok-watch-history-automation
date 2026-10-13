import unittest
from unittest.mock import Mock, patch

from scripts.link_processing import LinkProcessor, TikTokURLProcessingError


class TestLinkProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = LinkProcessor()

    @patch("scripts.link_processing.requests.head")
    def test_rejects_non_tiktok_clipboard_value_without_request(self, head):
        with self.assertRaisesRegex(TikTokURLProcessingError, r"not an HTTP\(S\) TikTok URL"):
            self.processor.get_link("https://example.com/@user/video/123")

        head.assert_not_called()

    @patch("scripts.link_processing.requests.head")
    def test_rejects_hostname_that_only_ends_with_tiktok_domain(self, head):
        with self.assertRaises(TikTokURLProcessingError):
            self.processor.get_link("https://not-tiktok.com/@user/video/123")

        head.assert_not_called()

    @patch("scripts.link_processing.requests.head")
    def test_accepts_tiktok_short_link_and_resolves_video(self, head):
        response = Mock()
        response.url = "https://www.tiktok.com/@creator/video/123456"
        head.return_value = response

        self.processor.get_link("https://vm.tiktok.com/abc123/")

        head.assert_called_once_with(
            "https://vm.tiktok.com/abc123/", allow_redirects=True, timeout=10
        )
        self.assertTrue(self.processor.is_valid_tiktok_url())
        self.assertEqual(self.processor.get_content_type(), "video")

    @patch("scripts.link_processing.requests.head")
    def test_identifies_resolved_photo_url(self, head):
        response = Mock()
        response.url = "https://www.tiktok.com/@creator/photo/987654"
        head.return_value = response

        self.processor.get_link("https://www.tiktok.com/@creator/photo/987654")

        self.assertEqual(self.processor.get_content_type(), "photo")

    @patch("scripts.link_processing.requests.head")
    def test_rejects_short_link_that_resolves_outside_tiktok(self, head):
        response = Mock()
        response.url = "https://example.com/@creator/video/123456"
        head.return_value = response

        self.processor.get_link("https://vm.tiktok.com/abc123/")

        self.assertFalse(self.processor.is_valid_tiktok_url())
        self.assertIsNone(self.processor.get_content_type())

    @patch("scripts.link_processing.requests.head")
    def test_rejects_tiktok_url_with_unsupported_content_path(self, head):
        response = Mock()
        response.url = "https://www.tiktok.com/@creator/live/123456"
        head.return_value = response

        self.processor.get_link("https://www.tiktok.com/@creator/live/123456")

        self.assertFalse(self.processor.is_valid_tiktok_url())
        self.assertIsNone(self.processor.get_content_type())


if __name__ == "__main__":
    unittest.main()
