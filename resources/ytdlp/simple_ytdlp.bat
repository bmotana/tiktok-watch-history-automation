 
@echo off
setlocal enabledelayedexpansion

if "%~1"=="" (
    set /p "URL=Enter the video URL: "
) else (
    set "URL=%~1"
)

if "%2"=="" (
    echo Please provide an output path.
    exit /b 1
)



echo.

set "formats="
for /f "tokens=1" %%a in ('yt-dlp -F "%URL%" ^| findstr /R "^[a-z][a-z0-9_-]*"') do (
    if not "%%a"=="ID" if not "%%a"=="download" (
        set "formats=!formats! %%a"
    )
)

if "%formats%"=="" (
    echo No formats found. Check if the video is accessible.
) else (
    echo.
)

set "OUTPUT_TEMPLATE=%2\%%(title).100s [%%(id)s].%%(ext)s"

for %%f in (%formats%) do (
    echo Trying format: %%f
    yt-dlp --restrict-filenames -q -f %%f -o "%OUTPUT_TEMPLATE%" "%URL%"
    if !errorlevel! equ 0 (
        echo Download successful with format: %%f
        goto :EOF
    ) else (
        echo Download failed with format: %%f
        echo Error code: !errorlevel!
    )
    echo.
)