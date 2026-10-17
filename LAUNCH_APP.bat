@echo off
setlocal
title ScholasticPulse Desktop Launcher

:: 1. If compiled executable exists in dist\, launch it directly
if exist "%~dp0dist\ScholasticPulse.exe" (
    start "" "%~dp0dist\ScholasticPulse.exe"
    exit /b 0
)

:: 2. Otherwise run using pythonw (silent, no black CMD window) or python
start "" pythonw "%~dp0study_balancer.py"
if %ERRORLEVEL% NEQ 0 (
    python "%~dp0study_balancer.py"
)
exit /b 0
