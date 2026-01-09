# YouTube Downloader

A modern YouTube downloader built in Python, featuring both **GUI** and **CLI** interfaces.  
Download videos, audio-only tracks, or entire playlists in high quality (MP4/M4A).  

This repository provides **Windows executables** for both GUI modes and a Python CLI script.

---

## 🚀 Features

- Download video + audio (up to 1080p, MP4)  
- Download video only (MP4, no audio)  
- Download audio only (M4A, 192 kbps)  
- Supports single videos and playlists  
- Lightweight GUI built with Tkinter  
- Command-line interface (CLI) for quick downloads  
- Windows executables available (`.exe`) with and without console logs  

---

## 🖥 GUI Version

### Available Executables

| Version | Description |
|---------|-------------|
| GUI without console | Clean interface only; no console window. Recommended for normal use. |
| GUI with console    | Shows a console window for logs, errors, and download details. Recommended for troubleshooting. |

### Usage

1. Download the `.exe` file from the [releases page](#).  
2. Double-click to open the application.  
3. Paste a YouTube video or playlist URL.  
4. Choose the download format (Video+Audio, Video only, or Audio only).  
5. Select destination folder and click **Download**.  

---

## 💻 CLI Version

### Usage

1. Ensure Python 3.8+ is installed.  
2. Open a terminal and navigate to the repo folder.  
3. Run the script:

```bash
python youtube_downloader_cli.py
