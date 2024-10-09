@echo off
setlocal enabledelayedexpansion

set "URL=https://vm.tiktok.com/ZMhrX8qXQ/"
echo Resolving URL...

for /f "tokens=*" %%a in ('yt-dlp -g "%URL%"') do set "RESOLVED_URL=%%a"

if "!RESOLVED_URL!"=="" (
    echo Failed to resolve URL. Exiting.
    goto :EOF
)

echo Resolved URL: !RESOLVED_URL!

echo Fetching information...
yt-dlp -J "!RESOLVED_URL!" > info.json

if %errorlevel% neq 0 (
    echo Failed to fetch information. Exiting.
    goto :EOF
)

for /f "tokens=*" %%a in ('type info.json ^| findstr "aweme_type"') do set "CONTENT_TYPE=%%a"
set "CONTENT_TYPE=!CONTENT_TYPE:*:=!"
set "CONTENT_TYPE=!CONTENT_TYPE:~0,-1!"

if "!CONTENT_TYPE!"=="0" (
    echo Content type: Video
    set "OUTPUT_TEMPLATE=%%(title).100s [%%(id)s].%%(ext)s"
    yt-dlp --restrict-filenames -v -o "!OUTPUT_TEMPLATE!" "!RESOLVED_URL!"
) else if "!CONTENT_TYPE!"=="150" (
    echo Content type: Photo/Slide
    echo Downloading images...
    yt-dlp --restrict-filenames -v --skip-download --write-thumbnail -o "image_%%(autonumber)d.%%(ext)s" "!RESOLVED_URL!"
) else (
    echo Unknown content type: !CONTENT_TYPE!
    echo Unable to process this content.
)

del info.json
pause