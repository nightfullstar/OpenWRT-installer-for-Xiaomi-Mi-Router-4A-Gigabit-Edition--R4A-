@echo off
REM Cross-platform Router Installer Launcher for Windows
REM This script will try to use the bundled Python or system Python

echo Router Installer - Starting...

REM Try bundled Python first
if exist "python\python.exe" (
    echo Using bundled Python...
    "python\python.exe" launcher.py
    goto end
)

REM Try system Python3
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using system Python...
    python launcher.py
    goto end
)

REM Try python3 command
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using system Python3...
    python3 launcher.py
    goto end
)

REM No Python found
echo ERROR: Python not found!
echo Please install Python 3.6 or later from https://python.org
echo Or use the bundled python folder if available.
pause

:end
pause
