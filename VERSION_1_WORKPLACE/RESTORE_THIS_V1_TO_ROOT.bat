@echo off
title Restore Version 1 Safe Reboot Point to Root Project
echo ======================================================================
echo   SAFE REBOOT / RESET POINT: RESTORING VERSION 1 TO ROOT PROJECT
echo ======================================================================
echo.
echo This will restore the clean pre-beautification baseline of:
echo   - study_balancer.py
echo   - index.html
echo   - All supporting data files
echo.
set /p confirm="Are you sure you want to restore Version 1 into root project? (Y/N): "
if /i "%confirm%" NEQ "Y" (
    echo Restoration cancelled.
    pause
    exit /b
)

echo.
echo Copying Version 1 files back to root directory...
copy /y "%~dp0study_balancer.py" "%~dp0..\study_balancer.py"
copy /y "%~dp0index.html" "%~dp0..\index.html"
echo.
echo [SUCCESS] Version 1 has been restored into root workspace!
echo.
pause
