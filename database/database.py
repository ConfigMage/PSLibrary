import sqlite3
import os
from typing import List, Optional, Tuple
from datetime import datetime
from contextlib import contextmanager
from .models import Folder, Script


class DatabaseManager:
    def __init__(self, db_path: str = "script_library.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create folders table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS folders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    parent_id INTEGER,
                    created_date TIMESTAMP NOT NULL,
                    path TEXT NOT NULL,
                    FOREIGN KEY (parent_id) REFERENCES folders(id) ON DELETE CASCADE
                )
            ''')
            
            # Create scripts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scripts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    folder_id INTEGER,
                    content TEXT NOT NULL DEFAULT '',
                    description TEXT NOT NULL DEFAULT '',
                    author TEXT NOT NULL DEFAULT '',
                    environment_tag TEXT NOT NULL DEFAULT 'Testing',
                    file_type TEXT NOT NULL DEFAULT 'ps1',
                    created_date TIMESTAMP NOT NULL,
                    modified_date TIMESTAMP NOT NULL,
                    last_opened_date TIMESTAMP NOT NULL,
                    FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE CASCADE
                )
            ''')
            
            # Create indexes for better search performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_scripts_name ON scripts(name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_scripts_content ON scripts(content)')
    
    # Folder operations
    def create_folder(self, folder: Folder) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO folders (name, parent_id, created_date, path)
                VALUES (?, ?, ?, ?)
            ''', (folder.name, folder.parent_id, folder.created_date, folder.path))
            return cursor.lastrowid
    
    def get_folder(self, folder_id: int) -> Optional[Folder]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM folders WHERE id = ?', (folder_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_folder(row)
            return None
    
    def get_all_folders(self) -> List[Folder]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM folders ORDER BY name')
            return [self._row_to_folder(row) for row in cursor.fetchall()]
    
    def get_child_folders(self, parent_id: Optional[int]) -> List[Folder]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if parent_id is None:
                cursor.execute('SELECT * FROM folders WHERE parent_id IS NULL ORDER BY name')
            else:
                cursor.execute('SELECT * FROM folders WHERE parent_id = ? ORDER BY name', (parent_id,))
            return [self._row_to_folder(row) for row in cursor.fetchall()]
    
    def update_folder(self, folder: Folder) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE folders 
                SET name = ?, parent_id = ?, path = ?
                WHERE id = ?
            ''', (folder.name, folder.parent_id, folder.path, folder.id))
            return cursor.rowcount > 0
    
    def delete_folder(self, folder_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM folders WHERE id = ?', (folder_id,))
            return cursor.rowcount > 0
    
    # Script operations
    def create_script(self, script: Script) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO scripts (name, folder_id, content, description, author, 
                                   environment_tag, file_type, created_date, 
                                   modified_date, last_opened_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (script.name, script.folder_id, script.content, script.description,
                  script.author, script.environment_tag, script.file_type,
                  script.created_date, script.modified_date, script.last_opened_date))
            return cursor.lastrowid
    
    def get_script(self, script_id: int) -> Optional[Script]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM scripts WHERE id = ?', (script_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_script(row)
            return None
    
    def get_scripts_by_folder(self, folder_id: Optional[int]) -> List[Script]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if folder_id is None:
                cursor.execute('SELECT * FROM scripts WHERE folder_id IS NULL ORDER BY name')
            else:
                cursor.execute('SELECT * FROM scripts WHERE folder_id = ? ORDER BY name', (folder_id,))
            return [self._row_to_script(row) for row in cursor.fetchall()]
    
    def update_script(self, script: Script) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            script.modified_date = datetime.now()
            cursor.execute('''
                UPDATE scripts 
                SET name = ?, folder_id = ?, content = ?, description = ?, 
                    author = ?, environment_tag = ?, file_type = ?, 
                    modified_date = ?, last_opened_date = ?
                WHERE id = ?
            ''', (script.name, script.folder_id, script.content, script.description,
                  script.author, script.environment_tag, script.file_type,
                  script.modified_date, script.last_opened_date, script.id))
            return cursor.rowcount > 0
    
    def update_script_last_opened(self, script_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE scripts 
                SET last_opened_date = ?
                WHERE id = ?
            ''', (datetime.now(), script_id))
            return cursor.rowcount > 0
    
    def delete_script(self, script_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM scripts WHERE id = ?', (script_id,))
            return cursor.rowcount > 0
    
    def search_scripts(self, query: str) -> List[Script]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            search_pattern = f'%{query}%'
            cursor.execute('''
                SELECT * FROM scripts 
                WHERE name LIKE ? OR content LIKE ? OR description LIKE ?
                ORDER BY name
            ''', (search_pattern, search_pattern, search_pattern))
            return [self._row_to_script(row) for row in cursor.fetchall()]
    
    # Helper methods
    def _row_to_folder(self, row) -> Folder:
        return Folder(
            id=row['id'],
            name=row['name'],
            parent_id=row['parent_id'],
            created_date=datetime.fromisoformat(row['created_date']),
            path=row['path']
        )
    
    def _row_to_script(self, row) -> Script:
        return Script(
            id=row['id'],
            name=row['name'],
            folder_id=row['folder_id'],
            content=row['content'],
            description=row['description'],
            author=row['author'],
            environment_tag=row['environment_tag'],
            file_type=row['file_type'],
            created_date=datetime.fromisoformat(row['created_date']),
            modified_date=datetime.fromisoformat(row['modified_date']),
            last_opened_date=datetime.fromisoformat(row['last_opened_date'])
        )