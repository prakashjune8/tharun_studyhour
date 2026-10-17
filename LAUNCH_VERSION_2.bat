@echo off
title Launch ScholasticPulse Version 2 (Shinobi Anime Edition)
if exist "%~dp0VERSION_2_WORKPLACE\dist\ScholasticPulse_V2.exe" (
    start "" "%~dp0VERSION_2_WORKPLACE\dist\ScholasticPulse_V2.exe"
) else (
    echo Executable not compiled yet. Launching Python script...
    python "%~dp0VERSION_2_WORKPLACE\study_balancer.py"
)
