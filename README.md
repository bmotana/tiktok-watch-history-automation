# TikTok Watch History Automation

Extract TikTok video and photo links from the watch history displayed on an Android device, then download the corresponding media. The script controls the device with ADB, mirrors it with scrcpy, and uses yt-dlp for video downloads.

This project automates interaction with TikTok's app interface. TikTok may change its screens, and the coordinate-based navigation may need adjustment for your device and display settings.

## Requirements

- Windows 10 or later
- Python 3.10 or later
- An Android device with USB debugging enabled and authorized for ADB
- The Android SDK platform tools (`adb`)
- Google Chrome and a compatible ChromeDriver for photo downloads

The repository includes scrcpy, ADB, FFmpeg, and yt-dlp helper files under `resources/`. Check the upstream licenses and notices for bundled third-party software before redistributing those binaries.

## Setup

Clone the repository and create a virtual environment:

```powershell
git clone https://github.com/bmotana/tiktok-watch-history-automation.git
cd tiktok-watch-history-automation
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

Connect and authorize your Android device, then confirm that `adb devices` lists it. Review `config/config.yaml` and update the configured resource paths if you run the project from a different working directory.

## Usage

Start scrcpy with your Android device connected, open TikTok, and run:

```powershell
python main.py
```

The automation navigates to watch history and processes up to ten entries. Downloads are saved to your Windows `Downloads` folder. The script may prompt you to dismiss an in-app advertisement before continuing.

Before downloading, the script checks that copied links use HTTP(S) and a TikTok hostname, follows TikTok short links, and accepts only resolved video or photo URLs. Invalid, unsupported, or off-site links are logged and skipped; the automation then advances to the next watch-history entry.

## Development

Install the development dependency, run Ruff, and execute the unit tests:

```powershell
python -m pip install -e ".[dev]"
ruff check .
python -m unittest discover -s tests -v
```

GitHub Actions runs Ruff, the unit tests, and a Python syntax check on Windows for pushes and pull requests. Link-processing tests mock network requests, so they do not contact TikTok.

## Privacy and responsible use

This tool operates on the TikTok account and device that you configure. Keep downloaded content private unless you have permission to share it, and follow TikTok's terms and applicable laws.

## License

This project's original code is released under the MIT License. See [LICENSE](LICENSE). Third-party tools and bundled binaries may have separate licenses.
