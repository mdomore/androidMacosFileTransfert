# Android-macOS File Transfer (Web Version)

A modern, web-based file transfer solution that allows you to upload files from your Android phone to your Mac over WiFi. Features a clean, compact interface with advanced file management capabilities and robust screen lock handling.

## Features

- **No USB Required**: Works over WiFi connection
- **No App Installation**: Uses your phone's web browser
- **Modern UI**: Clean, compact interface inspired by modern design systems
- **Mobile-Optimized**: Responsive design for all screen sizes
- **File Upload/Download**: Bidirectional file transfer
- **Advanced File Management**: Browse, delete, organize, and create folders
- **Multi-Select Operations**: Select multiple files for bulk download/delete
- **Progress Indicators**: Real-time upload progress with detailed status
- **Directory Navigation**: Click directory names to navigate, ".." to go up
- **Popup Menus**: Clean "..." menus for file actions
- **Custom Target Directory**: Choose where to save uploaded files
- **Folder Creation**: Create new folders directly from the interface
- **Screen Lock Handling**: Pauses and resumes uploads when screen locks
- **Resumable Uploads**: Continues interrupted transfers automatically
- **Upload State Persistence**: Remembers progress across page refreshes
- **Manual Controls**: Resume, cancel, and monitor upload progress

## Prerequisites

- **Python** (v3.8 or higher) - Usually pre-installed on macOS
- **WiFi Network**: Both devices must be on the same WiFi network

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd androidMacosFileTransfert
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Start the Web Server

```bash
./start_web.sh
```

The server will start and display:
- The URL to open on your phone
- The local URL for your Mac
- The folder where files will be saved

### Connect Your Phone

1. **Ensure both devices are on the same WiFi network**
2. **Open your phone's web browser** (Chrome, Safari, etc.)
3. **Enter the displayed URL** (e.g., `http://192.168.1.50:5001`)
4. **Start uploading files** from your phone to your Mac

## How It Works

The web server creates a modern web interface that:
1. **Runs on your Mac** and serves a responsive web page
2. **Accepts file uploads** from your phone's browser
3. **Saves files** to your chosen directory (default: `~/Downloads/`)
4. **Provides full file management** through the web interface
5. **Handles screen locks** gracefully with pause/resume functionality

## File Management Features

### Upload Files
- **Choose target directory** where files will be saved
- **Upload multiple files** at once with batch processing
- **Real-time progress** indicators with file-by-file status
- **Automatic directory creation** if needed
- **Screen lock handling** - uploads pause when screen locks and resume when unlocked
- **Resumable uploads** - interrupted transfers continue from where they left off
- **Upload state persistence** - progress saved across page refreshes

### Browse & Navigate
- **Click directory names** to enter folders
- **".." link** at the top to go up one level
- **File icons** show file types with appropriate emojis
- **File details** show size, date, and permissions
- **Custom directory support** - navigate to any accessible folder

### File Operations
- **Multi-select** files with checkboxes
- **Bulk download** selected files to phone
- **Bulk delete** selected files
- **Individual actions** via "..." popup menus
- **Create folders** in current directory
- **File type detection** with appropriate icons

### Target Directory
- **Default location**: `~/Downloads/`
- **Custom selection**: Choose any directory with path validation
- **Auto-sync**: Upload directory follows current browsing location
- **Reset option**: Return to default directory
- **Tilde expansion**: Supports `~/` paths for home directory

## Screen Lock Handling

### Automatic Pause/Resume
- **Detects screen lock** when page becomes hidden
- **Pauses uploads** automatically to prevent interruption
- **Shows status message** "⏸️ Upload paused (screen locked)"
- **Resumes automatically** when you unlock the phone
- **Manual resume** button available if needed

### Upload State Management
- **Persistent storage** - upload progress saved in browser
- **Resume on refresh** - continues from where it left off
- **Progress tracking** - remembers which files were uploaded
- **Manual controls** - cancel or resume uploads as needed

