# PowerShell Script Library - Bundle Creation Guide

## What is a Bundle?

A bundle is a standalone, portable version of the PowerShell Script Library that includes:
- The Python interpreter
- All required libraries (PyQt6, Pygments, etc.)
- Your application code
- All resources and assets

**Key Benefits:**
- No Python installation required
- No dependency installation needed
- Single folder that can be copied anywhere
- Works on machines without development tools

## Creating a Bundle

### Prerequisites (Development Machine Only)

You need Python and the app dependencies installed on YOUR machine to create the bundle.
The target machines won't need anything installed.

### Windows Bundle Creation

1. **Navigate to the PSLibrary directory**
   ```cmd
   cd C:\path\to\PSLibrary
   ```

2. **Run the bundle creation script**
   ```cmd
   deploy\create_bundle_windows.bat
   ```

3. **Wait for completion** (5-10 minutes)
   - PyInstaller will analyze your code
   - Download and include all dependencies
   - Create the executable

4. **Find your bundle**
   - Location: `PSLibrary_Portable\`
   - Size: ~100-150MB (includes everything)

### Linux/macOS Bundle Creation

1. **Navigate to the PSLibrary directory**
   ```bash
   cd /path/to/PSLibrary
   ```

2. **Run the bundle creation script**
   ```bash
   ./deploy/create_bundle_unix.sh
   ```

3. **Find your bundle**
   - Location: `PSLibrary_Portable/`

## Distributing the Bundle

### Method 1: ZIP Archive

**Windows:**
1. Right-click the `PSLibrary_Portable` folder
2. Select "Send to" → "Compressed (zipped) folder"
3. Share the resulting ZIP file

**Linux/macOS:**
```bash
tar -czf PSLibrary_Portable.tar.gz PSLibrary_Portable/
```

### Method 2: File Sharing
- Upload to cloud storage (Google Drive, Dropbox, etc.)
- Share via USB drive
- Host on your website

## Running the Portable Bundle

### For End Users

**Windows:**
1. Extract the ZIP file
2. Open the `PSLibrary_Portable` folder
3. Double-click `run.bat` or `PowerShellScriptLibrary.exe`

**Linux/macOS:**
1. Extract the archive
2. Open terminal in the folder
3. Run: `./run.sh` or `./PowerShellScriptLibrary`

### First Run Notes

- **Windows Defender** may show a warning (common for PyInstaller apps)
  - Click "More info" → "Run anyway"
- **macOS Gatekeeper** may block the app
  - Go to System Preferences → Security & Privacy
  - Click "Open Anyway"
- **Linux** may need execute permissions
  - Run: `chmod +x PowerShellScriptLibrary`

## Bundle Contents

```
PSLibrary_Portable/
├── PowerShellScriptLibrary.exe (or no .exe on Unix)
├── run.bat (Windows) or run.sh (Unix)
├── README.txt
├── resources/
├── PyQt6/
├── _internal/
└── [other bundled files]
```

## Advantages vs Disadvantages

### ✅ Advantages
- **No installation required** - just extract and run
- **Self-contained** - includes everything needed
- **Portable** - can run from USB drive
- **Version locked** - no dependency conflicts
- **Easy distribution** - single archive file

### ⚠️ Disadvantages
- **Larger size** - ~100-150MB vs ~10MB source
- **Slower startup** - unpacking takes a moment
- **Antivirus warnings** - common with PyInstaller
- **Platform specific** - need separate bundles per OS
- **Updates** - need to rebuild for code changes

## Troubleshooting

### Bundle Creation Fails

1. **Install PyInstaller manually:**
   ```bash
   pip install pyinstaller
   ```

2. **Check for errors in the spec file**

3. **Try building with console mode** (for debugging):
   - Edit the .spec file
   - Change `console=False` to `console=True`

### Runtime Errors

1. **Missing modules:**
   - Add to `hiddenimports` in the spec file
   
2. **Resource files not found:**
   - Add to `datas` in the spec file
   
3. **DLL errors:**
   - May need to include specific DLLs in `binaries`

## Alternative: One-File Bundle

To create a single executable file (slower but more portable):

1. Edit the bundle script
2. Add `--onefile` flag to PyInstaller command
3. Results in a single .exe file (~80MB)

Note: One-file mode is slower to start as it extracts to temp folder each run.

## Summary

- **For developers/technical users**: Use the installers
- **For end users**: Use the portable bundle
- **For mass distribution**: Create and share the bundle
- **For USB/portable use**: Use the bundle

The bundle creation scripts handle all the complexity of packaging your Python application into something that "just works" on any compatible computer!