from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from database.models import Script
from core.script_manager import ScriptManager


class SearchDialog(QDialog):
    script_selected = pyqtSignal(Script)
    
    def __init__(self, script_manager: ScriptManager, parent=None):
        super().__init__(parent)
        self.script_manager = script_manager
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Search Scripts")
        self.setModal(False)
        self.resize(600, 400)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Search input
        search_layout = QHBoxLayout()
        layout.addLayout(search_layout)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, content, or description...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        search_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        search_layout.addWidget(self.search_button)
        
        # Results label
        self.results_label = QLabel("Enter search terms above")
        layout.addWidget(self.results_label)
        
        # Results list
        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.results_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        button_layout.addStretch()
        
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_selected_script)
        self.open_button.setEnabled(False)
        button_layout.addWidget(self.open_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        # Connect selection change
        self.results_list.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Focus search input
        self.search_input.setFocus()
        
    def on_search_text_changed(self, text: str):
        # Debounce search to avoid too many queries
        self.search_timer.stop()
        if text.strip():
            self.search_timer.start(300)  # 300ms delay
            
    def perform_search(self):
        query = self.search_input.text().strip()
        if not query:
            self.results_list.clear()
            self.results_label.setText("Enter search terms above")
            return
            
        # Perform search
        results = self.script_manager.search_scripts(query)
        
        # Update UI
        self.results_list.clear()
        
        if results:
            self.results_label.setText(f"Found {len(results)} script(s)")
            
            for script in results:
                item = QListWidgetItem()
                item.setText(f"{script.name}.{script.file_type}")
                
                # Add description as tooltip if available
                if script.description:
                    item.setToolTip(script.description)
                    
                # Store script reference
                item.setData(Qt.ItemDataRole.UserRole, script)
                
                self.results_list.addItem(item)
        else:
            self.results_label.setText("No scripts found")
            
    def on_selection_changed(self):
        has_selection = bool(self.results_list.selectedItems())
        self.open_button.setEnabled(has_selection)
        
    def on_item_double_clicked(self, item: QListWidgetItem):
        script = item.data(Qt.ItemDataRole.UserRole)
        if script:
            self.script_selected.emit(script)
            self.accept()
            
    def open_selected_script(self):
        selected_items = self.results_list.selectedItems()
        if selected_items:
            script = selected_items[0].data(Qt.ItemDataRole.UserRole)
            if script:
                self.script_selected.emit(script)
                self.accept()