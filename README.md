# PowerShell & Batch Script Library Manager

A modern, VS Code-inspired GUI application for managing PowerShell (.ps1) and batch (.bat) scripts with advanced features.

## Features

- **Hierarchical Folder Structure**: Organize scripts in folders with drag-and-drop support
- **Advanced Code Editor**: Syntax highlighting for PowerShell and batch scripts with QScintilla
- **Tabbed Interface**: Open multiple scripts simultaneously
- **Properties Panel**: Edit script metadata (author, environment, description)
- **Search Functionality**: Search across script names, content, and descriptions
- **Theme Support**: Dark and light themes
- **Database Storage**: SQLite backend for persistent storage

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python main.py
```

## Usage

### Creating Scripts and Folders
- Right-click in the folder tree to create new scripts or folders
- Use the toolbar buttons or File menu for quick access

### Editing Scripts
- Double-click a script to open it in the editor
- Multiple scripts can be open in tabs
- Unsaved changes are indicated with a dot (●) in the tab title

### Managing Properties
- Select a script or folder to view its properties in the right panel
- Edit metadata like author, environment (Testing/Production), and description
- Click "Save Properties" to update

### Searching
- Use Ctrl+F or the Search button to find scripts
- Search by name, content, or description

### Themes
- Switch between dark and light themes via View > Theme menu

## Project Structure

```
PSLibrary/
├── main.py              # Application entry point
├── database/            # Database models and management
│   ├── models.py       # Data models (Script, Folder)
│   └── database.py     # Database operations
├── core/               # Core functionality
│   ├── script_manager.py    # Business logic
│   └── syntax_highlighter.py # Syntax highlighting
├── gui/                # User interface components
│   ├── main_window.py      # Main application window
│   ├── folder_tree.py      # Folder tree widget
│   ├── editor_tabs.py      # Tabbed editor
│   ├── properties_panel.py # Properties sidebar
│   ├── search_dialog.py    # Search functionality
│   └── theme_manager.py    # Theme management
└── requirements.txt    # Python dependencies
```

## Database Schema

The application uses SQLite with two main tables:

- **folders**: Hierarchical folder structure
- **scripts**: Script files with metadata

## License

This project is provided as-is for educational and personal use.