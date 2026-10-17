@echo off
title Restore ScholasticPulse to Version 1 (Safe Baseline)
echo ======================================================================
echo   SCHOLASTICPULSE: SAFE REBOOT TO VERSION 1 BASELINE
echo ======================================================================
echo.
echo This 1-Click script safely resets the project back to Version 1:
echo (The state right before the design / beautification conversation started)
echo.
set /p confirm="Do you want to reset your root project to Version 1 now? (Y/N): "
if /i "%confirm%" NEQ "Y" (
    echo Reset cancelled.
    pause
    exit /b
)

echo.
echo Restoring Version 1 study_balancer.py...
copy /y "%~dp0VERSION_1_WORKPLACE\study_balancer.py" "%~dp0study_balancer.py"
echo Restoring Version 1 index.html...
copy /y "%~dp0VERSION_1_WORKPLACE\index.html" "%~dp0index.html"
echo.
echo ======================================================================
echo [SUCCESS] Safe Reboot Complete!
echo ScholasticPulse is now back to Version 1 baseline.
echo ======================================================================
echo.
pause
