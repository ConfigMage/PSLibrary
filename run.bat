@echo off
REM PowerShell Script Library Launcher
REM Uses Python 3.12 which has the required packages installed

set PYTHON_PATH=C:\Python312\python.exe

if not exist "%PYTHON_PATH%" (
    echo Error: Python 3.12 not found at %PYTHON_PATH%
    echo Please install Python 3.12 or update the PYTHON_PATH in this script
    pause
    exit /b 1
)

echo Starting PowerShell Script Library...
"%PYTHON_PATH%" main.py %*