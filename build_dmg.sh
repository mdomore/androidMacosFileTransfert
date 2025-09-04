#!/bin/bash

# Build script for Android File Transfer DMG
# This script creates a DMG installer for the macOS app

set -e

APP_NAME="Android File Transfer"
APP_BUNDLE="AndroidFileTransfer.app"
DMG_NAME="AndroidFileTransfer-1.0.0.dmg"
VOLUME_NAME="Android File Transfer"

echo "Building Android File Transfer DMG..."

# Clean up previous builds
if [ -d "$APP_BUNDLE" ]; then
    echo "Cleaning up previous app bundle..."
    rm -rf "$APP_BUNDLE"
fi

if [ -f "$DMG_NAME" ]; then
    echo "Removing previous DMG..."
    rm -f "$DMG_NAME"
fi

# Create the app bundle structure
echo "Creating app bundle structure..."
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Copy Info.plist
if [ -f "AndroidFileTransfer.app/Contents/Info.plist" ]; then
    cp AndroidFileTransfer.app/Contents/Info.plist "$APP_BUNDLE/Contents/"
else
    echo "Creating Info.plist..."
    cat > "$APP_BUNDLE/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>AndroidFileTransfer</string>
    <key>CFBundleIdentifier</key>
    <string>com.androidfiletransfer.app</string>
    <key>CFBundleName</key>
    <string>Android File Transfer</string>
    <key>CFBundleDisplayName</key>
    <string>Android File Transfer</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.14</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
EOF
fi

# Copy the executable
if [ -f "AndroidFileTransfer.app/Contents/MacOS/AndroidFileTransfer" ]; then
    cp AndroidFileTransfer.app/Contents/MacOS/AndroidFileTransfer "$APP_BUNDLE/Contents/MacOS/"
else
    echo "Creating executable script..."
    cat > "$APP_BUNDLE/Contents/MacOS/AndroidFileTransfer" << 'EOF'
#!/bin/bash
# Get the directory where the app bundle is located
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROJECT_DIR="$APP_DIR/Contents/Resources"

# Change to the project directory
cd "$PROJECT_DIR"

# Function to get local IP addresses
get_local_ip() {
    local ip=$(ifconfig | grep -E "inet [0-9]" | grep -v "127.0.0.1" | head -1 | awk '{print $2}')
    echo "$ip"
}

# Function to show URL in a dialog
show_url_dialog() {
    local ip="$1"
    local port="5001"
    local url="http://$ip:$port"
    
    osascript -e "display dialog \"🚀 Android File Transfer Server Started!

📱 Access URL: $url

📋 Instructions:
1. Copy the URL above
2. Open your phone's web browser  
3. Paste the URL and press Enter
4. Start transferring files!

The server will continue running in the background.
Click 'Open Browser' to open the URL now.\" buttons {\"OK\", \"Open Browser\"} default button \"Open Browser\" with title \"Android File Transfer\""
    
    if [ $? -eq 0 ]; then
        open "$url"
    fi
}

# Function to start the web server
start_server() {
    if ! command -v python3 &> /dev/null; then
        osascript -e 'display dialog "Python 3 is required but not installed. Please install Python 3 and try again." buttons {"OK"} default button "OK"'
        exit 1
    fi
    
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies..."
        pip install -r requirements.txt --quiet
    fi
    
    local_ip=$(get_local_ip)
    show_url_dialog "$local_ip"
    
    echo "Starting Android File Transfer server..."
    echo "Access URL: http://$local_ip:5001"
    echo "Press Ctrl+C to stop the server"
    
    python3 backend/web_server.py
}

cleanup() {
    echo "Stopping Android File Transfer server..."
    exit 0
}

trap cleanup SIGINT SIGTERM
start_server
EOF
fi

chmod +x "$APP_BUNDLE/Contents/MacOS/AndroidFileTransfer"

# Copy project files
cp -r backend "$APP_BUNDLE/Contents/Resources/"
cp requirements.txt "$APP_BUNDLE/Contents/Resources/"

# Create a simple icon (using system icon as fallback)
echo "Creating app icon..."
# Use a system icon as fallback
cp /System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/GenericApplicationIcon.icns "$APP_BUNDLE/Contents/Resources/icon.icns" 2>/dev/null || true

# Create a temporary DMG
echo "Creating DMG..."
TEMP_DMG="temp.dmg"
DMG_SIZE=50  # MB

# Create a temporary directory for DMG contents
DMG_TEMP_DIR="dmg_temp"
rm -rf "$DMG_TEMP_DIR"
mkdir -p "$DMG_TEMP_DIR"

# Copy app to temp directory
cp -r "$APP_BUNDLE" "$DMG_TEMP_DIR/"

# Create a README for the DMG
cat > "$DMG_TEMP_DIR/README.txt" << 'EOF'
Android File Transfer for macOS
==============================

Installation:
1. Drag "Android File Transfer.app" to your Applications folder
2. Double-click the app to start the file transfer server
3. Follow the on-screen instructions to connect your phone

Usage:
- The app will show you a URL to access from your phone
- Open this URL in your phone's web browser
- Start transferring files between your phone and Mac

Requirements:
- macOS 10.14 or later
- Python 3 (usually pre-installed)
- WiFi connection

For support and updates, visit the project repository.
EOF

# Create the DMG
hdiutil create -srcfolder "$DMG_TEMP_DIR" -volname "$VOLUME_NAME" -fs HFS+ -fsargs "-c c=64,a=16,e=16" -format UDRW -size ${DMG_SIZE}m "$TEMP_DMG"

# Mount the DMG
echo "Mounting DMG for customization..."
MOUNT_OUTPUT=$(hdiutil attach -readwrite -noverify -noautoopen "$TEMP_DMG")
MOUNT_POINT=$(echo "$MOUNT_OUTPUT" | grep -E '^/dev/' | head -1 | awk '{print $3}')

if [ -z "$MOUNT_POINT" ]; then
    echo "Failed to mount DMG, creating without customization..."
else
    # Wait for mount
    sleep 2
    
    # Set DMG properties
    echo "Customizing DMG..."
    # Set background (optional)
    # Set icon positions
    # Set window properties
    
    # Unmount the DMG
    hdiutil detach "$MOUNT_POINT" 2>/dev/null || true
fi

# Convert to final DMG
echo "Creating final DMG..."
hdiutil convert "$TEMP_DMG" -format UDZO -imagekey zlib-level=9 -o "$DMG_NAME"

# Clean up
rm -f "$TEMP_DMG"
rm -rf "$DMG_TEMP_DIR"

echo "✅ DMG created successfully: $DMG_NAME"
echo "📦 App bundle: $APP_BUNDLE"
echo ""
echo "To install:"
echo "1. Double-click $DMG_NAME"
echo "2. Drag the app to Applications folder"
echo "3. Launch the app and follow the instructions"
