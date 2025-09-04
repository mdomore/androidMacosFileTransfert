import os
import json
import time
import shutil
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import threading
import subprocess
import socket

app = Flask(__name__)
CORS(app)

class WebFileManager:
    def __init__(self):
        self.base_path = os.path.expanduser("~/Downloads")
        self.ensure_base_path()
        
    def ensure_base_path(self):
        """Ensure the base transfer directory exists"""
        Path(self.base_path).mkdir(parents=True, exist_ok=True)
    
    def get_local_ip(self):
        """Get the local IP address of the Mac"""
        try:
            # Get local IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"
    
    def list_files(self, path=""):
        """List files in the transfer directory"""
        try:
            full_path = Path(self.base_path) / path if path else Path(self.base_path)
            
            if not full_path.exists():
                return []
            
            files = []
            for item in full_path.iterdir():
                try:
                    stat = item.stat()
                    file_info = {
                        'name': item.name,
                        'path': str(item.relative_to(Path(self.base_path))),
                        'is_dir': item.is_dir(),
                        'size': stat.st_size if item.is_file() else None,
                        'date': time.strftime('%b %d %H:%M', time.localtime(stat.st_mtime)),
                        'permissions': oct(stat.st_mode)[-3:]
                    }
                    files.append(file_info)
                except (OSError, PermissionError):
                    continue
            
            # Sort: directories first, then files
            files.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
            return files
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def get_file_info(self, file_path):
        """Get detailed file information"""
        try:
            full_path = Path(self.base_path) / file_path
            
            if not full_path.exists():
                return None
            
            stat = full_path.stat()
            
            # Get file type using file command
            try:
                result = subprocess.run(['file', '-b', str(full_path)], 
                                      capture_output=True, text=True)
                file_type = result.stdout.strip()
            except:
                file_type = "Unknown"
            
            return {
                'path': file_path,
                'size': stat.st_size,
                'type': file_type,
                'modified': stat.st_mtime,
                'permissions': oct(stat.st_mode)[-3:]
            }
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None
    
    def create_directory(self, dir_name, parent_path=""):
        """Create a new directory"""
        try:
            full_path = Path(self.base_path) / parent_path / dir_name
            full_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False
    
    def delete_file(self, file_path):
        """Delete a file or directory"""
        try:
            full_path = Path(self.base_path) / file_path
            
            if not full_path.exists():
                return False
            
            if full_path.is_dir():
                shutil.rmtree(full_path)
            else:
                full_path.unlink()
            
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

file_manager = WebFileManager()

