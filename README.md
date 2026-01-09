youtube-downloader-pro

YouTube Downloader Pro is a Python-based YouTube downloader built on top of **yt-dlp**, providing both a **command-line interface (CLI)** and a **graphical user interface (GUI)** for downloading videos, audio, and playlists.

CLI Version – A terminal-based interactive downloader for quick and simple usage.
GUI Version – A modern Tkinter-based graphical interface with multiple format options and download progress tracking.

---

Features

CLI Version
- Interactive menu-driven interface.
- Download single videos or full playlists.
- Choose between:
  - Video + Audio (MP4, up to 1080p)
  - Video only (MP4, no audio)
  - Audio only (M4A, best quality)
- Automatic playlist folder organization.
- Clear console output with progress and error messages.
- No external GUI dependencies.

GUI Version
- Modern and clean Tkinter-based interface.
- Paste video or playlist URL directly.
- Select download format and quality.
- Choose output destination folder.
- Real-time progress bar.
- Status and error feedback.
- Two Windows executable builds:
  - GUI without console (clean user experience)
  - GUI with console (shows logs for debugging)

---

Installation

Clone the repository:

git clone https://github.com/David-Zamora04/youtube-downloader-pro.git
cd youtube-downloader-pro

(Optional) Create a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

Install dependencies:

pip install -U yt-dlp

Note:
FFmpeg is required for merging video and audio streams and for audio extraction.
Make sure `ffmpeg` is available in your system PATH or placed next to the executable.

---

Usage

CLI Version

Run the CLI script:

python youtube_downloader_cli.py

Follow the on-screen instructions to:
- Paste a YouTube video or playlist URL.
- Choose the download mode (1 / 2 / 3).
- Monitor progress directly in the terminal.
- Download multiple items in a single session.

---

GUI Version

Run the GUI script:

python youtube_downloader_gui.py

Or download the prebuilt Windows executables from the Releases page.

Steps:
- Paste the YouTube URL.
- Select the desired download format.
- Choose destination folder.
- Click the download button and track progress.

---

Building Executables (Windows)

You can build your own `.exe` files using PyInstaller:

GUI without console:

pyinstaller --onefile --noconsole youtube_downloader_gui.py

GUI with console (logs enabled):

pyinstaller --onefile youtube_downloader_gui.py

CLI executable:

pyinstaller --onefile youtube_downloader_cli.py

---

Contributing

Contributions are welcome.
Feel free to open issues or submit pull requests for:
- Bug fixes
- UI improvements
- Additional download options
- Performance enhancements

---

License

This project is intended for educational and personal use.
You are free to modify and adapt it.
Attribution is appreciated.

---

Notes

- Requires Python 3.8+
- Uses yt-dlp as the core downloading engine.
- FFmpeg is mandatory for audio extraction and video/audio merging.
- Playlist downloads are automatically organized into folders.
- The console GUI version is recommended for debugging and error tracking.
