@echo off
chcp 65001 >nul
title IDM Viewer v2

cd /d "%~dp0"

REM Find python
set PYCMD=
where python >nul 2>&1 && set PYCMD=python
if "%PYCMD%"=="" (where py >nul 2>&1 && set PYCMD=py)
if "%PYCMD%"=="" (where python3 >nul 2>&1 && set PYCMD=python3)

if "%PYCMD%"=="" (
    echo.
    echo [ERROR] Python not found. Install from https://python.org
    echo.
    pause
    exit /b 1
)

%PYCMD% launch_viewer.py
