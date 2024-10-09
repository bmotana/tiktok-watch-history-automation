@echo off
setlocal enabledelayedexpansion

if "%~1"=="" (
    set /p "URL=Enter the video URL: "
) else (
    set "URL=%~1"
)

echo Fetching available formats...
yt-dlp -F "%URL%"

set "OUTPUT_TEMPLATE=%%(title)s.%%(ext)s"

set "formats=h264_720p_2669673-0 h264_720p_2669673-1 h264_720p_2669673-2 bytevc1_1080p_1725713-0 bytevc1_1080p_1725713-1 bytevc1_1080p_1725713-2"

echo Attempting downloads:
for %%f in (%formats%) do (
    echo Trying format: %%f
    yt-dlp  -v -f %%f -o "%OUTPUT_TEMPLATE%" "%URL%"
    if !errorlevel! equ 0 (
        echo Download successful with format: %%f
        goto :EOF
    ) else (
        echo Download failed with format: %%f
        echo Error code: !errorlevel!
    )
    echo.
)

echo All download attempts failed.
pause