from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QMenu, QToolBar, QStatusBar, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from .folder_tree import FolderTreeWidget
from .editor_tabs import EditorTabWidget
from .properties_panel import PropertiesPanel
from .search_dialog import SearchDialog
from .theme_manager import ThemeManager
from core.script_manager import ScriptManager
from database.database import DatabaseManager
from database.models import Script, Folder


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.script_manager = ScriptManager(self.db_manager)
        self.theme_manager = ThemeManager()
        self.search_dialog = None
        
        self.setup_ui()
        self.setup_connections()
        self.apply_theme()
        
    def setup_ui(self):
        self.setWindowTitle("PowerShell & Batch Script Library")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create splitter for resizable panels
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.main_splitter)
        
        # Left panel - Folder tree
        self.folder_tree = FolderTreeWidget(self.script_manager)
        self.folder_tree.setMinimumWidth(200)
        self.folder_tree.setMaximumWidth(400)
        self.main_splitter.addWidget(self.folder_tree)
        
        # Center panel - Editor tabs
        self.editor_tabs = EditorTabWidget(self.script_manager)
        self.main_splitter.addWidget(self.editor_tabs)
        
        # Right panel - Properties
        self.properties_panel = PropertiesPanel(self.script_manager)
        self.properties_panel.setMinimumWidth(250)
        self.properties_panel.setMaximumWidth(400)
        self.main_splitter.addWidget(self.properties_panel)
        
        # Set initial splitter sizes
        self.main_splitter.setSizes([250, 900, 300])
        
        # Setup menu bar
        self.setup_menu_bar()
        
        # Setup toolbar
        self.setup_toolbar()
        
        # Setup status bar
        self.setup_status_bar()
        
    def setup_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        self.new_script_action = QAction("New &Script", self)
        self.new_script_action.setShortcut(QKeySequence.StandardKey.New)
        file_menu.addAction(self.new_script_action)
        
        self.new_folder_action = QAction("New &Folder", self)
        self.new_folder_action.setShortcut("Ctrl+Shift+N")
        file_menu.addAction(self.new_folder_action)
        
        file_menu.addSeparator()
        
        self.save_action = QAction("&Save", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        file_menu.addAction(self.save_action)
        
        self.save_all_action = QAction("Save &All", self)
        self.save_all_action.setShortcut("Ctrl+Shift+S")
        file_menu.addAction(self.save_all_action)
        
        file_menu.addSeparator()
        
        self.exit_action = QAction("E&xit", self)
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        file_menu.addAction(self.exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        self.search_action = QAction("&Find...", self)
        self.search_action.setShortcut(QKeySequence.StandardKey.Find)
        edit_menu.addAction(self.search_action)
        
        edit_menu.addSeparator()
        
        self.delete_action = QAction("&Delete", self)
        self.delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        edit_menu.addAction(self.delete_action)
        
        self.rename_action = QAction("&Rename", self)
        self.rename_action.setShortcut("F2")
        edit_menu.addAction(self.rename_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        self.toggle_folder_tree_action = QAction("Toggle &Folder Tree", self)
        self.toggle_folder_tree_action.setCheckable(True)
        self.toggle_folder_tree_action.setChecked(True)
        view_menu.addAction(self.toggle_folder_tree_action)
        
        self.toggle_properties_action = QAction("Toggle &Properties", self)
        self.toggle_properties_action.setCheckable(True)
        self.toggle_properties_action.setChecked(True)
        view_menu.addAction(self.toggle_properties_action)
        
        view_menu.addSeparator()
        
        self.theme_menu = view_menu.addMenu("&Theme")
        self.dark_theme_action = QAction("&Dark", self)
        self.dark_theme_action.setCheckable(True)
        self.dark_theme_action.setChecked(True)
        self.theme_menu.addAction(self.dark_theme_action)
        
        self.light_theme_action = QAction("&Light", self)
        self.light_theme_action.setCheckable(True)
        self.theme_menu.addAction(self.light_theme_action)
        
    def setup_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        toolbar.addAction(self.new_script_action)
        toolbar.addAction(self.new_folder_action)
        toolbar.addSeparator()
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.search_action)
        
    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Script info label
        self.script_info_label = QWidget()
        self.status_bar.addWidget(self.script_info_label)
        
        # Cursor position label
        self.cursor_pos_label = QWidget()
        self.status_bar.addPermanentWidget(self.cursor_pos_label)
        
    def setup_connections(self):
        # File menu actions
        self.new_script_action.triggered.connect(self.new_script)
        self.new_folder_action.triggered.connect(self.new_folder)
        self.save_action.triggered.connect(self.save_current_script)
        self.save_all_action.triggered.connect(self.save_all_scripts)
        self.exit_action.triggered.connect(self.close)
        
        # Edit menu actions
        self.search_action.triggered.connect(self.show_search_dialog)
        self.delete_action.triggered.connect(self.delete_selected)
        self.rename_action.triggered.connect(self.rename_selected)
        
        # View menu actions
        self.toggle_folder_tree_action.toggled.connect(self.toggle_folder_tree)
        self.toggle_properties_action.toggled.connect(self.toggle_properties_panel)
        self.dark_theme_action.triggered.connect(lambda: self.change_theme("dark"))
        self.light_theme_action.triggered.connect(lambda: self.change_theme("light"))
        
        # Folder tree signals
        self.folder_tree.script_selected.connect(self.open_script)
        self.folder_tree.folder_selected.connect(self.on_folder_selected)
        
        # Editor tabs signals
        self.editor_tabs.current_script_changed.connect(self.on_current_script_changed)
        self.editor_tabs.script_modified.connect(self.on_script_modified)
        self.editor_tabs.cursor_position_changed.connect(self.update_cursor_position)
        
        # Properties panel signals
        self.properties_panel.properties_changed.connect(self.on_properties_changed)
        
    def new_script(self):
        self.folder_tree.create_new_script()
        
    def new_folder(self):
        self.folder_tree.create_new_folder()
        
    def save_current_script(self):
        self.editor_tabs.save_current_script()
        
    def save_all_scripts(self):
        self.editor_tabs.save_all_scripts()
        
    def show_search_dialog(self):
        if not self.search_dialog:
            self.search_dialog = SearchDialog(self.script_manager, self)
            self.search_dialog.script_selected.connect(self.open_script)
        self.search_dialog.show()
        self.search_dialog.raise_()
        self.search_dialog.activateWindow()
        
    def delete_selected(self):
        self.folder_tree.delete_selected()
        
    def rename_selected(self):
        self.folder_tree.rename_selected()
        
    def toggle_folder_tree(self, checked):
        self.folder_tree.setVisible(checked)
        
    def toggle_properties_panel(self, checked):
        self.properties_panel.setVisible(checked)
        
    def change_theme(self, theme_name):
        self.theme_manager.set_theme(theme_name)
        self.apply_theme()
        self.dark_theme_action.setChecked(theme_name == "dark")
        self.light_theme_action.setChecked(theme_name == "light")
        
    def apply_theme(self):
        theme = self.theme_manager.get_current_theme()
        self.setStyleSheet(theme.get_app_stylesheet())
        self.editor_tabs.apply_theme(theme)
        
    def open_script(self, script: Script):
        self.editor_tabs.open_script(script)
        self.properties_panel.set_script(script)
        
    def on_folder_selected(self, folder: Folder):
        self.properties_panel.set_folder(folder)
        
    def on_current_script_changed(self, script: Script):
        if script:
            self.properties_panel.set_script(script)
            self.update_status_bar(f"Editing: {script.name}")
        else:
            self.properties_panel.clear()
            self.update_status_bar("Ready")
            
    def on_script_modified(self, script: Script, modified: bool):
        if modified:
            self.update_status_bar(f"Editing: {script.name} (modified)")
            
    def on_properties_changed(self, item):
        if isinstance(item, Script):
            self.editor_tabs.update_script_tab(item)
            self.folder_tree.refresh_item(item)
        elif isinstance(item, Folder):
            self.folder_tree.refresh_item(item)
            
    def update_cursor_position(self, line: int, column: int):
        self.status_bar.showMessage(f"Ln {line}, Col {column}", 0)
        
    def update_status_bar(self, message: str):
        self.status_bar.showMessage(message, 5000)
        
    def closeEvent(self, event):
        # Check for unsaved changes
        if self.editor_tabs.has_unsaved_changes():
            reply = QMessageBox.question(
                self, 
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them before closing?",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self.save_all_scripts()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()