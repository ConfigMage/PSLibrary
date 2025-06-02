@echo off
title PowerShell Script Library - Windows Installer
echo ===========================================================
echo PowerShell Script Library - Windows Installer
echo ===========================================================
echo.

REM Change to parent directory
cd ..

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Display Python version
echo Found Python:
python --version
echo.

REM Check Python version is 3.10+
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.10 or higher is required
    echo Please upgrade your Python installation
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
echo.

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo.
    echo Trying alternative installation method...
    python -m pip install PyQt6==6.5.0
    python -m pip install PyQt6-QScintilla==2.14.1
    python -m pip install Pygments==2.16.1
    
    if errorlevel 1 (
        echo.
        echo Installation failed. Please try manual installation:
        echo 1. Run: python -m pip install PyQt6==6.5.0
        echo 2. Run: python -m pip install PyQt6-QScintilla==2.14.1
        echo 3. Run: python -m pip install Pygments==2.16.1
        pause
        exit /b 1
    )
)

echo.
echo Running installation check...
python check_installation.py
if errorlevel 1 (
    echo.
    echo WARNING: Installation check reported issues
    echo Please review the output above
    echo.
)

echo.
echo ===========================================================
echo Installation Complete!
echo ===========================================================
echo.
echo You can now run the application using:
echo   - run.bat (recommended)
echo   - python main.py
echo.
echo A desktop shortcut will be created...
echo.

REM Create desktop shortcut
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\PowerShell Script Library.lnk'); $Shortcut.TargetPath = '%CD%\run.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.IconLocation = 'powershell.exe'; $Shortcut.Save()"

if exist "%USERPROFILE%\Desktop\PowerShell Script Library.lnk" (
    echo Desktop shortcut created successfully!
) else (
    echo Failed to create desktop shortcut
)

echo.
pause