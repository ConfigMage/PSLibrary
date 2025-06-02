#!/usr/bin/env python3
"""
System requirements checker for PowerShell Script Library
Checks Python version, dependencies, and system compatibility
"""

import sys
import platform
import subprocess
import os
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Print script header"""
    print("=" * 60)
    print("PowerShell Script Library - System Requirements Check")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version meets requirements"""
    print(f"{Colors.BOLD}Python Version Check:{Colors.RESET}")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"  Current version: {version_str}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"  {Colors.RED}✗ Python 3.10 or higher required{Colors.RESET}")
        return False
    elif version.minor > 12:
        print(f"  {Colors.YELLOW}⚠ Python {version_str} detected - not tested{Colors.RESET}")
        return True
    else:
        print(f"  {Colors.GREEN}✓ Python version compatible{Colors.RESET}")
        return True

def check_pip():
    """Check if pip is installed"""
    print(f"\n{Colors.BOLD}Pip Check:{Colors.RESET}")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  {Colors.GREEN}✓ pip is installed{Colors.RESET}")
            print(f"  {result.stdout.strip()}")
            return True
        else:
            print(f"  {Colors.RED}✗ pip is not installed{Colors.RESET}")
            return False
    except Exception as e:
        print(f"  {Colors.RED}✗ Error checking pip: {e}{Colors.RESET}")
        return False

def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print(f"\n{Colors.BOLD}Dependencies Check:{Colors.RESET}")
    
    dependencies = {
        "PyQt6": "PyQt6",
        "PyQt6.Qsci": "PyQt6-QScintilla",
        "pygments": "Pygments",
        "sqlite3": "sqlite3 (built-in)"
    }
    
    all_installed = True
    
    for module, display_name in dependencies.items():
        if check_package(module):
            print(f"  {Colors.GREEN}✓ {display_name} is installed{Colors.RESET}")
        else:
            print(f"  {Colors.RED}✗ {display_name} is NOT installed{Colors.RESET}")
            all_installed = False
    
    return all_installed

def check_system_info():
    """Display system information"""
    print(f"\n{Colors.BOLD}System Information:{Colors.RESET}")
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Architecture: {platform.machine()}")
    print(f"  Python executable: {sys.executable}")
    
    # Check for virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"  {Colors.BLUE}ℹ Running in virtual environment{Colors.RESET}")

def check_disk_space():
    """Check available disk space"""
    print(f"\n{Colors.BOLD}Disk Space Check:{Colors.RESET}")
    try:
        import shutil
        path = Path.cwd()
        stat = shutil.disk_usage(path)
        free_mb = stat.free // (1024 * 1024)
        
        if free_mb < 200:
            print(f"  {Colors.RED}✗ Low disk space: {free_mb}MB free{Colors.RESET}")
            print(f"    At least 200MB recommended")
            return False
        else:
            print(f"  {Colors.GREEN}✓ Sufficient disk space: {free_mb}MB free{Colors.RESET}")
            return True
    except Exception as e:
        print(f"  {Colors.YELLOW}⚠ Could not check disk space: {e}{Colors.RESET}")
        return True

def check_permissions():
    """Check file system permissions"""
    print(f"\n{Colors.BOLD}Permissions Check:{Colors.RESET}")
    test_file = Path("test_permissions.tmp")
    
    try:
        # Test write permissions
        test_file.write_text("test")
        test_file.unlink()
        print(f"  {Colors.GREEN}✓ Write permissions OK{Colors.RESET}")
        return True
    except Exception as e:
        print(f"  {Colors.RED}✗ No write permissions in current directory{Colors.RESET}")
        print(f"    Error: {e}")
        return False

def suggest_fixes(python_ok, pip_ok, deps_ok):
    """Suggest fixes for any issues found"""
    if python_ok and pip_ok and deps_ok:
        return
    
    print(f"\n{Colors.BOLD}Suggested Fixes:{Colors.RESET}")
    
    if not python_ok:
        print(f"\n{Colors.YELLOW}Python Version:{Colors.RESET}")
        print("  1. Download Python 3.10 or higher from https://www.python.org/")
        print("  2. During installation, check 'Add Python to PATH'")
    
    if not pip_ok:
        print(f"\n{Colors.YELLOW}Pip Installation:{Colors.RESET}")
        print("  1. Download get-pip.py from https://bootstrap.pypa.io/get-pip.py")
        print(f"  2. Run: {sys.executable} get-pip.py")
    
    if not deps_ok:
        print(f"\n{Colors.YELLOW}Missing Dependencies:{Colors.RESET}")
        print("  Run one of these commands:")
        print(f"    - Windows: cd .. && install.bat")
        print(f"    - Unix: cd .. && ./install.sh")
        print(f"    - Manual: {sys.executable} -m pip install -r ../requirements.txt")

def main():
    """Main function"""
    print_header()
    
    # Run all checks
    python_ok = check_python_version()
    pip_ok = check_pip()
    deps_ok = check_dependencies()
    check_system_info()
    disk_ok = check_disk_space()
    perms_ok = check_permissions()
    
    # Summary
    print(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
    all_ok = python_ok and pip_ok and deps_ok and disk_ok and perms_ok
    
    if all_ok:
        print(f"{Colors.GREEN}✓ All system requirements met!{Colors.RESET}")
        print(f"\nYou can run the application with:")
        print(f"  cd ..")
        print(f"  {sys.executable} main.py")
        return 0
    else:
        print(f"{Colors.RED}✗ Some requirements are not met{Colors.RESET}")
        suggest_fixes(python_ok, pip_ok, deps_ok)
        return 1

if __name__ == "__main__":
    sys.exit(main())