# HTML template for the mobile web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Android File Transfer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f7;
            color: #1d1d1f;
        }
        
        .header {
            background: #007aff;
            color: white;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 24px;
            font-weight: 600;
        }
        
        .header p {
            font-size: 14px;
            opacity: 0.9;
            margin-top: 5px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 16px;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 8px;
            }
        }
        
        .upload-section {
            background: white;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            border: 1px solid #e2e8f0;
        }
        
        @media (max-width: 768px) {
            .upload-section {
                padding: 12px;
                margin-bottom: 12px;
            }
        }
        
        .directory-selector {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 12px;
        }
        
        .directory-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .directory-title {
            font-weight: 600;
            color: #495057;
        }
        
        .directory-path {
            font-family: monospace;
            background: white;
            border: 1px solid #ced4da;
            border-radius: 4px;
            padding: 8px 12px;
            font-size: 14px;
            color: #6c757d;
            margin-bottom: 10px;
            word-break: break-all;
        }
        
        .directory-actions {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }
        
        @media (max-width: 768px) {
            .directory-actions {
                flex-direction: column;
                gap: 4px;
            }
        }
        
        .dir-btn {
            background: #64748b;
            color: white;
            border: none;
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 12px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        @media (max-width: 768px) {
            .dir-btn {
                padding: 8px 12px;
                font-size: 13px;
                width: 100%;
            }
        }
        
        .dir-btn:hover {
            background: #475569;
        }
        
        .dir-btn.primary {
            background: #3b82f6;
        }
        
        .dir-btn.primary:hover {
            background: #2563eb;
        }
        
        .upload-btn {
            background: #3b82f6;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            width: 100%;
            margin-bottom: 8px;
            transition: background-color 0.2s;
        }
        
        @media (max-width: 768px) {
            .upload-btn {
                padding: 14px 20px;
                font-size: 16px;
                margin-bottom: 12px;
            }
        }
        
        .upload-btn:hover {
            background: #2563eb;
        }
        
        .file-input {
            display: none;
        }
        
        .progress {
            width: 100%;
            height: 4px;
            background: #e5e5e7;
            border-radius: 2px;
            overflow: hidden;
            margin-top: 10px;
        }
        
        .progress-bar {
            height: 100%;
            background: #34c759;
            width: 0%;
            transition: width 0.3s ease;
        }
        
        .files-section {
            background: white;
            border-radius: 8px;
            padding: 16px;
            border: 1px solid #e2e8f0;
        }
        
        @media (max-width: 768px) {
            .files-section {
                padding: 12px;
            }
        }
        
        .files-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        
        .files-header-left {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        @media (max-width: 768px) {
            .files-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
            }
            
            .files-header-left {
                width: 100%;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 8px;
            }
            
            .files-title {
                font-size: 16px;
            }
        }
        
        .files-title {
            font-size: 16px;
            font-weight: 600;
        }
        
        .refresh-btn {
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 13px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .create-folder-btn {
            background: #10b981;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 13px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        

        
        @media (max-width: 768px) {
            .refresh-btn {
                padding: 10px 16px;
                font-size: 14px;
                width: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 6px;
            }
            
            .create-folder-btn {
                padding: 10px 16px;
                font-size: 14px;
                min-width: 120px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 6px;
            }
            

        }
        
        .file-list {
            list-style: none;
        }
        
        .file-item {
            display: flex;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #f1f5f9;
        }
        
        @media (max-width: 768px) {
            .file-item {
                padding: 12px 0;
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }
            
            .file-item-content {
                display: flex;
                align-items: center;
                width: 100%;
            }
        }
        
        .file-item:last-child {
            border-bottom: none;
        }
        
        .file-icon {
            width: 32px;
            height: 32px;
            background: #f8fafc;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
            font-size: 16px;
        }
        
        @media (max-width: 768px) {
            .file-icon {
                width: 40px;
                height: 40px;
                font-size: 20px;
                margin-right: 12px;
            }
        }
        
        .file-info {
            flex: 1;
        }
        
        @media (max-width: 768px) {
            .file-info {
                flex: 1;
                min-width: 0;
            }
        }
        
        .file-name {
            font-weight: 500;
            margin-bottom: 1px;
            font-size: 14px;
        }
        
        .file-name.clickable {
            cursor: pointer;
            color: #3b82f6;
            text-decoration: underline;
        }
        
        .file-name.clickable:hover {
            color: #2563eb;
        }
        
        .file-menu-btn {
            background: none;
            border: none;
            padding: 6px;
            cursor: pointer;
            border-radius: 4px;
            font-size: 18px;
            color: #64748b;
            transition: background-color 0.2s;
            min-width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .file-menu-btn:hover {
            background: #f1f5f9;
            color: #374151;
        }
        
        .file-menu-popup {
            position: absolute;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            padding: 4px 0;
            z-index: 1000;
            min-width: 120px;
            display: none;
        }
        
        .file-menu-popup.show {
            display: block;
        }
        
        .file-menu-item {
            display: flex;
            align-items: center;
            padding: 8px 12px;
            cursor: pointer;
            font-size: 13px;
            color: #374151;
            transition: background-color 0.2s;
        }
        
        .file-menu-item:hover {
            background: #f8fafc;
        }
        
        .file-menu-item.danger {
            color: #ef4444;
        }
        
        .file-menu-item.danger:hover {
            background: #fef2f2;
        }
        
        .file-menu-item .icon {
            margin-right: 8px;
            font-size: 14px;
        }
        
        .file-details {
            font-size: 11px;
            color: #64748b;
        }
        
        .file-actions {
            display: flex;
            gap: 6px;
        }
        
        @media (max-width: 768px) {
            .file-actions {
                flex-direction: column;
                gap: 4px;
                margin-top: 8px;
            }
            
            .file-actions button {
                padding: 8px 12px;
                font-size: 13px;
                min-width: 90px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 4px;
            }
        }
        
        .action-btn {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .action-btn.danger {
            background: #ef4444;
            color: white;
            border-color: #ef4444;
        }
        
        .action-btn:hover {
            background: #f1f5f9;
        }
        
        .action-btn.danger:hover {
            background: #dc2626;
        }
        
        .file-checkbox {
            margin-right: 8px;
            transform: scale(1.1);
        }
        
        @media (max-width: 768px) {
            .file-checkbox {
                transform: scale(1.3);
                margin-right: 12px;
            }
        }
        
        .file-item.selected {
            background: #eff6ff;
            border-radius: 6px;
        }
        
        .bulk-actions {
            display: none;
            background: #f8fafc;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 12px;
            border: 1px solid #e2e8f0;
        }
        
        .bulk-actions.show {
            display: block;
        }
        
        .bulk-actions-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .bulk-actions-left {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .bulk-actions-right {
            display: flex;
            gap: 8px;
        }
        
        .select-all-btn {
            background: #6c757d;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            cursor: pointer;
        }
        
        .bulk-delete-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            cursor: pointer;
        }
        
        .bulk-download-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            cursor: pointer;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: #8e8e93;
        }
        
        .empty-state p {
            margin-bottom: 10px;
        }
        
        .status {
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 8px;
            font-size: 14px;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📱 Android File Transfer</h1>
        <p>Upload files from your phone to your Mac</p>
    </div>
    
    <div class="container">
        <div id="status"></div>
        
        <div class="upload-section">
            <h3>Upload Files</h3>
            
            <div class="directory-selector">
                <div class="directory-header">
                    <div class="directory-title">📁 Target Directory</div>
                </div>
                <div class="directory-path" id="currentUploadPath">~/Downloads</div>
                <div class="directory-actions">
                    <button class="dir-btn primary" onclick="selectUploadDirectory()">📂 Choose Directory</button>
                    <button class="dir-btn" onclick="resetUploadDirectory()">🏠 Reset to Default</button>
    
                </div>
            </div>
            
            <input type="file" id="fileInput" class="file-input" multiple>
            <button class="upload-btn" onclick="document.getElementById('fileInput').click()">
                📁 Choose Files to Upload
            </button>
            <div class="progress" id="progress" style="display: none;">
                <div class="progress-bar" id="progressBar"></div>
            </div>
        </div>
        
        <div class="files-section">
            <div class="files-header">
                <div class="files-header-left">
                    <div class="files-title">Files on Mac</div>
                    <button class="create-folder-btn" onclick="createFolderInCurrentDirectory()">📁 Create Folder</button>
                </div>
                <button class="refresh-btn" onclick="loadFiles()">🔄 Refresh</button>
            </div>
            
            <div class="bulk-actions" id="bulkActions">
                <div class="bulk-actions-content">
                    <div class="bulk-actions-left">
                        <span id="selectedCount">0 files selected</span>
                        <button class="select-all-btn" onclick="toggleSelectAll()">Select All</button>
                    </div>
                    <div class="bulk-actions-right">
                        <button class="bulk-download-btn" onclick="downloadSelected()">⬇️ Download Selected</button>
                        <button class="bulk-delete-btn" onclick="deleteSelected()">🗑️ Delete Selected</button>
                    </div>
                </div>
            </div>
            
            <div id="fileList"></div>
        </div>
    </div>

    <script>
        let currentPath = '';
        let selectedFiles = new Set();
        let allFiles = [];
        let uploadDirectory = '~/Downloads';
        let baseUploadDirectory = '~/Downloads';
        
        // Load files on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadFiles();
            updateUploadPathDisplay();
        });
        
        // File upload handling
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const files = e.target.files;
            if (files.length > 0) {
                uploadFiles(files);
            }
        });
        
        async function uploadFiles(files) {
            const progress = document.getElementById('progress');
            const progressBar = document.getElementById('progressBar');
            
            progress.style.display = 'block';
            progressBar.style.width = '0%';
            
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const formData = new FormData();
                formData.append('file', file);
                formData.append('path', currentPath);
                formData.append('upload_directory', uploadDirectory);
                
                try {
                    const response = await fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        showStatus('File uploaded successfully: ' + file.name, 'success');
                    } else {
                        showStatus('Failed to upload: ' + file.name, 'error');
                    }
                } catch (error) {
                    showStatus('Error uploading: ' + file.name, 'error');
                }
                
                // Update progress
                const progressPercent = ((i + 1) / files.length) * 100;
                progressBar.style.width = progressPercent + '%';
            }
            
            // Hide progress after a delay
            setTimeout(() => {
                progress.style.display = 'none';
            }, 2000);
            
            // Refresh file list
            loadFiles();
        }
        
        async function loadFiles() {
            try {
                const response = await fetch('/api/files?path=' + encodeURIComponent(currentPath));
                const files = await response.json();
                allFiles = files;
                selectedFiles.clear();
                
                // Add ".." entry at the top if we're in a subdirectory
                if (currentPath && currentPath.trim() !== '') {
                    const parentPath = currentPath.split('/').slice(0, -1).join('/');
                    const parentEntry = {
                        name: '..',
                        path: parentPath,
                        is_dir: true,
                        size: null,
                        date: 'Parent directory'
                    };
                    allFiles.unshift(parentEntry);
                }
                
                displayFiles(allFiles);
                updateBulkActions();
            } catch (error) {
                showStatus('Error loading files', 'error');
            }
        }
        
        function displayFiles(files) {
            const fileList = document.getElementById('fileList');
            
            if (files.length === 0) {
                fileList.innerHTML = `
                    <div class="empty-state">
                        <p>📁 No files found</p>
                        <p>Upload some files from your phone to get started</p>
                    </div>
                `;
                return;
            }
            
            let html = '<ul class="file-list">';
            
            files.forEach(file => {
                const isParentDir = file.name === '..';
                const icon = isParentDir ? '⬆️' : (file.is_dir ? '📁' : getFileIcon(file.name));
                const size = file.size ? formatFileSize(file.size) : '';
                const isSelected = selectedFiles.has(file.path);
                const selectedClass = isSelected ? 'selected' : '';
                
                const safeId = file.path.replace(/[^a-zA-Z0-9]/g, '_');
                
                html += `
                    <li class="file-item ${selectedClass}">
                        <div class="file-item-content">
                            ${!isParentDir ? `<input type="checkbox" class="file-checkbox" ${isSelected ? 'checked' : ''} 
                                   onchange="toggleFileSelection('${file.path}')">` : ''}
                            <div class="file-icon">${icon}</div>
                            <div class="file-info">
                                <div class="file-name ${file.is_dir ? 'clickable' : ''}" 
                                     ${file.is_dir ? `onclick="navigateTo('${file.path}')"` : ''}>${file.name}</div>
                                <div class="file-details">${size} • ${file.date}</div>
                            </div>
                            ${!isParentDir ? `<div style="position: relative;">
                                <button class="file-menu-btn" onclick="showFileMenu('${file.path}', ${file.is_dir}, event)">⋯</button>
                                <div class="file-menu-popup" id="menu-${safeId}">
                                    ${file.is_dir ? 
                                        `<div class="file-menu-item" onclick="navigateTo('${file.path}')">
                                            <span class="icon">📂</span>Open
                                        </div>` :
                                        `<div class="file-menu-item" onclick="downloadFile('${file.path}')">
                                            <span class="icon">⬇️</span>Download
                                        </div>`
                                    }
                                    <div class="file-menu-item danger" onclick="deleteFile('${file.path}')">
                                        <span class="icon">🗑️</span>Delete
                                    </div>
                                </div>
                            </div>` : ''}
                        </div>
                    </li>
                `;
            });
            
            html += '</ul>';
            fileList.innerHTML = html;
        }
        
        function getFileIcon(fileName) {
            const ext = fileName.split('.').pop()?.toLowerCase();
            const icons = {
                'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'gif': '🖼️',
                'mp4': '🎥', 'avi': '🎥', 'mov': '🎥',
                'mp3': '🎵', 'wav': '🎵', 'flac': '🎵',
                'pdf': '📄', 'doc': '📄', 'docx': '📄',
                'zip': '📦', 'rar': '📦', '7z': '📦'
            };
            return icons[ext] || '📄';
        }
        
        function formatFileSize(bytes) {
            if (!bytes) return '';
            const sizes = ['B', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(1024));
            return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
        }
        
        async function navigateTo(path) {
            currentPath = path;
            loadFiles();
            
            // Update upload directory to match the current directory
            uploadDirectory = baseUploadDirectory + (path ? '/' + path : '');
            updateUploadPathDisplay();
            
            showStatus(`Upload directory updated to: ${path || 'Downloads folder'}`, 'success');
        }
        
        async function downloadFile(path) {
            try {
                const response = await fetch('/api/download?path=' + encodeURIComponent(path));
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = path.split('/').pop();
                    a.click();
                    window.URL.revokeObjectURL(url);
                }
            } catch (error) {
                showStatus('Error downloading file', 'error');
            }
        }
        
        async function deleteFile(path) {
            if (!confirm('Are you sure you want to delete this file?')) return;
            
            try {
                const response = await fetch('/api/delete', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ path: path })
                });
                
                if (response.ok) {
                    showStatus('File deleted successfully', 'success');
                    loadFiles();
                } else {
                    showStatus('Failed to delete file', 'error');
                }
            } catch (error) {
                showStatus('Error deleting file', 'error');
            }
        }
        
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.innerHTML = `<div class="status ${type}">${message}</div>`;
            setTimeout(() => {
                status.innerHTML = '';
            }, 3000);
        }
        
        function toggleFileSelection(filePath) {
            if (selectedFiles.has(filePath)) {
                selectedFiles.delete(filePath);
            } else {
                selectedFiles.add(filePath);
            }
            updateBulkActions();
            displayFiles(allFiles); // Refresh display to show selection state
        }
        
        function updateBulkActions() {
            const bulkActions = document.getElementById('bulkActions');
            const selectedCount = document.getElementById('selectedCount');
            
            if (selectedFiles.size > 0) {
                bulkActions.classList.add('show');
                selectedCount.textContent = `${selectedFiles.size} file${selectedFiles.size === 1 ? '' : 's'} selected`;
            } else {
                bulkActions.classList.remove('show');
            }
        }
        
        function toggleSelectAll() {
            const allSelected = selectedFiles.size === allFiles.length;
            
            if (allSelected) {
                selectedFiles.clear();
            } else {
                allFiles.forEach(file => {
                    selectedFiles.add(file.path);
                });
            }
            
            updateBulkActions();
            displayFiles(allFiles);
        }
        
        async function downloadSelected() {
            if (selectedFiles.size === 0) return;
            
            // Filter out directories (can't download directories)
            const filesToDownload = Array.from(selectedFiles).filter(filePath => {
                const file = allFiles.find(f => f.path === filePath);
                return file && !file.is_dir;
            });
            
            if (filesToDownload.length === 0) {
                showStatus('No files selected for download (directories cannot be downloaded)', 'error');
                return;
            }
            
            if (filesToDownload.length !== selectedFiles.size) {
                showStatus(`Downloading ${filesToDownload.length} files (directories skipped)`, 'success');
            }
            
            // Download files one by one
            for (const filePath of filesToDownload) {
                try {
                    const response = await fetch('/api/download?path=' + encodeURIComponent(filePath));
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = filePath.split('/').pop();
                        a.click();
                        window.URL.revokeObjectURL(url);
                        
                        // Small delay between downloads to avoid overwhelming the browser
                        await new Promise(resolve => setTimeout(resolve, 100));
                    } else {
                        showStatus(`Failed to download: ${filePath.split('/').pop()}`, 'error');
                    }
                } catch (error) {
                    showStatus(`Error downloading: ${filePath.split('/').pop()}`, 'error');
                }
            }
            
            showStatus(`Downloaded ${filesToDownload.length} file${filesToDownload.length === 1 ? '' : 's'}`, 'success');
        }
        
        async function deleteSelected() {
            if (selectedFiles.size === 0) return;
            
            const fileCount = selectedFiles.size;
            if (!confirm(`Are you sure you want to delete ${fileCount} file${fileCount === 1 ? '' : 's'}?`)) {
                return;
            }
            
            let successCount = 0;
            let failCount = 0;
            
            for (const filePath of selectedFiles) {
                try {
                    const response = await fetch('/api/delete', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ path: filePath })
                    });
                    
                    if (response.ok) {
                        successCount++;
                    } else {
                        failCount++;
                    }
                } catch (error) {
                    failCount++;
                }
            }
            
            if (successCount > 0) {
                showStatus(`Successfully deleted ${successCount} file${successCount === 1 ? '' : 's'}`, 'success');
            }
            if (failCount > 0) {
                showStatus(`Failed to delete ${failCount} file${failCount === 1 ? '' : 's'}`, 'error');
            }
            
            selectedFiles.clear();
            loadFiles();
        }
        
        function updateUploadPathDisplay() {
            document.getElementById('currentUploadPath').textContent = uploadDirectory;
        }
        
        async function selectUploadDirectory() {
            const newPath = prompt('Enter the full path to the directory where you want to save files:', uploadDirectory);
            if (newPath && newPath.trim() !== '') {
                // Validate the path by trying to list it
                try {
                    const response = await fetch(`/api/validate-directory?path=${encodeURIComponent(newPath.trim())}`);
                    if (response.ok) {
                        baseUploadDirectory = newPath.trim();
                        uploadDirectory = baseUploadDirectory + (currentPath ? '/' + currentPath : '');
                        updateUploadPathDisplay();
                        showStatus('Upload directory updated successfully', 'success');
                    } else {
                        showStatus('Invalid directory path. Please check the path and try again.', 'error');
                    }
                } catch (error) {
                    showStatus('Error validating directory path', 'error');
                }
            }
        }
        
        function resetUploadDirectory() {
            uploadDirectory = '~/Downloads';
            baseUploadDirectory = '~/Downloads';
            updateUploadPathDisplay();
            showStatus('Upload directory reset to default', 'success');
        }
        

        
        async function createFolderInCurrentDirectory() {
            const folderName = prompt('Enter the name for the new folder:', '');
            if (folderName && folderName.trim() !== '') {
                try {
                    // Create folder in the current directory being viewed
                    const currentDir = baseUploadDirectory + (currentPath ? '/' + currentPath : '');
                    const response = await fetch('/api/create-folder', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ 
                            path: currentDir,
                            folder_name: folderName.trim()
                        })
                    });
                    
                    if (response.ok) {
                        showStatus(`Folder "${folderName}" created successfully`, 'success');
                        loadFiles(); // Refresh the file list to show the new folder
                    } else {
                        showStatus('Failed to create folder', 'error');
                    }
                } catch (error) {
                    showStatus('Error creating folder', 'error');
                }
            }
        }
        

        
        function showFileMenu(filePath, isDirectory, event) {
            // Create a safe ID from the file path
            const safeId = filePath.replace(/[^a-zA-Z0-9]/g, '_');
            const menuId = `menu-${safeId}`;
            
            // Hide all other menus first
            const allMenus = document.querySelectorAll('.file-menu-popup');
            allMenus.forEach(menu => {
                if (menu.id !== menuId) {
                    menu.classList.remove('show');
                }
            });
            
            // Toggle the current menu
            const menu = document.getElementById(menuId);
            if (menu) {
                const isVisible = menu.classList.contains('show');
                
                if (isVisible) {
                    menu.classList.remove('show');
                } else {
                    menu.classList.add('show');
                    
                    // Position the menu relative to the button
                    const button = event.target;
                    const rect = button.getBoundingClientRect();
                    const menuRect = menu.getBoundingClientRect();
                    
                    // Position below the button, aligned to the right
                    menu.style.top = '100%';
                    menu.style.right = '0';
                    menu.style.left = 'auto';
                }
            }
        }
        
        // Close menus when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.file-menu-btn') && !event.target.closest('.file-menu-popup')) {
                const allMenus = document.querySelectorAll('.file-menu-popup');
                allMenus.forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/files', methods=['GET'])
