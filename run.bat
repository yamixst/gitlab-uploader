@echo off
setlocal enabledelayedexpansion

:: Get the script's directory
set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%venv"

:: Set color codes
set "BLUE=[94m"
set "GREEN=[92m"
set "RED=[91m"
set "RESET=[0m"

echo %BLUE%GitLab Uploader Setup and Launch%RESET%

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%Error: Python is not installed or not in PATH%RESET%
    echo Please install Python and try again
    pause
    exit /b 1
)

cd "%SCRIPT_DIR%"

:: Create virtual environment if it doesn't exist
if not exist "%VENV_DIR%" (
    echo %BLUE%Creating virtual environment...%RESET%
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo %RED%Failed to create virtual environment%RESET%
        pause
        exit /b 1
    )
    echo %GREEN%Virtual environment created successfully%RESET%
)

:: Activate virtual environment
echo %BLUE%Activating virtual environment...%RESET%
call "%VENV_DIR%\Scripts\activate.bat"
echo %GREEN%Virtual environment activated%RESET%

:: Install dependencies
echo %BLUE%Installing required packages...%RESET%
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo %GREEN%Requirements installed successfully%RESET%

:: Run the application
echo %BLUE%Starting GitLab Uploader...%RESET%
python gitlab_uploader.py

:: Deactivate virtual environment (this line will only be reached if the application is closed)
call deactivate

echo %GREEN%Session completed%RESET%
pause