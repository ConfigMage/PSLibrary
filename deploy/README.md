# PowerShell Script Library - Deployment Guide

This guide provides instructions for deploying the PowerShell Script Library application on various systems.

## Prerequisites

- Python 3.10 or higher (3.12 recommended)
- pip (Python package manager)
- Git (optional, for cloning the repository)

## Quick Installation

### Windows

1. Download or clone the PSLibrary folder to your desired location
2. Navigate to the `deploy` folder
3. Run the installer:
   ```cmd
   install_windows.bat
   ```

### Linux/macOS

1. Download or clone the PSLibrary folder to your desired location
2. Navigate to the `deploy` folder
3. Make the installer executable and run it:
   ```bash
   chmod +x install_unix.sh
   ./install_unix.sh
   ```

## Manual Installation

### Step 1: Install Python

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation

#### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

#### macOS
```bash
# Using Homebrew
brew install python@3.12
```

### Step 2: Install Dependencies

Navigate to the PSLibrary directory and run:

```bash
# Windows
pip install -r requirements.txt

# Linux/macOS (may need sudo)
pip3 install -r requirements.txt
```

### Step 3: Verify Installation

Run the check script:
```bash
python check_installation.py
```

### Step 4: Launch the Application

```bash
# Windows
python main.py
# or use the run.bat file

# Linux/macOS
python3 main.py
# or use ./run.sh
```

## Troubleshooting

### PyQt6 Installation Issues

If PyQt6 fails to install, try:

1. **Update pip**:
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Install with specific version**:
   ```bash
   pip install PyQt6==6.5.0
   ```

3. **Try PySide6 instead**:
   ```bash
   pip install -r requirements_pyside.txt
   ```

### DLL Loading Errors (Windows)

If you get DLL errors:

1. Uninstall all PyQt6 packages:
   ```bash
   pip uninstall -y PyQt6 PyQt6-Qt6 PyQt6-sip PyQt6-QScintilla
   ```

2. Reinstall with matching versions:
   ```bash
   pip install PyQt6-Qt6==6.5.0
   pip install PyQt6-sip==13.5.1
   pip install PyQt6==6.5.0
   pip install PyQt6-QScintilla==2.14.1
   ```

### Permission Errors (Linux/macOS)

If you get permission errors, either:

1. Use `sudo` for system-wide installation:
   ```bash
   sudo pip3 install -r requirements.txt
   ```

2. Or use `--user` flag for user installation:
   ```bash
   pip3 install --user -r requirements.txt
   ```

## Creating a Standalone EXE (Windows)

To create a single-file executable that doesn't require Python installation:

```bash
# Navigate to deploy folder
cd deploy

# Run the bundle creator
create_bundle_windows.bat
```

This will create:
- `PSLibrary.exe` - Single-file executable
- `SIGNING_INSTRUCTIONS.txt` - Instructions for code signing

### Code Signing the EXE

To avoid "Unknown Publisher" warnings, sign the EXE with a code signing certificate:

1. **Find your certificate thumbprint**:
   - Open `certmgr.msc`
   - Navigate to Personal → Certificates
   - Find your code signing certificate
   - Double-click → Details → Thumbprint

2. **Sign the EXE**:
   ```cmd
   signtool sign /sha1 "YourThumbprint" /t http://timestamp.digicert.com /fd sha256 PSLibrary.exe
   ```

3. **Verify the signature**:
   ```cmd
   signtool verify /pa PSLibrary.exe
   ```

**Note**: `signtool.exe` comes with Windows SDK or Visual Studio.

### Distribution

After signing:
1. Delete `SIGNING_INSTRUCTIONS.txt` 
2. The signed `PSLibrary.exe` is ready for distribution
3. Users can run it directly - no installation needed!

## Creating a Portable Bundle (Linux/macOS)

```bash
./deploy/create_bundle_unix.sh
```

This will create a `PSLibrary_Portable` folder with everything needed to run the application.

### Bundle vs Installer

- **Installers** (`install_windows.bat`, `install_unix.sh`):
  - Require Python on target machine
  - Smaller download (~10MB)
  - For developers or technical users
  
- **Single-File EXE** (Windows only):
  - Includes Python and all dependencies
  - One file (~40-50MB)
  - Can be code signed
  - For end users who want simplicity

- **Portable Bundle** (Linux/macOS):
  - Include Python and all dependencies
  - Larger size (~100-150MB)
  - Folder structure
  - For end users on non-Windows platforms

See `BUNDLE_GUIDE.md` for detailed bundle creation and distribution instructions.

## Configuration

The application stores its data in:
- **Database**: `script_library.db` in the application directory (when run from source)
- **Database**: User's AppData folder (when run as single-file EXE)
- **Settings**: User's home directory under `.scriptlibrary/`

## Updating

To update to a newer version:

1. Backup your `script_library.db` file
2. Download the new version
3. Copy your `script_library.db` to the new directory
4. Run the installer again to update dependencies

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Run `check_installation.py` to diagnose problems
3. Check that your Python version is 3.10 or higher
4. Ensure all dependencies are properly installed

## System Requirements

- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 11+
- **Python**: 3.10 - 3.12
- **RAM**: 512MB minimum
- **Storage**: 200MB for application and dependencies