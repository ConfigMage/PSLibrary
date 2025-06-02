"""
Compatibility layer for PyQt6 and PySide6
"""

try:
    # Try PyQt6 first
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    from PyQt6.Qsci import *
    QT_BINDING = "PyQt6"
    print("Using PyQt6")
except ImportError:
    try:
        # Fall back to PySide6
        from PySide6.QtWidgets import *
        from PySide6.QtCore import *
        from PySide6.QtGui import *
        # Note: QScintilla might need separate handling for PySide6
        QT_BINDING = "PySide6"
        print("Using PySide6")
        print("Warning: QScintilla support may be limited with PySide6")
    except ImportError:
        raise ImportError(
            "Neither PyQt6 nor PySide6 could be imported. "
            "Please install one of them:\n"
            "  pip install PyQt6==6.5.0\n"
            "  or\n"
            "  pip install PySide6==6.5.0"
        )