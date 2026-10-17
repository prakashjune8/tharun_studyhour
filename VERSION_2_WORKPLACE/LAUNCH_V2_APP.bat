@echo off
title Launch ScholasticPulse Version 2 (Anime Edition)
if exist "%~dp0dist\ScholasticPulse_V2.exe" (
    start "" "%~dp0dist\ScholasticPulse_V2.exe"
) else (
    echo Executable not found in dist. Launching Python script...
    python "%~dp0study_balancer.py"
)
