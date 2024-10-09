import time
import pygetwindow as gw
from scripts.tiktok_navigation import AndroidController
from scripts.video_downloader import VideoDownloader
from scripts.link_processing import LinkProcessor
from scripts.image_downloader import ImageDownloader
import pyperclip
import logging
import os


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def go_to_tiktok(controller: AndroidController) -> None:
    controller.close_tiktok()
    time.sleep(2)
    controller.open_tiktok()
    input("Press Enter if you dealt with the add")
    time.sleep(3)
    logging.info("Navigating to TikTok profile")
    controller.click_on_profile()
    time.sleep(3)
    controller.click_on_options()
    time.sleep(3)
    controller.click_on_settings_privacy()
    controller.click_on_acc_activity()
    time.sleep(6)
    controller.click_on_watch_history()
    time.sleep(5)
    controller.click_on_first_video()
    logging.info("Reached first video in watch history")


def extract_link_and_next(controller: AndroidController, video_downloader: VideoDownloader, link_processor: LinkProcessor) -> None:
    try:
        time.sleep(3)
        controller.press_and_hold(500, 500, 2000)
        controller.click(351, 1100)
        time.sleep(2)
        link = pyperclip.paste()
        link_processor.get_link(link)
        content_type = link_processor.get_content_type()
        if content_type == "photo":
            img_downloader = ImageDownloader(link)
            img_downloader.download()
        elif content_type == "video":
            video_downloader.get_link(link)
            video_downloader.download_video()
        time.sleep(6)
        controller.swipe_up()
    except Exception as e:
        logging.error(f"Error in extract_link_and_next: {str(e)}")

def multiple_links(num_of_links: int, controller: AndroidController, video_downloader: VideoDownloader, link_processor: LinkProcessor) -> None:
    try:
        for i in range(num_of_links):
            extract_link_and_next(controller, video_downloader, link_processor)
    finally:
        downloads_folder = video_downloader.get_downloads_path()
        os.startfile(downloads_folder)


def main(controller: AndroidController, video_downloader: VideoDownloader, link_processor: LinkProcessor) -> None:
    windows = gw.getWindowsWithTitle('RKY-LX2')
    if windows:
        scrcpy_window: gw.Window = windows[0]
        scrcpy_window.activate()
        logging.info("scrcpy window activated")
        time.sleep(1)
        go_to_tiktok(controller)
        multiple_links(10, controller, video_downloader, link_processor)
    else:
        logging.warning("scrcpy window not found.")


if __name__ == '__main__':
    config_path = "config/config.yaml"
    android_controller: AndroidController = AndroidController(config_path)
    vid_downloader: VideoDownloader = VideoDownloader(config_path)
    url_processor = LinkProcessor()
    main(android_controller, vid_downloader, url_processor)
