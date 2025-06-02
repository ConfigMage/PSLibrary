from PyQt6.QtWidgets import (
    QTreeWidget, QTreeWidgetItem, QMenu, QInputDialog,
    QMessageBox, QAbstractItemView, QHeaderView, QStyle
)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, QByteArray
from PyQt6.QtGui import QAction, QDrag, QIcon, QPalette
from typing import Optional, Dict
import json
from database.models import Script, Folder
from core.script_manager import ScriptManager


class FolderTreeItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.item_data = None
        self.item_type = None
        
    def set_data(self, data, item_type: str):
        self.item_data = data
        self.item_type = item_type
        
        if item_type == "folder":
            self.setText(0, data.name)
            # Use system folder icon
            if self.treeWidget():
                folder_icon = self.treeWidget().style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
                self.setIcon(0, folder_icon)
            self.setData(0, Qt.ItemDataRole.UserRole, ("folder", data.id))
        elif item_type == "script":
            display_name = f"{data.name}.{data.file_type}"
            self.setText(0, display_name)
            # Use file icon
            if self.treeWidget():
                file_icon = self.treeWidget().style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
                self.setIcon(0, file_icon)
            self.setData(0, Qt.ItemDataRole.UserRole, ("script", data.id))


class FolderTreeWidget(QTreeWidget):
    script_selected = pyqtSignal(Script)
    folder_selected = pyqtSignal(Folder)
    
    def __init__(self, script_manager: ScriptManager):
        super().__init__()
        self.script_manager = script_manager
        self.item_map: Dict[tuple, FolderTreeItem] = {}
        
        self.setup_ui()
        self.load_tree()
        
    def setup_ui(self):
        self.setHeaderLabel("Explorer")
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # Enable drag and drop
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setAcceptDrops(True)
        
        # Selection behavior
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
        # Tree appearance
        self.setIndentation(20)
        self.setAnimated(True)
        self.setUniformRowHeights(True)
        
        # Show lines connecting items
        self.setRootIsDecorated(True)
        
        # Header appearance
        header = self.header()
        header.setStretchLastSection(True)
        
        # Connect signals
        self.itemClicked.connect(self.on_item_clicked)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.itemExpanded.connect(self.on_item_expanded)
        self.itemCollapsed.connect(self.on_item_collapsed)
        
    def load_tree(self):
        self.clear()
        self.item_map.clear()
        
        # Get folder tree structure
        folder_tree = self.script_manager.get_folder_tree()
        
        # Create root folders
        self._create_folder_items(None, folder_tree)
        
        # Load scripts for root level
        root_scripts = self.script_manager.get_scripts_by_folder(None)
        for script in root_scripts:
            self._create_script_item(None, script)
        
    def _create_folder_items(self, parent_item: Optional[FolderTreeItem], 
                           folder_tree: Dict):
        parent_id = parent_item.item_data.id if parent_item else None
        
        # Create folders for this level
        for folder in folder_tree.get(parent_id, []):
            folder_item = self._create_folder_item(parent_item, folder)
            
            # Recursively create subfolders
            self._create_folder_items(folder_item, folder_tree)
            
            # Add scripts to this folder
            scripts = self.script_manager.get_scripts_by_folder(folder.id)
            for script in scripts:
                self._create_script_item(folder_item, script)
                    
    def _create_folder_item(self, parent: Optional[FolderTreeItem], 
                          folder: Folder) -> FolderTreeItem:
        if parent:
            item = FolderTreeItem(parent)
        else:
            item = FolderTreeItem(self)
            
        item.set_data(folder, "folder")
        self.item_map[("folder", folder.id)] = item
        return item
        
    def _create_script_item(self, parent: Optional[FolderTreeItem], 
                          script: Script) -> FolderTreeItem:
        if parent:
            item = FolderTreeItem(parent)
        else:
            item = FolderTreeItem(self)
            
        item.set_data(script, "script")
        self.item_map[("script", script.id)] = item
        return item
        
    def on_item_clicked(self, item: FolderTreeItem, column: int):
        if item.item_type == "folder":
            self.folder_selected.emit(item.item_data)
        elif item.item_type == "script":
            self.script_selected.emit(item.item_data)
            
    def on_item_double_clicked(self, item: FolderTreeItem, column: int):
        if item.item_type == "script":
            self.script_selected.emit(item.item_data)
            
    def on_item_expanded(self, item: FolderTreeItem):
        # Update folder icon to open folder
        if item.item_type == "folder" and self.style():
            open_folder_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon)
            item.setIcon(0, open_folder_icon)
            
    def on_item_collapsed(self, item: FolderTreeItem):
        # Update folder icon to closed folder
        if item.item_type == "folder" and self.style():
            folder_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
            item.setIcon(0, folder_icon)
            
    def show_context_menu(self, position):
        item = self.itemAt(position)
        menu = QMenu(self)
        
        if item and item.item_type == "folder":
            # Folder context menu
            new_script_action = QAction("New Script", self)
            new_script_action.triggered.connect(
                lambda: self.create_new_script(item.item_data.id)
            )
            menu.addAction(new_script_action)
            
            new_folder_action = QAction("New Folder", self)
            new_folder_action.triggered.connect(
                lambda: self.create_new_folder(item.item_data.id)
            )
            menu.addAction(new_folder_action)
            
            menu.addSeparator()
            
            rename_action = QAction("Rename", self)
            rename_action.triggered.connect(lambda: self.rename_item(item))
            menu.addAction(rename_action)
            
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.delete_item(item))
            menu.addAction(delete_action)
            
        elif item and item.item_type == "script":
            # Script context menu
            open_action = QAction("Open", self)
            open_action.triggered.connect(
                lambda: self.script_selected.emit(item.item_data)
            )
            menu.addAction(open_action)
            
            menu.addSeparator()
            
            rename_action = QAction("Rename", self)
            rename_action.triggered.connect(lambda: self.rename_item(item))
            menu.addAction(rename_action)
            
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.delete_item(item))
            menu.addAction(delete_action)
            
        else:
            # Root context menu
            new_script_action = QAction("New Script", self)
            new_script_action.triggered.connect(lambda: self.create_new_script(None))
            menu.addAction(new_script_action)
            
            new_folder_action = QAction("New Folder", self)
            new_folder_action.triggered.connect(lambda: self.create_new_folder(None))
            menu.addAction(new_folder_action)
            
        menu.exec(self.mapToGlobal(position))
        
    def create_new_script(self, folder_id: Optional[int] = None):
        name, ok = QInputDialog.getText(self, "New Script", "Script name:")
        if ok and name:
            # Remove extension if provided
            if name.endswith('.ps1') or name.endswith('.bat'):
                name = name[:-4]
                
            file_type, ok = QInputDialog.getItem(
                self, "Script Type", "Select script type:",
                ["ps1", "bat"], 0, False
            )
            
            if ok:
                script = self.script_manager.create_script(
                    name=name,
                    folder_id=folder_id,
                    file_type=file_type
                )
                
                # Find parent item
                parent_item = None
                if folder_id:
                    parent_item = self.item_map.get(("folder", folder_id))
                    # Expand parent folder to show the new script
                    if parent_item:
                        parent_item.setExpanded(True)
                    
                # Create tree item
                self._create_script_item(parent_item, script)
                
                # Select and open the new script
                new_item = self.item_map.get(("script", script.id))
                if new_item:
                    self.setCurrentItem(new_item)
                    self.script_selected.emit(script)
                    
    def create_new_folder(self, parent_id: Optional[int] = None):
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and name:
            folder = self.script_manager.create_folder(
                name=name,
                parent_id=parent_id
            )
            
            # Find parent item
            parent_item = None
            if parent_id:
                parent_item = self.item_map.get(("folder", parent_id))
                
            # Create tree item
            new_item = self._create_folder_item(parent_item, folder)
            
            # Expand parent if exists
            if parent_item:
                parent_item.setExpanded(True)
            
            # Select the new folder
            self.setCurrentItem(new_item)
            self.folder_selected.emit(folder)
            
    def rename_item(self, item: FolderTreeItem):
        old_name = item.item_data.name
        new_name, ok = QInputDialog.getText(
            self, "Rename", "New name:", text=old_name
        )
        
        if ok and new_name and new_name != old_name:
            if item.item_type == "folder":
                item.item_data.name = new_name
                if self.script_manager.update_folder(item.item_data):
                    item.setText(0, new_name)
                else:
                    QMessageBox.warning(self, "Error", "Failed to rename folder")
                    
            elif item.item_type == "script":
                # Remove extension if provided
                if new_name.endswith('.ps1') or new_name.endswith('.bat'):
                    new_name = new_name[:-4]
                    
                item.item_data.name = new_name
                if self.script_manager.update_script(item.item_data):
                    display_name = f"{new_name}.{item.item_data.file_type}"
                    item.setText(0, display_name)
                else:
                    QMessageBox.warning(self, "Error", "Failed to rename script")
                    
    def delete_item(self, item: FolderTreeItem):
        msg = f"Are you sure you want to delete '{item.item_data.name}'?"
        reply = QMessageBox.question(
            self, "Confirm Delete", msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if item.item_type == "folder":
                if self.script_manager.delete_folder(item.item_data.id):
                    # Remove from tree
                    parent = item.parent() or self.invisibleRootItem()
                    parent.removeChild(item)
                    del self.item_map[("folder", item.item_data.id)]
                else:
                    QMessageBox.warning(
                        self, "Error", 
                        "Cannot delete folder. Make sure it's empty."
                    )
                    
            elif item.item_type == "script":
                if self.script_manager.delete_script(item.item_data.id):
                    # Remove from tree
                    parent = item.parent() or self.invisibleRootItem()
                    parent.removeChild(item)
                    del self.item_map[("script", item.item_data.id)]
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete script")
                    
    def delete_selected(self):
        item = self.currentItem()
        if isinstance(item, FolderTreeItem):
            self.delete_item(item)
            
    def rename_selected(self):
        item = self.currentItem()
        if isinstance(item, FolderTreeItem):
            self.rename_item(item)
            
    def refresh_item(self, data):
        if isinstance(data, Folder):
            item = self.item_map.get(("folder", data.id))
            if item:
                item.setText(0, data.name)
        elif isinstance(data, Script):
            item = self.item_map.get(("script", data.id))
            if item:
                display_name = f"{data.name}.{data.file_type}"
                item.setText(0, display_name)
                
    def refresh(self):
        """Reload the entire tree while preserving expansion state"""
        # Save expansion state
        expanded_folders = set()
        for key, item in self.item_map.items():
            if key[0] == "folder" and item.isExpanded():
                expanded_folders.add(key[1])
        
        # Save current selection
        current = self.currentItem()
        current_key = None
        if isinstance(current, FolderTreeItem):
            current_key = (current.item_type, current.item_data.id)
        
        # Reload tree
        self.load_tree()
        
        # Restore expansion state
        for folder_id in expanded_folders:
            item = self.item_map.get(("folder", folder_id))
            if item:
                item.setExpanded(True)
        
        # Restore selection
        if current_key and current_key in self.item_map:
            self.setCurrentItem(self.item_map[current_key])
                
    # Drag and drop support
    def mimeData(self, items):
        mime_data = QMimeData()
        if items:
            item = items[0]
            if isinstance(item, FolderTreeItem):
                data = {
                    "type": item.item_type,
                    "id": item.item_data.id
                }
                mime_data.setText(json.dumps(data))
        return mime_data
        
    def dropMimeData(self, parent, index, data, action):
        if not data.hasText():
            return False
            
        try:
            drop_data = json.loads(data.text())
            item_type = drop_data["type"]
            item_id = drop_data["id"]
            
            # Determine target folder
            target_folder_id = None
            if parent and isinstance(parent, FolderTreeItem):
                if parent.item_type == "folder":
                    target_folder_id = parent.item_data.id
                elif parent.item_type == "script":
                    # Drop on script - use its parent folder
                    target_folder_id = parent.item_data.folder_id
                    
            # Perform the move
            if item_type == "folder":
                success = self.script_manager.move_folder(item_id, target_folder_id)
            elif item_type == "script":
                success = self.script_manager.move_script(item_id, target_folder_id)
            else:
                return False
                
            if success:
                # Reload tree to reflect changes
                self.load_tree()
                return True
                
        except Exception as e:
            print(f"Drop error: {e}")
            
        return False