def list_files():
    """List files in the transfer directory"""
    path = request.args.get('path', '')
    # Handle ~ expansion for relative paths
    if path and path.startswith('~/'):
        path = str(Path(path).expanduser())
    files = file_manager.list_files(path)
    return jsonify(files)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload from phone"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        path = request.form.get('path', '')
        upload_directory = request.form.get('upload_directory', file_manager.base_path)
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Create destination path using the specified upload directory
        dest_path = Path(upload_directory) / path / file.filename
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the file
        file.save(str(dest_path))
        
        return jsonify({'success': True, 'filename': file.filename})
    except Exception as e:
        print(f"Error uploading file: {e}")
        return jsonify({'error': 'Upload failed'}), 500

@app.route('/api/download', methods=['GET'])
def download_file():
    """Download a file to the phone"""
    try:
        path = request.args.get('path')
        if not path:
            return jsonify({'error': 'Path required'}), 400
        
        # Handle ~ expansion for relative paths
        if path.startswith('~/'):
            full_path = Path(path).expanduser()
        else:
            full_path = Path(file_manager.base_path) / path
        
        if not full_path.exists():
            return jsonify({'error': 'File not found'}), 404
        
        return send_from_directory(full_path.parent, full_path.name)
    except Exception as e:
        print(f"Error downloading file: {e}")
        return jsonify({'error': 'Download failed'}), 500

