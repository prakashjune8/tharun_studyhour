@echo off
title Build ScholasticPulse Version 1 Standalone EXE
echo ======================================================================
echo    BUILDING STANDALONE EXECUTABLE: ScholasticPulse_V1.exe
echo ======================================================================
cd /d "%~dp0"
pyinstaller --noconfirm --onefile --windowed --name "ScholasticPulse_V1" study_balancer.py
echo.
echo Build finished! Executable is at: "%~dp0dist\ScholasticPulse_V1.exe"
pause
