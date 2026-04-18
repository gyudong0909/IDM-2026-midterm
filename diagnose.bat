@echo off
chcp 65001 >nul
title IDM Diagnose
cls

echo ============================================================
echo   IDM Viewer Diagnose (problem finder)
echo ============================================================
echo.

echo [1/5] Current directory check...
echo   Current dir: %cd%
echo   Batch dir:   %~dp0
echo.

cd /d "%~dp0"
echo   Changed to:  %cd%
echo.

echo [2/5] File check...
if exist study_viewer_v2.html (
    echo   [OK] study_viewer_v2.html found
) else (
    echo   [FAIL] study_viewer_v2.html NOT FOUND
)
if exist launch_viewer.py (
    echo   [OK] launch_viewer.py found
) else (
    echo   [FAIL] launch_viewer.py NOT FOUND
)
echo.

echo [3/5] Python check...
python --version 2>nul
if errorlevel 1 (
    echo   [FAIL] 'python' command NOT FOUND
    py --version 2>nul
    if errorlevel 1 (
        echo   [FAIL] 'py' command NOT FOUND
        python3 --version 2>nul
        if errorlevel 1 (
            echo   [FAIL] 'python3' command NOT FOUND
            echo.
            echo   *** Python is NOT installed on Windows! ***
            echo   *** Install from https://python.org       ***
            echo   *** IMPORTANT: Check "Add to PATH" during install ***
        ) else (
            echo   [OK] python3 available
        )
    ) else (
        echo   [OK] py available (Python Launcher for Windows)
    )
) else (
    echo   [OK] python available
)
echo.

echo [4/5] Port 8765 check...
netstat -an | findstr ":8765" >nul
if errorlevel 1 (
    echo   [OK] Port 8765 is free
) else (
    echo   [WARN] Port 8765 already in use!
    echo   Another process is using this port. Either:
    echo   - Close the other process
    echo   - Change PORT in launch_viewer.py
)
echo.

echo [5/5] Trying to start server manually...
echo.
echo Press any key to attempt starting server...
pause >nul

echo.
echo ============================================================
echo   If server starts, keep this window open and try:
echo   http://localhost:8765/study_viewer_v2.html
echo ============================================================
echo.

where python >nul 2>&1 && (
    python launch_viewer.py
    goto :eof
)
where py >nul 2>&1 && (
    py launch_viewer.py
    goto :eof
)
where python3 >nul 2>&1 && (
    python3 launch_viewer.py
    goto :eof
)

echo ERROR: No Python interpreter found.
echo.
echo Alternative: use WSL instead.
echo   1. Open WSL/Ubuntu terminal
echo   2. cd /mnt/c/Users/gyudo/iCloudDrive/Desktop/2026-1/데이터마이닝개론/IDM-2026-midterm
echo   3. python3 -m http.server 8765
echo   4. Open http://localhost:8765/study_viewer_v2.html in Chrome
echo.
pause
