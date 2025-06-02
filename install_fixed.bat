@echo off
echo Installing PowerShell Script Library dependencies...
echo.

REM Use the Python 3.12 installation that already has packages
set PYTHON_PATH=C:\Python312\python.exe

REM Check if Python 3.12 exists
if not exist "%PYTHON_PATH%" (
    echo Error: Python 3.12 not found at %PYTHON_PATH%
    echo Please install Python 3.12 or update the PYTHON_PATH in this script
    pause
    exit /b 1
)

echo Using Python: %PYTHON_PATH%
"%PYTHON_PATH%" --version
echo.

REM Upgrade pip first
echo Upgrading pip...
"%PYTHON_PATH%" -m pip install --upgrade pip

echo.
echo Installing PyQt6...
"%PYTHON_PATH%" -m pip install PyQt6==6.5.0

echo.
echo Installing QScintilla...
"%PYTHON_PATH%" -m pip install PyQt6-QScintilla==2.14.1

echo.
echo Installing Pygments...
"%PYTHON_PATH%" -m pip install Pygments==2.16.1

echo.
echo Installation complete!
echo.
echo You can now run the application with: %PYTHON_PATH% main.py
pause