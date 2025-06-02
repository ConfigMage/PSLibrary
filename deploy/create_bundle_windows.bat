@echo off
title PowerShell Script Library - Bundle Creator
echo ===========================================================
echo Creating Portable Bundle for PowerShell Script Library
echo ===========================================================
echo.

REM Change to parent directory
cd ..

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
echo Checking for PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "PSLibrary_Portable" rmdir /s /q "PSLibrary_Portable"

REM Create spec file for PyInstaller
echo Creating PyInstaller spec file...
(
echo # -*- mode: python ; coding: utf-8 -*-
echo.
echo block_cipher = None
echo.
echo a = Analysis(
echo     ['main.py'],
echo     pathex=[],
echo     binaries=[],
echo     datas=[
echo         ^('resources', 'resources'^),
echo         ^('README.md', '.'^),
echo         ^('requirements.txt', '.'^),
echo     ],
echo     hiddenimports=[
echo         'PyQt6.QtCore',
echo         'PyQt6.QtGui', 
echo         'PyQt6.QtWidgets',
echo         'PyQt6.Qsci',
echo         'pygments',
echo         'pygments.lexers',
echo         'pygments.lexers.shell',
echo         'pygments.formatters',
echo         'sqlite3',
echo     ],
echo     hookspath=[],
echo     hooksconfig={},
echo     runtime_hooks=[],
echo     excludes=[],
echo     win_no_prefer_redirects=False,
echo     win_private_assemblies=False,
echo     cipher=block_cipher,
echo     noarchive=False,
echo ^)
echo.
echo pyz = PYZ^(a.pure, a.zipped_data, cipher=block_cipher^)
echo.
echo exe = EXE(
echo     pyz,
echo     a.scripts,
echo     [],
echo     exclude_binaries=True,
echo     name='PowerShellScriptLibrary',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=True,
echo     console=False,
echo     disable_windowed_traceback=False,
echo     argv_emulation=False,
echo     target_arch=None,
echo     codesign_identity=None,
echo     entitlements_file=None,
echo     icon='resources/app.ico' if os.path.exists^('resources/app.ico'^) else None,
echo ^)
echo.
echo coll = COLLECT(
echo     exe,
echo     a.binaries,
echo     a.zipfiles,
echo     a.datas,
echo     strip=False,
echo     upx=True,
echo     upx_exclude=[],
echo     name='PowerShellScriptLibrary',
echo ^)
) > PSLibrary.spec

REM Build the application
echo.
echo Building portable application...
echo This may take several minutes...
python -m PyInstaller PSLibrary.spec --clean

if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    pause
    exit /b 1
)

REM Create portable folder structure
echo.
echo Creating portable bundle...
mkdir PSLibrary_Portable
xcopy /E /I /Y dist\PowerShellScriptLibrary PSLibrary_Portable\

REM Create run script for portable version
echo @echo off > PSLibrary_Portable\run.bat
echo cd /d "%%~dp0" >> PSLibrary_Portable\run.bat
echo start PowerShellScriptLibrary.exe >> PSLibrary_Portable\run.bat

REM Create readme for portable version
(
echo PowerShell Script Library - Portable Version
echo ==========================================
echo.
echo This is a portable version that includes all dependencies.
echo No installation required!
echo.
echo To run: Double-click run.bat or PowerShellScriptLibrary.exe
echo.
echo Note: Windows Defender may flag the executable on first run.
echo This is normal for PyInstaller applications.
echo.
echo Your scripts database will be created in this folder.
) > PSLibrary_Portable\README.txt

REM Clean up build files
echo.
echo Cleaning up build files...
rmdir /s /q build
rmdir /s /q dist
del PSLibrary.spec

echo.
echo ===========================================================
echo Portable Bundle Created Successfully!
echo ===========================================================
echo.
echo Location: %CD%\PSLibrary_Portable
echo.
echo The portable version includes:
echo - All Python dependencies
echo - PyQt6 libraries
echo - No installation required
echo.
echo To distribute:
echo 1. Zip the PSLibrary_Portable folder
echo 2. Users can extract and run anywhere
echo.
pause