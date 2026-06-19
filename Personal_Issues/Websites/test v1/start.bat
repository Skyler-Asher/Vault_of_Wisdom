@echo off
title Planner

:: ── Find Python ─────────────────────────────────────────────
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON=python
    goto :start
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON=py
    goto :start
)

echo.
echo  Python not found.
echo  Download it from https://www.python.org/downloads/
echo  Make sure to check "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:: ── Start server ─────────────────────────────────────────────
:start
cd /d "%~dp0"

:: Open browser after 1 second (gives server time to start)
start "" cmd /c "timeout /t 1 >nul && start http://localhost:8000/index.html"

:: Start the server (this window stays open — close it to stop)
%PYTHON% server.py

pause
