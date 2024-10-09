import subprocess
import yaml
from typing import Dict, Any
import time
class AndroidController:
    """
    A class for controlling Android devices using ADB commands.
    """

    # Coordinate constants
    PROFILE_COORDS = (630, 1585)
    OPTIONS_COORDS = (630, 135)
    SETTINGS_PRIVACY_COORDS = (530, 1485)
    ACC_ACTIVITY_COORDS = (377, 1393)
    WATCH_HISTORY_COORDS = (385, 1050)
    WATCH_VIDEO_COORDS = (133, 584)
    SWIPE_UP_START = (350, 1200)
    SWIPE_UP_END = (350, 600)
    TIKTOK_APP_PACKAGE = "com.zhiliaoapp.musically"

    def __init__(self,  config_path: str):
        """
        Initialize the AndroidController.

        Args:
            config_path (str): The directory path where ADB is located.
        """
        self.config: Dict[str, Any] = self._load_config(config_path)
        self.app_dir: str = self.config['paths']['app_dir']


    @staticmethod
    def _load_config(config_path: str) -> Dict[str, Any]:
        """
        Load the YAML configuration file.

        Args:
            config_path (str): The path to the YAML configuration file.

        Returns:
            Dict[str, Any]: The loaded configuration as a dictionary.
        """
        with open(config_path) as file:
            return yaml.safe_load(file)

    def _run_command(self, command: str) -> None:
        """
        Run an ADB command.

        Args:
            command (str): The ADB command to run.
        """
        try:
            subprocess.run(command, shell=True, cwd=self.app_dir, check=True)
            time.sleep(1)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    def _click(self, x: int, y: int) -> None:
        if not (0 <= x <= 720 and 0 <= y <= 1600):  # Example screen size
            raise ValueError(f"Invalid coordinates: ({x}, {y})")
        command: str = f"adb shell input tap {x} {y}"
        self._run_command(command)


    def click(self, x: int, y: int) -> None:
        if not (0 <= x <= 720 and 0 <= y <= 1600):  # Example screen size
            raise ValueError(f"Invalid coordinates: ({x}, {y})")
        command: str = f"adb shell input tap {x} {y}"
        self._run_command(command)
    def press_and_hold(self, x: int, y: int, duration_ms: int) -> None:
        """
        Simulate a press and hold action at the specified coordinates.

        Args:
            x (int): The x-coordinate of the touch point.
            y (int): The y-coordinate of the touch point.
            duration_ms (int): The duration of the press in milliseconds.
        """
        command: str = f"adb shell input swipe {x} {y} {x} {y} {duration_ms}"
        self._run_command(command)


    def open_tiktok(self) -> None:
        """
        Open the TikTok app.
        """
        command: str = f"adb shell monkey -p {self.TIKTOK_APP_PACKAGE} -c android.intent.category.LAUNCHER 1 > NUL 2>&1 "
        self._run_command(command)

    def close_tiktok(self) -> None:
        """
        Open the TikTok app.
        """
        command: str = f"adb shell am force-stop {self.TIKTOK_APP_PACKAGE}"
        self._run_command(command)

    def swipe_up(self) -> None:
        """
        Simulate a swipe up action.
        """
        command: str = f"adb shell input swipe {self.SWIPE_UP_START[0]} {self.SWIPE_UP_START[1]} {self.SWIPE_UP_END[0]} {self.SWIPE_UP_END[1]} 100"
        self._run_command(command)

    def click_on_profile(self) -> None:
        """
        Click on the profile icon.
        """
        self._click(*self.PROFILE_COORDS)

    def click_on_options(self) -> None:
        """
        Click on the options menu.
        """
        self._click(*self.OPTIONS_COORDS)

    def click_on_settings_privacy(self) -> None:
        """
        Click on the settings and privacy option.
        """
        self._click(*self.SETTINGS_PRIVACY_COORDS)

    def click_on_acc_activity(self) -> None:
        """
        Click on the account activity option.
        """
        self._click(*self.ACC_ACTIVITY_COORDS)

    def click_on_watch_history(self) -> None:
        """
        Click on the watch history option.
        """
        self._click(*self.WATCH_HISTORY_COORDS)

    def click_on_first_video(self) -> None:
        """
        Click on a video in the watch history.
        """
        self._click(*self.WATCH_VIDEO_COORDS)

    # todo: add a method for closing the app/tiktok

    # todo: add a method for locking the phone
