from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit,
    QComboBox, QLabel, QPushButton, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Union, Optional
from database.models import Script, Folder
from core.script_manager import ScriptManager


class PropertiesPanel(QWidget):
    properties_changed = pyqtSignal(object)  # Script or Folder
    
    def __init__(self, script_manager: ScriptManager):
        super().__init__()
        self.script_manager = script_manager
        self.current_item = None
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        self.title_label = QLabel("Properties")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.title_label)
        
        # Scroll area for properties
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        layout.addWidget(scroll)
        
        # Container widget
        self.container = QWidget()
        scroll.setWidget(self.container)
        self.container_layout = QVBoxLayout(self.container)
        
        # Script properties group
        self.script_group = QGroupBox("Script Properties")
        self.script_layout = QFormLayout()
        self.script_group.setLayout(self.script_layout)
        self.container_layout.addWidget(self.script_group)
        
        # Script fields
        self.script_name = QLineEdit()
        self.script_layout.addRow("Name:", self.script_name)
        
        self.script_type = QComboBox()
        self.script_type.addItems(["ps1", "bat"])
        self.script_layout.addRow("Type:", self.script_type)
        
        self.script_author = QLineEdit()
        self.script_layout.addRow("Author:", self.script_author)
        
        self.script_env = QComboBox()
        self.script_env.addItems(["Testing", "Production"])
        self.script_layout.addRow("Environment:", self.script_env)
        
        self.script_description = QTextEdit()
        self.script_description.setMaximumHeight(100)
        self.script_layout.addRow("Description:", self.script_description)
        
        # Folder properties group
        self.folder_group = QGroupBox("Folder Properties")
        self.folder_layout = QFormLayout()
        self.folder_group.setLayout(self.folder_layout)
        self.container_layout.addWidget(self.folder_group)
        
        # Folder fields
        self.folder_name = QLineEdit()
        self.folder_layout.addRow("Name:", self.folder_name)
        
        self.folder_path = QLineEdit()
        self.folder_path.setReadOnly(True)
        self.folder_layout.addRow("Path:", self.folder_path)
        
        # Metadata group
        self.metadata_group = QGroupBox("Metadata")
        self.metadata_layout = QFormLayout()
        self.metadata_group.setLayout(self.metadata_layout)
        self.container_layout.addWidget(self.metadata_group)
        
        # Metadata fields
        self.created_date = QLineEdit()
        self.created_date.setReadOnly(True)
        self.metadata_layout.addRow("Created:", self.created_date)
        
        self.modified_date = QLineEdit()
        self.modified_date.setReadOnly(True)
        self.metadata_layout.addRow("Modified:", self.modified_date)
        
        self.last_opened = QLineEdit()
        self.last_opened.setReadOnly(True)
        self.metadata_layout.addRow("Last Opened:", self.last_opened)
        
        # Save button
        self.save_button = QPushButton("Save Properties")
        self.save_button.clicked.connect(self.save_properties)
        self.container_layout.addWidget(self.save_button)
        
        # Spacer
        self.container_layout.addStretch()
        
        # Initially hide all groups
        self.clear()
        
    def set_script(self, script: Script):
        self.current_item = script
        
        # Show script properties, hide folder properties
        self.script_group.setVisible(True)
        self.folder_group.setVisible(False)
        self.metadata_group.setVisible(True)
        self.save_button.setVisible(True)
        
        # Populate fields
        self.script_name.setText(script.name)
        self.script_type.setCurrentText(script.file_type)
        self.script_author.setText(script.author)
        self.script_env.setCurrentText(script.environment_tag)
        self.script_description.setText(script.description)
        
        # Metadata
        self.created_date.setText(script.created_date.strftime("%Y-%m-%d %H:%M"))
        self.modified_date.setText(script.modified_date.strftime("%Y-%m-%d %H:%M"))
        self.last_opened.setText(script.last_opened_date.strftime("%Y-%m-%d %H:%M"))
        
        self.title_label.setText(f"Properties - {script.name}.{script.file_type}")
        
    def set_folder(self, folder: Folder):
        self.current_item = folder
        
        # Show folder properties, hide script properties
        self.script_group.setVisible(False)
        self.folder_group.setVisible(True)
        self.metadata_group.setVisible(True)
        self.save_button.setVisible(True)
        
        # Populate fields
        self.folder_name.setText(folder.name)
        self.folder_path.setText(folder.path)
        
        # Metadata
        self.created_date.setText(folder.created_date.strftime("%Y-%m-%d %H:%M"))
        self.modified_date.setText("")
        self.last_opened.setText("")
        
        self.title_label.setText(f"Properties - {folder.name}")
        
    def clear(self):
        self.current_item = None
        self.script_group.setVisible(False)
        self.folder_group.setVisible(False)
        self.metadata_group.setVisible(False)
        self.save_button.setVisible(False)
        self.title_label.setText("Properties")
        
        # Clear all fields
        self.script_name.clear()
        self.script_author.clear()
        self.script_description.clear()
        self.folder_name.clear()
        self.folder_path.clear()
        self.created_date.clear()
        self.modified_date.clear()
        self.last_opened.clear()
        
    def save_properties(self):
        if isinstance(self.current_item, Script):
            # Update script properties
            self.current_item.name = self.script_name.text()
            self.current_item.file_type = self.script_type.currentText()
            self.current_item.author = self.script_author.text()
            self.current_item.environment_tag = self.script_env.currentText()
            self.current_item.description = self.script_description.toPlainText()
            
            if self.script_manager.update_script(self.current_item):
                self.properties_changed.emit(self.current_item)
                # Refresh modified date
                self.modified_date.setText(
                    self.current_item.modified_date.strftime("%Y-%m-%d %H:%M")
                )
                
        elif isinstance(self.current_item, Folder):
            # Update folder properties
            old_name = self.current_item.name
            new_name = self.folder_name.text()
            
            if new_name and new_name != old_name:
                self.current_item.name = new_name
                if self.script_manager.update_folder(self.current_item):
                    self.properties_changed.emit(self.current_item)
                    # Refresh path
                    self.folder_path.setText(self.current_item.path)