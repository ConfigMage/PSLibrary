from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Folder:
    id: Optional[int] = None
    name: str = ""
    parent_id: Optional[int] = None
    created_date: datetime = None
    path: str = ""
    
    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now()


@dataclass
class Script:
    id: Optional[int] = None
    name: str = ""
    folder_id: Optional[int] = None
    content: str = ""
    description: str = ""
    author: str = ""
    environment_tag: str = "Testing"  # Testing or Production
    file_type: str = "ps1"  # ps1 or bat
    created_date: datetime = None
    modified_date: datetime = None
    last_opened_date: datetime = None
    
    def __post_init__(self):
        now = datetime.now()
        if self.created_date is None:
            self.created_date = now
        if self.modified_date is None:
            self.modified_date = now
        if self.last_opened_date is None:
            self.last_opened_date = now