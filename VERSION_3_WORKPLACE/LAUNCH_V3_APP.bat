@echo off
title ScholasticPulse V3 Launcher
cd /d "%~dp0"
if exist "dist\ScholasticPulse_V3.exe" (
    start "" "dist\ScholasticPulse_V3.exe"
) else if exist "ScholasticPulse_V3.exe" (
    start "" "ScholasticPulse_V3.exe"
) else (
    echo [INFO] Executable not found. Launching via Python...
    python study_balancer.py
)
exit