@app.route('/api/delete', methods=['POST'])
def delete_file():
    """Delete a file"""
    try:
        data = request.json
        path = data.get('path')
        
        if not path:
            return jsonify({'error': 'Path required'}), 400
        
        # Handle ~ expansion for relative paths
        if path.startswith('~/'):
            path = str(Path(path).expanduser())
        
        success = file_manager.delete_file(path)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Delete failed'}), 500
    except Exception as e:
        print(f"Error deleting file: {e}")
        return jsonify({'error': 'Delete failed'}), 500

@app.route('/api/validate-directory', methods=['GET'])
def validate_directory():
    """Validate if a directory path exists and is writable"""
    try:
        path = request.args.get('path')
        if not path:
            return jsonify({'error': 'Path required'}), 400
        
        # Handle ~ expansion for relative paths
        if path.startswith('~/'):
            dir_path = Path(path).expanduser()
        else:
            dir_path = Path(path)
        
        # Check if path exists and is a directory
        if not dir_path.exists():
            return jsonify({'error': 'Directory does not exist'}), 404
        
        if not dir_path.is_dir():
            return jsonify({'error': 'Path is not a directory'}), 400
        
        # Check if directory is writable by trying to create a test file
        test_file = dir_path / '.test_write_permission'
        try:
            test_file.touch()
            test_file.unlink()  # Remove the test file
        except (OSError, PermissionError):
            return jsonify({'error': 'Directory is not writable'}), 403
        
        return jsonify({'success': True, 'path': str(dir_path)})
    except Exception as e:
        print(f"Error validating directory: {e}")
        return jsonify({'error': 'Validation failed'}), 500

