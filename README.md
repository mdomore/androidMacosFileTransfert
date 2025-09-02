# Android-macOS File Transfer (Web Version)

A modern, web-based file transfer solution that allows you to upload files from your Android phone to your Mac over WiFi. Features a clean, compact interface with advanced file management capabilities.

## Features

- **No USB Required**: Works over WiFi connection
- **No App Installation**: Uses your phone's web browser
- **Modern UI**: Clean, compact interface inspired by modern design systems
- **Mobile-Optimized**: Responsive design for all screen sizes
- **File Upload/Download**: Bidirectional file transfer
- **Advanced File Management**: Browse, delete, organize, and create folders
- **Multi-Select Operations**: Select multiple files for bulk download/delete
- **Progress Indicators**: Real-time upload progress
- **Directory Navigation**: Click directory names to navigate, ".." to go up
- **Popup Menus**: Clean "..." menus for file actions
- **Custom Target Directory**: Choose where to save uploaded files
- **Folder Creation**: Create new folders directly from the interface

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

## File Management Features

### Upload Files
- **Choose target directory** where files will be saved
- **Upload multiple files** at once
- **Real-time progress** indicators
- **Automatic directory creation** if needed

### Browse & Navigate
- **Click directory names** to enter folders
- **".." link** at the top to go up one level
- **File icons** show file types
- **File details** show size and date

### File Operations
- **Multi-select** files with checkboxes
- **Bulk download** selected files
- **Bulk delete** selected files
- **Individual actions** via "..." popup menus
- **Create folders** in current directory

### Target Directory
- **Default location**: `~/Downloads/`
- **Custom selection**: Choose any directory
- **Auto-sync**: Upload directory follows current browsing location
- **Reset option**: Return to default directory

## Project Structure

```
androidMacosFileTransfert/
├── backend/
│   └── web_server.py          # Main web server
├── venv/                      # Python virtual environment
├── requirements.txt           # Python dependencies
├── start_web.sh              # Startup script
├── .gitignore                # Git ignore file
└── README.md                 # This file
```

## API Endpoints

- `GET /` - Main web interface
- `GET /api/files` - List files in directory (supports `~` expansion)
- `POST /api/upload` - Upload file from phone
- `GET /api/download` - Download file to phone (supports `~` expansion)
- `POST /api/delete` - Delete file (supports `~` expansion)
- `GET /api/validate-directory` - Validate directory path
- `POST /api/create-folder` - Create new folder
- `GET /api/info` - Server information

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

### File Not Appearing
- **Refresh Page**: Click the refresh button in the web interface
- **Check Target Directory**: Files are saved to your chosen directory (default: `~/Downloads/`)
- **Permissions**: Ensure the folder has write permissions
- **Path Issues**: Use "Choose Directory" to select a valid path

### Navigation Issues
- **".." Link**: Use the ".." link at the top to go up directories
- **Click Directory Names**: Click on folder names to enter them
- **Popup Menus**: Use the "..." button for file actions
- **Multi-Select**: Use checkboxes to select multiple files

## Advantages

- **Simple Setup**: No complex configuration required
- **Cross-Platform**: Works with any device that has a web browser
- **No Dependencies**: No need for special apps or drivers
- **Secure**: Files stay on your local network
- **Fast**: Direct WiFi transfer without internet
- **Modern Interface**: Clean, intuitive design
- **Advanced Features**: Multi-select, folder creation, custom directories
- **Public-Ready**: No personal information in the code
- **Universal Paths**: Uses `~/Downloads` for cross-platform compatibility

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details
