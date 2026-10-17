@echo off
setlocal enabledelayedexpansion
title ScholasticPulse - 1-Click Desktop App Builder
echo ======================================================================
echo    SCHOLASTICPULSE: 1-CLICK DESKTOP APP BUILDER & PACKAGER
echo ======================================================================
echo.
echo [1/3] Checking environment & installing PyInstaller if needed...
python -m pip install pyinstaller --quiet

echo.
echo [2/3] Compiling standalone executable (ScholasticPulse.exe)...
echo       Please wait 10-20 seconds...
pyinstaller --noconfirm --onefile --windowed --name "ScholasticPulse" study_balancer.py

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Compilation failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/3] Creating 1-Click Desktop Shortcut on your Windows Desktop...
powershell -ExecutionPolicy Bypass -File "%~dp0CREATE_DESKTOP_SHORTCUT.ps1"

echo.
echo ======================================================================
echo  SUCCESS! Standalone Desktop App Created!
echo  Location: "%~dp0dist\ScholasticPulse.exe"
echo  A shortcut named "ScholasticPulse Class 8" is now on your Desktop!
echo ======================================================================
echo.
echo Launching the application now...
start "" "%~dp0dist\ScholasticPulse.exe"
timeout /t 3 >nul