### Best Practices
- **Set screen timeout** to maximum (30 minutes) before starting
- **Keep phone plugged in** during long transfers
- **Upload in batches** - select multiple files at once
- **Monitor progress** - watch for completion messages

## Project Structure

```
androidMacosFileTransfert/
├── backend/
│   └── web_server.py          # Main web server with all features
├── venv/                      # Python virtual environment
├── requirements.txt           # Python dependencies
├── start_web.sh              # Startup script
├── debug_app.sh              # Debug script
├── .gitignore                # Git ignore file
└── README.md                 # This file
```

## API Endpoints

- `GET /` - Main web interface
- `GET /api/files` - List files in directory (supports `~` expansion and custom base paths)
- `POST /api/upload` - Upload file from phone (handles custom directories)
- `GET /api/download` - Download file to phone (supports `~` expansion)
- `POST /api/delete` - Delete file (supports `~` expansion)
- `GET /api/validate-directory` - Validate directory path and permissions
- `POST /api/create-folder` - Create new folder in specified directory
- `GET /api/info` - Server information (IP, port, URL)

## Troubleshooting

### Can't Access the URL
- **Check WiFi**: Ensure both devices are on the same network
- **Try Different IP**: The server shows multiple IP addresses, try each one
- **Check Firewall**: Ensure port 5001 is not blocked
- **Restart Server**: Stop and restart the web server

### Upload Issues
- **File Size**: Large files may take time to upload
- **Network Speed**: WiFi speed affects upload performance
- **Browser Issues**: Try a different browser on your phone
- **Screen Lock**: Uploads pause when screen locks - unlock to resume
- **Interrupted Transfer**: Refresh page to resume from where it left off

### File Not Appearing
- **Refresh Page**: Click the refresh button in the web interface
- **Check Target Directory**: Files are saved to your chosen directory (default: `~/Downloads/`)
- **Permissions**: Ensure the folder has write permissions
- **Path Issues**: Use "Choose Directory" to select a valid path
- **Directory Navigation**: Make sure you're in the right folder

### Navigation Issues
- **".." Link**: Use the ".." link at the top to go up directories
- **Click Directory Names**: Click on folder names to enter them
- **Popup Menus**: Use the "..." button for file actions
- **Multi-Select**: Use checkboxes to select multiple files
- **Custom Directories**: Use "Choose Directory" for custom paths

### Screen Lock Problems
- **Upload Paused**: Normal behavior - unlock phone to resume
- **Lost Progress**: Refresh page to restore upload state
- **Manual Resume**: Use the "Resume" button if needed
- **Cancel Upload**: Use "Cancel" button to stop completely

## Advantages

- **Simple Setup**: No complex configuration required
- **Cross-Platform**: Works with any device that has a web browser
- **No Dependencies**: No need for special apps or drivers
- **Secure**: Files stay on your local network
- **Fast**: Direct WiFi transfer without internet
- **Modern Interface**: Clean, intuitive design
- **Advanced Features**: Multi-select, folder creation, custom directories
- **Screen Lock Resilient**: Handles phone screen locks gracefully
- **Resumable**: Continues interrupted transfers automatically
- **Public-Ready**: No personal information in the code
- **Universal Paths**: Uses `~/Downloads` for cross-platform compatibility
- **Robust Error Handling**: Graceful handling of network and file system errors

## Recent Updates

- **Screen Lock Handling**: Uploads pause when screen locks and resume when unlocked
- **Resumable Uploads**: Interrupted transfers continue from where they left off
- **Upload State Persistence**: Progress saved across page refreshes
- **Enhanced Progress Tracking**: File-by-file upload status with detailed feedback
- **Manual Controls**: Resume, cancel, and monitor upload progress
- **Custom Directory Support**: Full support for custom upload directories
- **Path Validation**: Ensures directory paths are valid and writable
- **Improved Error Handling**: Better error messages and recovery options

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details