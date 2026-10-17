@echo off
title Launch ScholasticPulse Version 1
if exist "%~dp0dist\ScholasticPulse_V1.exe" (
    start "" "%~dp0dist\ScholasticPulse_V1.exe"
) else (
    echo Executable not compiled yet. Running Python script...
    python "%~dp0study_balancer.py"
)
