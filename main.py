#!/usr/bin/env python3
"""
PowerShell & Batch Script Library Manager
A modern VS Code-inspired GUI application for managing PowerShell and batch scripts.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from gui.main_window import MainWindow


def main():
    # Create the application
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("PowerShell & Batch Script Library")
    app.setOrganizationName("ScriptLibrary")
    app.setApplicationDisplayName("Script Library Manager")
    
    # High DPI scaling is automatic in PyQt6, no need to set attributes
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()