@echo off
echo Fixing PowerShell Script Library installation...
echo.

REM Use Python 3.12
set PYTHON_PATH=C:\Python312\python.exe

if not exist "%PYTHON_PATH%" (
    echo Error: Python 3.12 not found at %PYTHON_PATH%
    pause
    exit /b 1
)

echo Using Python: %PYTHON_PATH%
"%PYTHON_PATH%" --version
echo.

echo Cleaning up old installations...
echo.

REM Uninstall all PyQt6 related packages
echo Uninstalling PyQt6 packages...
"%PYTHON_PATH%" -m pip uninstall -y PyQt6 PyQt6-Qt6 PyQt6-sip PyQt6-QScintilla

echo.
echo Installing fresh packages...
echo.

REM Install specific compatible versions
"%PYTHON_PATH%" -m pip install --force-reinstall --no-cache-dir PyQt6-Qt6==6.5.0
"%PYTHON_PATH%" -m pip install --force-reinstall --no-cache-dir PyQt6-sip==13.5.1
"%PYTHON_PATH%" -m pip install --force-reinstall --no-cache-dir PyQt6==6.5.0
"%PYTHON_PATH%" -m pip install --force-reinstall --no-cache-dir PyQt6-QScintilla==2.14.1
"%PYTHON_PATH%" -m pip install --force-reinstall --no-cache-dir Pygments==2.16.1

echo.
echo Testing installation...
"%PYTHON_PATH%" -c "import PyQt6.QtCore; print('PyQt6 imported successfully')"

echo.
echo Installation complete!
echo.
echo You can now run the application with: run.bat
pause