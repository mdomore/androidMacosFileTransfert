# Building Android File Transfer for macOS

This document explains how to build the Android File Transfer app as a native macOS application and create a DMG installer.

## Prerequisites

- macOS 10.14 or later
- Python 3 (usually pre-installed)
- Xcode Command Line Tools (for `hdiutil`)

## Quick Build

To build the app and create a DMG installer:

```bash
./simple_build.sh
```

This will create:
- `AndroidFileTransfer.app` - The macOS application bundle
- `AndroidFileTransfer-1.0.0.dmg` - The DMG installer

## What the Build Process Does

### 1. Creates App Bundle Structure
```
AndroidFileTransfer.app/
├── Contents/
│   ├── Info.plist          # App metadata
│   ├── MacOS/
│   │   └── AndroidFileTransfer  # Main executable
│   └── Resources/
│       ├── backend/        # Python web server
│       └── requirements.txt # Python dependencies
```

### 2. App Features
- **Native macOS app** - Double-click to launch
- **URL Display** - Shows access URL in a dialog when launched
- **Auto-setup** - Creates virtual environment and installs dependencies
- **Browser Integration** - Option to open URL in default browser
- **Error Handling** - Checks for Python installation

### 3. DMG Installer
- **Drag-and-drop installation** - Drag app to Applications folder
- **Compressed format** - Optimized file size
- **Universal compatibility** - Works on all supported macOS versions

## Manual Build Steps

If you prefer to build manually:

### 1. Create App Bundle
```bash
mkdir -p AndroidFileTransfer.app/Contents/{MacOS,Resources}
```

### 2. Create Info.plist
```bash
# Copy the Info.plist from the build script
```

### 3. Create Executable
```bash
# Copy the executable script and make it executable
chmod +x AndroidFileTransfer.app/Contents/MacOS/AndroidFileTransfer
```

### 4. Copy Resources
```bash
cp -r backend AndroidFileTransfer.app/Contents/Resources/
cp requirements.txt AndroidFileTransfer.app/Contents/Resources/
```

### 5. Create DMG
```bash
hdiutil create -srcfolder AndroidFileTransfer.app -volname "Android File Transfer" -format UDZO -imagekey zlib-level=9 -o AndroidFileTransfer-1.0.0.dmg
```

## App Behavior

When the app is launched:

1. **Checks for Python 3** - Shows error if not found
2. **Creates virtual environment** - Sets up isolated Python environment
3. **Installs dependencies** - Installs Flask and other requirements
4. **Gets local IP address** - Automatically detects network IP
5. **Shows URL dialog** - Displays access URL with instructions
6. **Starts web server** - Runs the file transfer server
7. **Opens browser** - Optionally opens URL in default browser

## Distribution

The DMG file can be distributed to users who can:
1. Download the DMG
2. Double-click to mount it
3. Drag the app to Applications folder
4. Launch the app and follow instructions

## Troubleshooting

### Build Issues
- **Permission denied**: Run `chmod +x simple_build.sh`
- **Python not found**: Install Python 3 from python.org
- **hdiutil not found**: Install Xcode Command Line Tools

### App Issues
- **App won't launch**: Check that the executable has proper permissions
- **Python errors**: Ensure Python 3 is installed and accessible
- **Network issues**: Check firewall settings and WiFi connection

## Customization

### Changing App Name
Edit the `APP_NAME` variable in `simple_build.sh`

### Changing Version
Edit the version strings in both the build script and Info.plist

### Adding Icon
Replace the default icon by adding an `icon.icns` file to the Resources folder

### Modifying Behavior
Edit the executable script in `AndroidFileTransfer.app/Contents/MacOS/AndroidFileTransfer`
