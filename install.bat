@echo off
echo Installing PowerShell Script Library dependencies...
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing PyQt6...
python -m pip install PyQt6==6.5.0

echo.
echo Installing QScintilla...
python -m pip install PyQt6-QScintilla==2.14.1

echo.
echo Installing Pygments...
python -m pip install Pygments==2.16.1

echo.
echo Installation complete!
echo.
echo You can now run the application with: python main.py
pause