from typing import Optional
import re
import requests
from urllib.parse import urlparse
import logging
from dataclasses import dataclass
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TikTokURLPatterns:
    """Constants for TikTok URL validation patterns."""
    DOMAIN = 'tiktok.com'
    FULL_URL = r'https?:\/\/((?:www\.)?tiktok\.com\/@[\w.-]+\/(video|photo)\/\d+)'
    CONTENT_TYPE = r'/(video|photo)/'


class TikTokURLProcessingError(Exception):
    """Custom exception for TikTok URL processing errors."""
    pass


class LinkProcessor:
    """
    A class to process and validate TikTok URLs.

    This class provides functionality to validate TikTok URLs and determine
    their content type (photo or video).

    Attributes:
        original_link (str): The original TikTok URL provided.
        resolved_link (str): The resolved URL after handling any redirects.
    """

    def __init__(self) -> None:
        """
        Initialize the LinkProcessor with a TikTok URL.

        Args:
            link (str): The TikTok URL to process.

        Raises:
            ValueError: If the provided link is empty or not a string.
            TikTokURLProcessingError: If there's an error resolving the URL.
        """
        self.original_link = None
        self.resolved_link = None


    def get_link(self, link: str) -> None:
        """
        Set the video link to be downloaded.

        Args:
            link (str): The video link.
        """
        if not isinstance(link, str) or not link.strip():
            logger.error("Invalid link provided: link must be a non-empty string")
            raise ValueError("Link must be a non-empty string")

        self.original_link = link.strip()
        try:
            self.resolved_link = self._resolve_shortlink()
            logger.info(f"Successfully resolved URL")
        except RequestException as e:
            logger.error(f"Failed to resolve URL: {str(e)}")
            raise TikTokURLProcessingError(f"Failed to resolve URL: {str(e)}")

    def _resolve_shortlink(self) -> str:
        """
        Resolve a shortened URL to its full form.

        Returns:
            str: The resolved URL.

        Raises:
            RequestException: If there's an error resolving the URL.
        """
        try:
            response = requests.head(
                self.original_link,
                allow_redirects=True,
                timeout=10
            )
            response.raise_for_status()
            return response.url
        except RequestException as e:
            logger.error(f"Error resolving shortlink: {str(e)}")
            raise

    def is_valid_tiktok_url(self) -> bool:
        """
        Check if the provided URL is a valid TikTok URL.

        Returns:
            bool: True if the URL is a valid TikTok URL, False otherwise.
        """
        try:
            parsed = urlparse(self.resolved_link)

            if not parsed.netloc.endswith(TikTokURLPatterns.DOMAIN):
                logger.debug(f"Invalid domain: {parsed.netloc}")
                return False

            is_valid = bool(re.match(TikTokURLPatterns.FULL_URL, self.resolved_link))
            if not is_valid:
                logger.debug(f"URL doesn't match TikTok pattern: {self.resolved_link}")

            return is_valid

        except Exception as e:
            logger.error(f"Error validating URL: {str(e)}")
            return False

    def get_content_type(self) -> Optional[str]:
        """
        Determine whether the TikTok URL is for a photo or video.

        Returns:
            Optional[str]: 'photo' or 'video' if the URL is valid, None if invalid.

        Note:
            Returns None if the URL is invalid or if content type cannot be determined.
        """
        if not self.is_valid_tiktok_url():
            logger.warning(f"Attempting to get content type for invalid URL: {self.resolved_link}")
            return None

        try:
            match = re.search(TikTokURLPatterns.CONTENT_TYPE, self.resolved_link)

            if not match:
                logger.debug(f"Could not determine content type for URL: {self.resolved_link}")
                return None

            content_type = match.group(1)
            logger.info(f"Content type determined: {content_type}")
            return content_type

        except Exception as e:
            logger.error(f"Error determining content type: {str(e)}")
            return None