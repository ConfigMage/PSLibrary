from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication
from dataclasses import dataclass
from typing import Dict


@dataclass
class Theme:
    name: str
    colors: Dict[str, str]
    
    def get_app_stylesheet(self) -> str:
        return f"""
        QMainWindow {{
            background-color: {self.colors['background']};
            color: {self.colors['text']};
        }}
        
        QWidget {{
            background-color: {self.colors['background']};
            color: {self.colors['text']};
        }}
        
        QTreeWidget {{
            background-color: {self.colors['sidebar']};
            border: none;
            outline: none;
        }}
        
        QTreeWidget::item {{
            padding: 4px;
            border-radius: 2px;
        }}
        
        QTreeWidget::item:selected {{
            background-color: {self.colors['selection']};
        }}
        
        QTreeWidget::item:hover {{
            background-color: {self.colors['hover']};
        }}
        
        QTabWidget::pane {{
            background-color: {self.colors['editor_bg']};
            border: none;
        }}
        
        QTabBar {{
            background-color: {self.colors['tab_bar']};
        }}
        
        QTabBar::tab {{
            background-color: {self.colors['tab_inactive']};
            color: {self.colors['text']};
            padding: 8px 16px;
            margin-right: 2px;
            border: none;
        }}
        
        QTabBar::tab:selected {{
            background-color: {self.colors['tab_active']};
        }}
        
        QTabBar::tab:hover {{
            background-color: {self.colors['hover']};
        }}
        
        QGroupBox {{
            border: 1px solid {self.colors['border']};
            border-radius: 4px;
            margin-top: 8px;
            padding-top: 8px;
            font-weight: bold;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }}
        
        QLineEdit, QTextEdit, QComboBox {{
            background-color: {self.colors['input_bg']};
            border: 1px solid {self.colors['border']};
            border-radius: 3px;
            padding: 4px;
            color: {self.colors['text']};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
            border-color: {self.colors['accent']};
        }}
        
        QLineEdit:read-only {{
            background-color: {self.colors['readonly_bg']};
            color: {self.colors['readonly_text']};
        }}
        
        QPushButton {{
            background-color: {self.colors['button_bg']};
            border: 1px solid {self.colors['border']};
            border-radius: 3px;
            padding: 6px 12px;
            color: {self.colors['button_text']};
        }}
        
        QPushButton:hover {{
            background-color: {self.colors['button_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: {self.colors['button_pressed']};
        }}
        
        QMenuBar {{
            background-color: {self.colors['menubar']};
            border-bottom: 1px solid {self.colors['border']};
        }}
        
        QMenuBar::item:selected {{
            background-color: {self.colors['hover']};
        }}
        
        QMenu {{
            background-color: {self.colors['menu_bg']};
            border: 1px solid {self.colors['border']};
        }}
        
        QMenu::item:selected {{
            background-color: {self.colors['selection']};
        }}
        
        QToolBar {{
            background-color: {self.colors['toolbar']};
            border-bottom: 1px solid {self.colors['border']};
            spacing: 3px;
            padding: 4px;
        }}
        
        QStatusBar {{
            background-color: {self.colors['statusbar']};
            border-top: 1px solid {self.colors['border']};
        }}
        
        QScrollBar:vertical {{
            background-color: {self.colors['scrollbar_bg']};
            width: 12px;
            border: none;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {self.colors['scrollbar_handle']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {self.colors['scrollbar_hover']};
        }}
        
        QSplitter::handle {{
            background-color: {self.colors['border']};
            width: 1px;
        }}
        """
        
    def apply_to_editor(self, editor):
        # Apply theme colors to QScintilla editor
        editor.setCaretLineBackgroundColor(QColor(self.colors['editor_line_highlight']))
        editor.setMarginsBackgroundColor(QColor(self.colors['editor_margin_bg']))
        editor.setMarginsForegroundColor(QColor(self.colors['editor_margin_fg']))
        
        # Update paper and default colors for the entire editor
        editor.setPaper(QColor(self.colors['editor_bg']))
        editor.setColor(QColor(self.colors['text']))
        
        # Set colors for all styles (0-127)
        for style in range(128):
            editor.setPaper(QColor(self.colors['editor_bg']), style)
        
        # Update lexer colors if available
        lexer = editor.lexer()
        if lexer:
            lexer.setDefaultPaper(QColor(self.colors['editor_bg']))
            lexer.setDefaultColor(QColor(self.colors['text']))


class ThemeManager:
    def __init__(self):
        self.dark_theme = Theme(
            name="dark",
            colors={
                "background": "#1e1e1e",
                "text": "#ffffff",
                "sidebar": "#252526",
                "editor_bg": "#1e1e1e",
                "selection": "#094771",
                "hover": "#2a2d2e",
                "border": "#464647",
                "tab_bar": "#2d2d30",
                "tab_active": "#1e1e1e",
                "tab_inactive": "#2d2d30",
                "input_bg": "#3c3c3c",
                "readonly_bg": "#2d2d30",
                "readonly_text": "#969696",
                "button_bg": "#0e639c",
                "button_text": "#ffffff",
                "button_hover": "#1177bb",
                "button_pressed": "#094771",
                "accent": "#007acc",
                "menubar": "#3c3c3c",
                "menu_bg": "#252526",
                "toolbar": "#2d2d30",
                "statusbar": "#007acc",
                "scrollbar_bg": "#1e1e1e",
                "scrollbar_handle": "#464647",
                "scrollbar_hover": "#5a5a5a",
                "editor_line_highlight": "#2a2a2a",
                "editor_margin_bg": "#2b2b2b",
                "editor_margin_fg": "#858585"
            }
        )
        
    def get_current_theme(self) -> Theme:
        return self.dark_theme