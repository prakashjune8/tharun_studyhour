@echo off
title ScholasticPulse - Class 8 Study Routine Balancer
echo Launching ScholasticPulse Desktop App...
python study_balancer.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred running python study_balancer.py.
    echo Press any key to exit...
    pause >nul
)
