@echo off
title PowerShell Script Library - EXE Creator
echo ===========================================================
echo Creating Single-File EXE for PowerShell Script Library
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
if exist "PSLibrary.exe" del /f /q "PSLibrary.exe"

REM Create spec file for PyInstaller (single-file)
echo Creating PyInstaller spec file for single-file EXE...
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
echo     a.binaries,
echo     a.zipfiles,
echo     a.datas,
echo     [],
echo     name='PSLibrary',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=True,
echo     upx_exclude=[],
echo     runtime_tmpdir=None,
echo     console=False,
echo     disable_windowed_traceback=False,
echo     argv_emulation=False,
echo     target_arch=None,
echo     codesign_identity=None,
echo     entitlements_file=None,
echo     icon='resources/app.ico' if os.path.exists^('resources/app.ico'^) else None,
echo ^)
) > PSLibrary.spec

REM Build the application
echo.
echo Building single-file EXE...
echo This may take several minutes...
python -m PyInstaller PSLibrary.spec --clean --onefile

if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    pause
    exit /b 1
)

REM Move the exe to parent directory
echo.
echo Moving EXE to project root...
move dist\PSLibrary.exe . >nul

REM Create signing instructions
echo Creating signing instructions...
(
echo CODE SIGNING INSTRUCTIONS
echo ========================
echo.
echo The PSLibrary.exe has been created but is NOT YET SIGNED.
echo To sign the executable with your code signing certificate:
echo.
echo 1. Open Command Prompt as Administrator
echo.
echo 2. Navigate to the folder containing PSLibrary.exe
echo.
echo 3. Use one of these commands depending on how your certificate is stored:
echo.
echo    If using certificate from Windows Certificate Store by name:
echo    signtool sign /n "Your Certificate Subject Name" /t http://timestamp.digicert.com /fd sha256 PSLibrary.exe
echo.
echo    If using certificate from Windows Certificate Store by thumbprint:
echo    signtool sign /sha1 "YourCertThumbprint" /t http://timestamp.digicert.com /fd sha256 PSLibrary.exe
echo.
echo    If using a PFX file:
echo    signtool sign /f "path\to\your\certificate.pfx" /p "password" /t http://timestamp.digicert.com /fd sha256 PSLibrary.exe
echo.
echo 4. Verify the signature:
echo    signtool verify /pa PSLibrary.exe
echo.
echo NOTES:
echo - signtool.exe comes with Windows SDK or Visual Studio
echo - The timestamp server ensures the signature remains valid after cert expiration
echo - /fd sha256 uses SHA-256 for the file digest ^(recommended^)
echo - You can find your certificate thumbprint in certmgr.msc
echo.
echo After signing, the EXE will show your publisher name instead of "Unknown Publisher"
) > SIGNING_INSTRUCTIONS.txt

REM Clean up build files
echo.
echo Cleaning up build files...
rmdir /s /q build
rmdir /s /q dist
del PSLibrary.spec

echo.
echo ===========================================================
echo Single-File EXE Created Successfully!
echo ===========================================================
echo.
echo Location: %CD%\PSLibrary.exe
echo Size: 
dir PSLibrary.exe | find "PSLibrary.exe"
echo.
echo IMPORTANT: The EXE is NOT signed yet!
echo.
echo To sign the executable:
echo 1. Read SIGNING_INSTRUCTIONS.txt for detailed steps
echo 2. Use signtool with your certificate thumbprint
echo 3. After signing, delete SIGNING_INSTRUCTIONS.txt before distribution
echo.
echo The single-file EXE includes:
echo - All Python dependencies
echo - PyQt6 libraries  
echo - No installation required
echo - Database will be created in user's AppData folder
echo.
pause