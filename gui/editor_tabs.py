from PyQt6.QtWidgets import (
    QTabWidget, QWidget, QVBoxLayout, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from PyQt6.Qsci import QsciScintilla
from typing import Dict, Optional
from database.models import Script
from core.script_manager import ScriptManager
from core.syntax_highlighter import SyntaxHighlighterFactory


class ScriptEditor(QsciScintilla):
    def __init__(self, script: Script):
        super().__init__()
        self.script = script
        self.original_content = script.content
        self.setup_editor()
        self.set_content(script.content)
        
    def setup_editor(self):
        # Editor settings
        self.setUtf8(True)
        self.setFont(QFont("Consolas", 10))
        
        # Line numbers
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#2b2b2b"))
        self.setMarginsForegroundColor(QColor("#858585"))
        
        # Indentation
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setAutoIndent(True)
        
        # Brace matching
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        
        # Current line highlighting
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#2a2a2a"))
        
        # Set lexer based on file type
        lexer = SyntaxHighlighterFactory.get_highlighter(self.script.file_type, self)
        if lexer:
            self.setLexer(lexer)
            
    def set_content(self, content: str):
        self.setText(content)
        self.setModified(False)
        
    def get_content(self) -> str:
        return self.text()
        
    def is_content_changed(self) -> bool:
        return self.get_content() != self.original_content
        
    def save_content(self):
        self.original_content = self.get_content()
        self.setModified(False)


class EditorTabWidget(QTabWidget):
    current_script_changed = pyqtSignal(Script)
    script_modified = pyqtSignal(Script, bool)
    cursor_position_changed = pyqtSignal(int, int)
    
    def __init__(self, script_manager: ScriptManager):
        super().__init__()
        self.script_manager = script_manager
        self.editors: Dict[int, ScriptEditor] = {}
        self.setup_ui()
        
    def setup_ui(self):
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        
        # Connect signals
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.on_tab_changed)
        
    def open_script(self, script: Script):
        # Check if already open
        if script.id in self.editors:
            # Switch to existing tab
            editor = self.editors[script.id]
            index = self.indexOf(editor)
            self.setCurrentIndex(index)
            return
            
        # Mark as opened
        self.script_manager.mark_script_opened(script.id)
        
        # Create new editor
        editor = ScriptEditor(script)
        self.editors[script.id] = editor
        
        # Add tab
        tab_name = f"{script.name}.{script.file_type}"
        index = self.addTab(editor, tab_name)
        self.setCurrentIndex(index)
        
        # Connect editor signals
        editor.textChanged.connect(lambda: self.on_text_changed(editor))
        editor.cursorPositionChanged.connect(
            lambda line, col: self.cursor_position_changed.emit(line + 1, col + 1)
        )
        
    def close_tab(self, index: int):
        editor = self.widget(index)
        if isinstance(editor, ScriptEditor):
            if editor.is_content_changed():
                reply = QMessageBox.question(
                    self,
                    "Unsaved Changes",
                    f"Save changes to {editor.script.name}?",
                    QMessageBox.StandardButton.Save |
                    QMessageBox.StandardButton.Discard |
                    QMessageBox.StandardButton.Cancel
                )
                
                if reply == QMessageBox.StandardButton.Save:
                    self.save_script(editor)
                elif reply == QMessageBox.StandardButton.Cancel:
                    return
                    
            # Remove from editors dict
            if editor.script.id in self.editors:
                del self.editors[editor.script.id]
                
        self.removeTab(index)
        
    def save_current_script(self):
        current_editor = self.currentWidget()
        if isinstance(current_editor, ScriptEditor):
            self.save_script(current_editor)
            
    def save_all_scripts(self):
        for editor in self.editors.values():
            if editor.is_content_changed():
                self.save_script(editor)
                
    def save_script(self, editor: ScriptEditor):
        editor.script.content = editor.get_content()
        if self.script_manager.update_script(editor.script):
            editor.save_content()
            self.update_tab_title(editor, modified=False)
            self.script_modified.emit(editor.script, False)
        else:
            QMessageBox.warning(self, "Error", "Failed to save script")
            
    def on_text_changed(self, editor: ScriptEditor):
        if editor.is_content_changed():
            self.update_tab_title(editor, modified=True)
            self.script_modified.emit(editor.script, True)
        else:
            self.update_tab_title(editor, modified=False)
            self.script_modified.emit(editor.script, False)
            
    def update_tab_title(self, editor: ScriptEditor, modified: bool):
        index = self.indexOf(editor)
        if index >= 0:
            tab_name = f"{editor.script.name}.{editor.script.file_type}"
            if modified:
                tab_name = f"● {tab_name}"
            self.setTabText(index, tab_name)
            
    def on_tab_changed(self, index: int):
        if index >= 0:
            editor = self.widget(index)
            if isinstance(editor, ScriptEditor):
                self.current_script_changed.emit(editor.script)
                # Update cursor position
                line, col = editor.getCursorPosition()
                self.cursor_position_changed.emit(line + 1, col + 1)
        else:
            self.current_script_changed.emit(None)
            
    def has_unsaved_changes(self) -> bool:
        for editor in self.editors.values():
            if editor.is_content_changed():
                return True
        return False
        
    def update_script_tab(self, script: Script):
        if script.id in self.editors:
            editor = self.editors[script.id]
            index = self.indexOf(editor)
            if index >= 0:
                tab_name = f"{script.name}.{script.file_type}"
                if editor.is_content_changed():
                    tab_name = f"● {tab_name}"
                self.setTabText(index, tab_name)
                
    def apply_theme(self, theme):
        # Apply theme to all open editors
        for editor in self.editors.values():
            if hasattr(theme, 'apply_to_editor'):
                theme.apply_to_editor(editor)