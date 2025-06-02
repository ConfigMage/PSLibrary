#!/bin/bash

echo "==========================================================="
echo "Creating Portable Bundle for PowerShell Script Library"
echo "==========================================================="
echo

# Change to parent directory
cd "$(dirname "$0")/.." || exit 1

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python is not installed"
    exit 1
fi

# Check if PyInstaller is installed
echo "Checking for PyInstaller..."
$PYTHON_CMD -m pip show pyinstaller &> /dev/null
if [ $? -ne 0 ]; then
    echo "Installing PyInstaller..."
    $PYTHON_CMD -m pip install pyinstaller || {
        echo "ERROR: Failed to install PyInstaller"
        exit 1
    }
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist PSLibrary_Portable

# Create spec file for PyInstaller
echo "Creating PyInstaller spec file..."
cat > PSLibrary.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        ('README.md', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'PyQt6.Qsci',
        'pygments',
        'pygments.lexers',
        'pygments.lexers.shell',
        'pygments.formatters',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PowerShellScriptLibrary',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PowerShellScriptLibrary',
)
EOF

# Build the application
echo
echo "Building portable application..."
echo "This may take several minutes..."
$PYTHON_CMD -m PyInstaller PSLibrary.spec --clean

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Build failed"
    exit 1
fi

# Create portable folder structure
echo
echo "Creating portable bundle..."
mkdir -p PSLibrary_Portable
cp -r dist/PowerShellScriptLibrary/* PSLibrary_Portable/

# Create run script for portable version
cat > PSLibrary_Portable/run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")" || exit 1
./PowerShellScriptLibrary "$@"
EOF
chmod +x PSLibrary_Portable/run.sh
chmod +x PSLibrary_Portable/PowerShellScriptLibrary

# Create readme for portable version
cat > PSLibrary_Portable/README.txt << 'EOF'
PowerShell Script Library - Portable Version
==========================================

This is a portable version that includes all dependencies.
No installation required!

To run: 
- Linux/Mac: ./run.sh or ./PowerShellScriptLibrary
- Make sure the files have execute permission (chmod +x)

Your scripts database will be created in this folder.

Note: On macOS, you may need to allow the app in Security settings
if it's blocked by Gatekeeper.
EOF

# Clean up build files
echo
echo "Cleaning up build files..."
rm -rf build dist
rm -f PSLibrary.spec

echo
echo "==========================================================="
echo "Portable Bundle Created Successfully!"
echo "==========================================================="
echo
echo "Location: $(pwd)/PSLibrary_Portable"
echo
echo "The portable version includes:"
echo "- All Python dependencies"
echo "- PyQt6 libraries"
echo "- No installation required"
echo
echo "To distribute:"
echo "1. Create archive: tar -czf PSLibrary_Portable.tar.gz PSLibrary_Portable/"
echo "2. Users can extract and run anywhere"
echo