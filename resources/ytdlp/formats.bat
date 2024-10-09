@echo off
setlocal enabledelayedexpansion

set "URL=https://vm.tiktok.com/ZMhrX8qXQ/"

echo Fetching format information:
yt-dlp -F "%URL%"

echo.
echo Parsing formats:
set "formats="
for /f "tokens=1" %%a in ('yt-dlp -F "%URL%" ^| findstr /R "^[a-z][a-z0-9_-]*"') do (
    if not "%%a"=="ID" if not "%%a"=="download" (
        set "formats=!formats! %%a"
        echo Found format: %%a
    )
)

if "%formats%"=="" (
    echo No formats found. Check if the video is accessible.
) else (
    echo.
    echo Available formats:%formats%
)

pause

set "OUTPUT_TEMPLATE=%%(title).100s [%%(id)s].%%(ext)s"

for %%f in (%formats%) do (
    echo Trying format: %%f
    yt-dlp --restrict-filenames -v -f %%f -o "%OUTPUT_TEMPLATE%" "%URL%"
    if !errorlevel! equ 0 (
        echo Download successful with format: %%f
        goto :EOF
    ) else (
        echo Download failed with format: %%f
        echo Error code: !errorlevel!
    )
    echo.
)