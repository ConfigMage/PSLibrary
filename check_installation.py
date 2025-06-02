#!/usr/bin/env python3
"""
Diagnostic script to check if all dependencies are properly installed
"""

import sys
import subprocess

def check_python_version():
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("⚠️  WARNING: Python 3.8 or higher is required")
        return False
    else:
        print("✓ Python version is compatible")
        return True

def check_package(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✓ {package_name} is installed")
        return True
    except ImportError:
        print(f"✗ {package_name} is NOT installed")
        return False

def suggest_installation():
    print("\n" + "="*60)
    print("INSTALLATION INSTRUCTIONS")
    print("="*60)
    print("\nOption 1: Run the installation script (Recommended)")
    print("  Windows: install.bat")
    print("  Linux/Mac: ./install.sh")
    
    print("\nOption 2: Manual installation with PyQt6")
    print("  python -m pip install PyQt6==6.5.0")
    print("  python -m pip install PyQt6-QScintilla==2.14.1")
    print("  python -m pip install Pygments==2.16.1")
    
    print("\nOption 3: If PyQt6 fails, try PySide6")
    print("  python -m pip install PySide6==6.5.0")
    print("  python -m pip install QScintilla==2.14.1")
    print("  python -m pip install Pygments==2.16.1")
    
    print("\nOption 4: Install from requirements file")
    print("  python -m pip install -r requirements.txt")
    
    print("\n" + "="*60)

def main():
    print("PowerShell Script Library - Installation Check")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        print("\nPlease upgrade to Python 3.8 or higher")
        return
    
    print("\nChecking required packages...")
    
    all_ok = True
    
    # Check for Qt bindings
    has_qt = False
    if check_package("PyQt6"):
        has_qt = True
        # Also check QScintilla for PyQt6
        check_package("PyQt6-QScintilla", "PyQt6.Qsci")
    elif check_package("PySide6"):
        has_qt = True
        print("⚠️  Note: Using PySide6 - some features may be limited")
    else:
        all_ok = False
    
    # Check other dependencies
    if not check_package("Pygments", "pygments"):
        all_ok = False
    
    # Check if sqlite3 is available (should be built-in)
    if not check_package("sqlite3"):
        print("⚠️  sqlite3 is not available - this should be included with Python")
        all_ok = False
    
    print("\n" + "="*60)
    
    if all_ok and has_qt:
        print("✓ All dependencies are installed!")
        print("\nYou can now run the application with:")
        print("  python main.py")
    else:
        print("✗ Some dependencies are missing")
        suggest_installation()

if __name__ == "__main__":
    main()