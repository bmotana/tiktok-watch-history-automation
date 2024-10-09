import subprocess
import os
import yaml
from typing import Dict, Any
import time
import logging

class VideoDownloader:
    """
    A class for downloading videos using yt-dlp.

    This class handles the configuration loading, link management, and video downloading
    process using the yt-dlp tool.

    Attributes:
        config (Dict[str, Any]): Configuration dictionary loaded from a YAML file.
        downloader_dir (str): Directory where the yt-dlp executable is located.
        sleep_duration (int): Duration to sleep between download attempts.
        link (str): The video link to be downloaded.
        logger (logging.Logger): Logger for the class.
    """

    def __init__(self, config_path: str):
        """
        Initialize the VideoDownloader with the given configuration file path.

        Args:
            config_path (str): Path to the YAML configuration file.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.config: Dict[str, Any] = self._load_config(config_path)
        self.downloader_dir: str = self.config['paths']['yt-dplt_dir']
        self.sleep_duration: int = self.config.get('sleep_duration', 4)
        self.link = None
        self.logger.info("VideoDownloader initialized")
        self.downloads_path = self.get_downloads_path()

    @staticmethod
    def get_downloads_path():
        home_directory = os.path.expanduser("~")
        downloads_folder = os.path.join(home_directory, "Downloads")
        return downloads_folder

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate the configuration dictionary.

        Args:
            config (Dict[str, Any]): Configuration dictionary to validate.

        Raises:
            ValueError: If a required configuration key is missing or empty.
        """
        required_keys = ['paths']
        for key in required_keys:
            if key not in config or not config[key]:
                raise ValueError(f"Missing or empty required configuration: {key}")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load and validate the configuration from a YAML file.

        Args:
            config_path (str): Path to the YAML configuration file.

        Returns:
            Dict[str, Any]: Loaded and validated configuration dictionary.
        """
        with open(config_path) as file:
            config = yaml.safe_load(file)
        self._validate_config(config)
        return config



    def get_link(self, link: str) -> None:
        """
        Set the video link to be downloaded.

        Args:
            link (str): The video link.
        """
        self.link = link

    def download_video(self) -> None:
        """
        Download the video using yt-dlp.

        This method constructs the yt-dlp command, executes it, and handles any errors
        that may occur during the download process.

        Raises:
            ValueError: If the link is not set before calling this method.
        """
        if self.link is None:
            raise ValueError("Link not set. Call get_link() first.")
        command: str = f"simple_ytdlp.bat {self.link} {self.downloads_path}"
        self.logger.info(f"Downloading video: {self.link}")
        try:
            subprocess.run(command, shell=True, cwd=self.downloader_dir, check=True)
            self.logger.info("Video downloaded successfully")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error downloading video: {e}")
        time.sleep(self.sleep_duration)


