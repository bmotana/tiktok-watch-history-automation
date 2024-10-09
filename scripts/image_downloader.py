import base64
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging

class ImageDownloader:
    def __init__(self, tiktok_url):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.downloads_path = self.get_downloads_path()
        self.link = tiktok_url


    @staticmethod
    def get_downloads_path():
        home_directory = os.path.expanduser("~")
        downloads_folder = os.path.join(home_directory, "Downloads")
        return downloads_folder

    @staticmethod
    def download_image(url, save_path):
        # Check if the URL is base64-encoded
        if url.startswith('data:image'):
            # Base64 image
            header, encoded = url.split(',', 1)
            data = base64.b64decode(encoded)
            with open(save_path, 'wb') as f:
                f.write(data)
        else:
            # Normal image URL
            response = requests.get(url)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)

    @staticmethod
    def _set_up_driver_options():
        chrome_options = Options()
        chrome_options.add_argument("--headless=old")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--mute-audio')  # Mute any audio
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Disable logging
        return chrome_options

    @staticmethod
    def _get_signature(url):
        url_parts = url.split('&')
        signature = None
        for part in url_parts:
            if 'signature=' in part:
                signature = part.split('signature=')[1]  # Extract the signature
                break
        return signature


    def download(self):
        chrome_options = self._set_up_driver_options()
        driver = webdriver.Chrome(options=chrome_options)
        # Open the TikTok photo slideshow URL
        driver.get(self.link)
        # Wait for the images to be visible on the page
        try:
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.TAG_NAME, 'img'))
            )
        except Exception as e:
            print(f"Error: {e}")
            driver.quit()
        # Locate image elements
        images = driver.find_elements(By.TAG_NAME, 'img')
        signatures = []
        for index, img in enumerate(images):
            try:
                img_url = img.get_attribute('src')
                if ('p16-sign-va.tiktokcdn.com' in img_url) and ("tos-maliva-i-photomode-us" in img_url):
                    signature = self._get_signature(img_url)
                    if not signature in signatures and signature:
                        save_path = f'{self.downloads_path}/image_{index}_{signature}.jpg'
                        try:
                            self.download_image(img_url, save_path)
                            print(f'Downloaded {save_path}')
                        except Exception as e:
                            print(f"Failed to download image {index}: {e}")
                        finally:
                            signatures.append(signature)
            except StaleElementReferenceException:
                print(f"Skipped image {index} due to StaleElementReferenceException")
                continue
        # Close the browser
        driver.quit()
