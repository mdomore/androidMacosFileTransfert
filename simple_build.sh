#!/bin/bash

# Simple build script for Android File Transfer
# Creates a basic DMG without complex customization

set -e

APP_NAME="Android File Transfer"
APP_BUNDLE="AndroidFileTransfer.app"
DMG_NAME="AndroidFileTransfer-1.0.0.dmg"

echo "Building Android File Transfer..."

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

# Create Info.plist
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

# Create the executable
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

chmod +x "$APP_BUNDLE/Contents/MacOS/AndroidFileTransfer"

# Copy project files
echo "Copying project files..."
cp -r backend "$APP_BUNDLE/Contents/Resources/"
cp requirements.txt "$APP_BUNDLE/Contents/Resources/"

# Create a simple DMG
echo "Creating DMG..."
hdiutil create -srcfolder "$APP_BUNDLE" -volname "$APP_NAME" -format UDZO -imagekey zlib-level=9 -o "$DMG_NAME"

echo "✅ DMG created successfully: $DMG_NAME"
echo "📦 App bundle: $APP_BUNDLE"
echo ""
echo "To install:"
echo "1. Double-click $DMG_NAME"
echo "2. Drag the app to Applications folder"
echo "3. Launch the app and follow the instructions"
