#!/bin/bash

# Web-based Android File Transfer Startup Script

echo "🌐 Starting Web-based Android File Transfer..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if Python dependencies are installed
if ! python -c "import flask" &> /dev/null; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Start the web server
echo "🌐 Starting web server..."
python backend/web_server.py

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping web server..."
    deactivate 2>/dev/null
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup SIGINT

# Wait for the process
wait
