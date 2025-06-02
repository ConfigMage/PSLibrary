#!/bin/bash

echo "==========================================================="
echo "PowerShell Script Library - Unix Installer"
echo "==========================================================="
echo

# Change to parent directory
cd "$(dirname "$0")/.." || exit 1

# Detect OS
OS="Unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
fi

echo "Detected OS: $OS"
echo

# Check if Python is installed
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python is not installed"
    echo
    echo "Please install Python 3.10 or higher:"
    if [[ "$OS" == "Linux" ]]; then
        echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "  Fedora: sudo dnf install python3 python3-pip"
        echo "  Arch: sudo pacman -S python python-pip"
    elif [[ "$OS" == "macOS" ]]; then
        echo "  Using Homebrew: brew install python@3.12"
        echo "  Or download from: https://www.python.org/downloads/"
    fi
    exit 1
fi

# Display Python version
echo "Found Python:"
$PYTHON_CMD --version
echo

# Check Python version is 3.10+
$PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Python 3.10 or higher is required"
    echo "Please upgrade your Python installation"
    exit 1
fi

# Check if pip is installed
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "ERROR: pip is not installed"
    echo "Please install pip for Python 3"
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip || {
    echo "WARNING: Failed to upgrade pip, trying with --user flag..."
    $PYTHON_CMD -m pip install --user --upgrade pip
}
echo

# Install dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
echo

# Try system-wide installation first
$PYTHON_CMD -m pip install -r requirements.txt 2>/dev/null || {
    echo "System-wide installation failed, trying user installation..."
    $PYTHON_CMD -m pip install --user -r requirements.txt || {
        echo
        echo "ERROR: Failed to install dependencies"
        echo
        echo "Trying alternative installation method..."
        $PYTHON_CMD -m pip install --user PyQt6==6.5.0
        $PYTHON_CMD -m pip install --user PyQt6-QScintilla==2.14.1
        $PYTHON_CMD -m pip install --user Pygments==2.16.1
        
        if [ $? -ne 0 ]; then
            echo
            echo "Installation failed. Please try manual installation:"
            echo "1. Run: $PYTHON_CMD -m pip install --user PyQt6==6.5.0"
            echo "2. Run: $PYTHON_CMD -m pip install --user PyQt6-QScintilla==2.14.1"
            echo "3. Run: $PYTHON_CMD -m pip install --user Pygments==2.16.1"
            exit 1
        fi
    }
}

echo
echo "Running installation check..."
$PYTHON_CMD check_installation.py || {
    echo
    echo "WARNING: Installation check reported issues"
    echo "Please review the output above"
    echo
}

# Create run script if it doesn't exist
if [ ! -f "run.sh" ]; then
    echo "Creating run script..."
    cat > run.sh << EOF
#!/bin/bash
cd "\$(dirname "\$0")" || exit 1
$PYTHON_CMD main.py "\$@"
EOF
    chmod +x run.sh
fi

# Create desktop entry for Linux
if [[ "$OS" == "Linux" ]]; then
    DESKTOP_FILE="$HOME/.local/share/applications/powershell-script-library.desktop"
    echo "Creating desktop entry..."
    mkdir -p "$HOME/.local/share/applications"
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=PowerShell Script Library
Comment=Manage PowerShell and Batch scripts
Exec=$PWD/run.sh
Icon=utilities-terminal
Terminal=false
Categories=Development;Utility;
EOF
    chmod +x "$DESKTOP_FILE"
    echo "Desktop entry created at: $DESKTOP_FILE"
fi

# Create macOS app bundle
if [[ "$OS" == "macOS" ]]; then
    echo "Creating macOS app launcher..."
    APP_NAME="PowerShell Script Library"
    APP_DIR="/Applications/${APP_NAME}.app"
    
    if [ -w "/Applications" ]; then
        cat > "/tmp/pslibrary_launcher.sh" << EOF
#!/bin/bash
cd "$PWD" || exit 1
$PYTHON_CMD main.py "\$@"
EOF
        chmod +x "/tmp/pslibrary_launcher.sh"
        
        echo "To create an app icon, you can:"
        echo "1. Create an Automator application that runs: $PWD/run.sh"
        echo "2. Save it as '${APP_NAME}' in your Applications folder"
    fi
fi

echo
echo "==========================================================="
echo "Installation Complete!"
echo "==========================================================="
echo
echo "You can now run the application using:"
echo "  - ./run.sh (recommended)"
echo "  - $PYTHON_CMD main.py"
echo

if [[ "$OS" == "Linux" ]]; then
    echo "A desktop entry has been created. You may need to:"
    echo "  - Log out and back in for it to appear in your menu"
    echo "  - Or run: update-desktop-database ~/.local/share/applications"
fi

echo