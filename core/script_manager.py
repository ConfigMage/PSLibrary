from typing import List, Optional, Dict, Any
from database.database import DatabaseManager
from database.models import Script, Folder


class ScriptManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self._script_cache: Dict[int, Script] = {}
        self._folder_cache: Dict[int, Folder] = {}
    
    # Script operations
    def create_script(self, name: str, folder_id: Optional[int] = None, 
                     file_type: str = "ps1", content: str = "") -> Script:
        script = Script(
            name=name,
            folder_id=folder_id,
            file_type=file_type,
            content=content
        )
        script.id = self.db.create_script(script)
        self._script_cache[script.id] = script
        return script
    
    def get_script(self, script_id: int) -> Optional[Script]:
        if script_id in self._script_cache:
            return self._script_cache[script_id]
        
        script = self.db.get_script(script_id)
        if script:
            self._script_cache[script_id] = script
        return script
    
    def update_script(self, script: Script) -> bool:
        success = self.db.update_script(script)
        if success:
            self._script_cache[script.id] = script
        return success
    
    def delete_script(self, script_id: int) -> bool:
        success = self.db.delete_script(script_id)
        if success and script_id in self._script_cache:
            del self._script_cache[script_id]
        return success
    
    def mark_script_opened(self, script_id: int) -> bool:
        success = self.db.update_script_last_opened(script_id)
        if success and script_id in self._script_cache:
            script = self._script_cache[script_id]
            from datetime import datetime
            script.last_opened_date = datetime.now()
        return success
    
    def get_scripts_by_folder(self, folder_id: Optional[int]) -> List[Script]:
        return self.db.get_scripts_by_folder(folder_id)
    
    def search_scripts(self, query: str) -> List[Script]:
        return self.db.search_scripts(query)
    
    # Folder operations
    def create_folder(self, name: str, parent_id: Optional[int] = None) -> Folder:
        path = self._calculate_folder_path(name, parent_id)
        folder = Folder(
            name=name,
            parent_id=parent_id,
            path=path
        )
        folder.id = self.db.create_folder(folder)
        self._folder_cache[folder.id] = folder
        return folder
    
    def get_folder(self, folder_id: int) -> Optional[Folder]:
        if folder_id in self._folder_cache:
            return self._folder_cache[folder_id]
        
        folder = self.db.get_folder(folder_id)
        if folder:
            self._folder_cache[folder_id] = folder
        return folder
    
    def update_folder(self, folder: Folder) -> bool:
        # Update path when parent changes
        folder.path = self._calculate_folder_path(folder.name, folder.parent_id)
        success = self.db.update_folder(folder)
        if success:
            self._folder_cache[folder.id] = folder
            # Update paths of child folders
            self._update_child_folder_paths(folder.id)
        return success
    
    def delete_folder(self, folder_id: int) -> bool:
        # Check if folder has scripts or subfolders
        scripts = self.get_scripts_by_folder(folder_id)
        children = self.get_child_folders(folder_id)
        
        if scripts or children:
            return False  # Don't delete non-empty folders
        
        success = self.db.delete_folder(folder_id)
        if success and folder_id in self._folder_cache:
            del self._folder_cache[folder_id]
        return success
    
    def get_all_folders(self) -> List[Folder]:
        folders = self.db.get_all_folders()
        for folder in folders:
            self._folder_cache[folder.id] = folder
        return folders
    
    def get_child_folders(self, parent_id: Optional[int]) -> List[Folder]:
        return self.db.get_child_folders(parent_id)
    
    def move_folder(self, folder_id: int, new_parent_id: Optional[int]) -> bool:
        folder = self.get_folder(folder_id)
        if not folder:
            return False
        
        # Check for circular reference
        if new_parent_id and self._would_create_circular_reference(folder_id, new_parent_id):
            return False
        
        folder.parent_id = new_parent_id
        return self.update_folder(folder)
    
    def move_script(self, script_id: int, new_folder_id: Optional[int]) -> bool:
        script = self.get_script(script_id)
        if not script:
            return False
        
        script.folder_id = new_folder_id
        return self.update_script(script)
    
    # Helper methods
    def _calculate_folder_path(self, name: str, parent_id: Optional[int]) -> str:
        if parent_id is None:
            return f"/{name}"
        
        parent = self.get_folder(parent_id)
        if parent:
            return f"{parent.path}/{name}"
        return f"/{name}"
    
    def _update_child_folder_paths(self, parent_id: int):
        children = self.get_child_folders(parent_id)
        for child in children:
            child.path = self._calculate_folder_path(child.name, child.parent_id)
            self.db.update_folder(child)
            self._folder_cache[child.id] = child
            # Recursively update children
            self._update_child_folder_paths(child.id)
    
    def _would_create_circular_reference(self, folder_id: int, target_parent_id: int) -> bool:
        current_id = target_parent_id
        while current_id is not None:
            if current_id == folder_id:
                return True
            parent = self.get_folder(current_id)
            current_id = parent.parent_id if parent else None
        return False
    
    def get_folder_tree(self) -> Dict[Optional[int], List[Folder]]:
        all_folders = self.get_all_folders()
        tree: Dict[Optional[int], List[Folder]] = {}
        
        for folder in all_folders:
            parent_id = folder.parent_id
            if parent_id not in tree:
                tree[parent_id] = []
            tree[parent_id].append(folder)
        
        return tree