@app.route('/api/create-folder', methods=['POST'])
def create_folder():
    """Create a new folder in the specified directory"""
    try:
        data = request.json
        base_path = data.get('path')
        folder_name = data.get('folder_name')
        
        if not base_path or not folder_name:
            return jsonify({'error': 'Path and folder name required'}), 400
        
        # Handle ~ expansion for relative paths
        if base_path.startswith('~/'):
            base_path = str(Path(base_path).expanduser())
        
        # Sanitize folder name
        folder_name = folder_name.strip()
        if not folder_name or '/' in folder_name or '\\' in folder_name:
            return jsonify({'error': 'Invalid folder name'}), 400
        
        # Create the new folder
        new_folder_path = Path(base_path) / folder_name
        
        if new_folder_path.exists():
            return jsonify({'error': 'Folder already exists'}), 409
        
        new_folder_path.mkdir(parents=True, exist_ok=True)
        
        return jsonify({'success': True, 'path': str(new_folder_path)})
    except Exception as e:
        print(f"Error creating folder: {e}")
        return jsonify({'error': 'Failed to create folder'}), 500

@app.route('/api/info')
def get_info():
    """Get server information"""
    local_ip = file_manager.get_local_ip()
    return jsonify({
        'ip': local_ip,
        'port': 5001,
        'url': f'http://{local_ip}:5001'
    })

if __name__ == '__main__':
    local_ip = file_manager.get_local_ip()
    print(f"🌐 Web server starting...")
    print(f"📱 Open this URL on your phone: http://{local_ip}:5001")
    print(f"💻 Or on your Mac: http://localhost:5001")
    print(f"📁 Files will be saved to: {file_manager.base_path}")
    
    app.run(host='0.0.0.0', port=5001, debug=True)


