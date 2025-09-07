#!/bin/bash

# Debug version of the Android File Transfer app
# This version shows all output and errors

# Get the directory where the app bundle is located
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROJECT_DIR="$APP_DIR/Contents/Resources"

echo "App directory: $APP_DIR"
echo "Project directory: $PROJECT_DIR"

# Change to the project directory
cd "$PROJECT_DIR"
echo "Current directory: $(pwd)"

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
    
    echo "Showing dialog for URL: $url"
    
    # Show dialog in background
    osascript -e "display dialog \"🚀 Android File Transfer Server Started!

📱 Access URL: $url

📋 Instructions:
1. Copy the URL above
2. Open your phone's web browser  
3. Paste the URL and press Enter
4. Start transferring files!

The server is now running in the background.
Click 'Open Browser' to open the URL now.\" buttons {\"OK\", \"Open Browser\"} default button \"Open Browser\" with title \"Android File Transfer\"" &
    
    # Open browser after a short delay
    sleep 1
    open "$url"
}

# Function to start the web server
start_server() {
    echo "Checking for Python 3..."
    if ! command -v python3 &> /dev/null; then
        echo "Python 3 not found!"
        osascript -e 'display dialog "Python 3 is required but not installed. Please install Python 3 and try again." buttons {"OK"} default button "OK"'
        exit 1
    fi
    
    echo "Python 3 found: $(which python3)"
    
    echo "Checking for virtual environment..."
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo "Failed to create virtual environment!"
            osascript -e 'display dialog "Failed to create virtual environment. Please check Python installation." buttons {"OK"} default button "OK"'
            exit 1
        fi
    fi
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "Installing dependencies..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "Failed to install dependencies!"
            osascript -e 'display dialog "Failed to install dependencies. Please check your internet connection." buttons {"OK"} default button "OK"'
            exit 1
        fi
    fi
    
    local_ip=$(get_local_ip)
    echo "Detected IP address: $local_ip"
    
    # Show dialog and start server
    show_url_dialog "$local_ip" &
    
    echo "Starting Android File Transfer server..."
    echo "Access URL: http://$local_ip:5001"
    echo "Press Ctrl+C to stop the server"
    echo "Working directory: $(pwd)"
    echo "Python path: $(which python3)"
    
    # Start the server with error handling
    echo "Starting Python server..."
    python3 backend/web_server.py 2>&1 | while read line; do
        echo "Server: $line"
    done
}

cleanup() {
    echo "Stopping Android File Transfer server..."
    exit 0
}

trap cleanup SIGINT SIGTERM
start_server
