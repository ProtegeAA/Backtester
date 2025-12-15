@echo off
REM Stock Backtester - One-Click Runner (Windows)
REM This script automatically sets up the environment and runs the backtester

echo ======================================
echo   Stock Backtester - One-Click Setup
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% detected

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment found
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade requirements
echo Checking dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
echo [OK] All dependencies installed

echo.
echo ======================================
echo   Setup Complete! Starting Backtester
echo ======================================
echo.

REM Run the interactive launcher
python launcher.py

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

pause
