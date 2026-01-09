import yt_dlp
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path


class YouTubeDownloader:
    """
    Modern YouTube downloader with GUI built using Tkinter.
    Supports video, audio-only, and playlist downloads via yt-dlp.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("850x720")
        self.root.resizable(False, False)

        # Tkinter variables
        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="1")
        self.output_path = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.is_downloading = False

        # Color palette (dark modern UI)
        self.colors = {
            'bg': '#0a0a0a',
            'card': '#1e1e1e',
            'card_hover': '#252525',
            'input_bg': '#2d2d2d',
            'input_border': '#3d3d3d',
            'primary': '#ff0033',
            'primary_hover': '#e6002e',
            'primary_shadow': '#cc0028',
            'accent': '#00d9ff',
            'text': '#ffffff',
            'text_secondary': '#b3b3b3',
            'text_dim': '#808080',
            'success': '#00e676',
            'error': '#ff1744',
        }

        self.root.configure(bg=self.colors['bg'])
        self.setup_styles()
        self.create_gui()

    def setup_styles(self):
        """Configure custom ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Modern.Horizontal.TProgressbar",
            troughcolor=self.colors['input_bg'],
            background=self.colors['primary'],
            borderwidth=0,
            thickness=8
        )

    def create_gui(self):
        """Create and assemble all UI sections."""
        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=40, pady=25)

        self.create_header(main)
        self.create_url_section(main)
        self.create_quality_section(main)
        self.create_destination_section(main)
        self.create_download_button(main)
        self.create_progress_section(main)

    # ================= HEADER =================
    def create_header(self, parent):
        """Application title and subtitle."""
        header = tk.Frame(parent, bg=self.colors['bg'])
        header.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            header,
            text="YouTube Downloader",
            bg=self.colors['bg'],
            fg=self.colors['text'],
            font=("Segoe UI", 24, "bold")
        ).pack()

        tk.Label(
            header,
            text="Download videos and playlists in high quality",
            bg=self.colors['bg'],
            fg=self.colors['text_secondary'],
            font=("Segoe UI", 10)
        ).pack(pady=(4, 8))

        tk.Frame(header, bg=self.colors['primary'], height=2)\
            .pack(fill=tk.X, padx=220)

    # ================= URL =================
    def create_url_section(self, parent):
        """YouTube video or playlist URL input."""
        section = tk.Frame(parent, bg=self.colors['bg'])
        section.pack(fill=tk.X, pady=(12, 0))

        tk.Label(
            section,
            text="Video or Playlist URL",
            bg=self.colors['bg'],
            fg=self.colors['text'],
            font=("Segoe UI", 11, "bold")
        ).pack(anchor=tk.W, pady=(0, 6))

        card = tk.Frame(section, bg=self.colors['card'])
        card.pack(fill=tk.X)

        content = tk.Frame(card, bg=self.colors['card'])
        content.pack(fill=tk.X, padx=18, pady=12)

        entry_bg = tk.Frame(content, bg=self.colors['input_bg'])
        entry_bg.pack(fill=tk.X)

        self.url_entry = tk.Entry(
            entry_bg,
            textvariable=self.url_var,
            bg=self.colors['input_bg'],
            fg=self.colors['text_dim'],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            insertbackground=self.colors['primary']
        )
        self.url_entry.pack(fill=tk.X, ipady=8, padx=12)

        placeholder = "Paste the YouTube URL here..."
        self.url_entry.insert(0, placeholder)

        def on_focus_in(e):
            if self.url_entry.get() == placeholder:
                self.url_entry.delete(0, tk.END)
                self.url_entry.config(fg=self.colors['text'])

        def on_focus_out(e):
            if not self.url_entry.get():
                self.url_entry.insert(0, placeholder)
                self.url_entry.config(fg=self.colors['text_dim'])

        self.url_entry.bind("<FocusIn>", on_focus_in)
        self.url_entry.bind("<FocusOut>", on_focus_out)

    # ================= QUALITY =================
    def create_quality_section(self, parent):
        """Download format and quality options."""
        section = tk.Frame(parent, bg=self.colors['bg'])
        section.pack(fill=tk.X, pady=(12, 0))

        tk.Label(
            section,
            text="Download Format",
            bg=self.colors['bg'],
            fg=self.colors['text'],
            font=("Segoe UI", 11, "bold")
        ).pack(anchor=tk.W, pady=(0, 6))

        card = tk.Frame(section, bg=self.colors['card'])
        card.pack(fill=tk.X)

        content = tk.Frame(card, bg=self.colors['card'])
        content.pack(fill=tk.X, padx=18, pady=10)

        options = [
            ("1", "Video + Audio (MP4)", "Up to 1080p"),
            ("2", "Video Only (MP4)", "No audio"),
            ("3", "Audio Only (M4A)", "192 kbps"),
        ]

        for value, title, desc in options:
            opt = tk.Frame(content, bg=self.colors['input_bg'])
            opt.pack(fill=tk.X, pady=3)

            tk.Radiobutton(
                opt,
                variable=self.quality_var,
                value=value,
                bg=self.colors['input_bg'],
                fg=self.colors['primary'],
                selectcolor=self.colors['input_bg']
            ).pack(side=tk.LEFT, padx=8)

            text = tk.Frame(opt, bg=self.colors['input_bg'])
            text.pack(side=tk.LEFT)

            tk.Label(
                text,
                text=title,
                bg=self.colors['input_bg'],
                fg=self.colors['text'],
                font=("Segoe UI", 9, "bold")
            ).pack(anchor=tk.W)

            tk.Label(
                text,
                text=desc,
                bg=self.colors['input_bg'],
                fg=self.colors['text_secondary'],
                font=("Segoe UI", 8)
            ).pack(anchor=tk.W)

    # ================= DESTINATION =================
    def create_destination_section(self, parent):
        """Output directory selector."""
        section = tk.Frame(parent, bg=self.colors['bg'])
        section.pack(fill=tk.X, pady=(12, 0))

        tk.Label(
            section,
            text="Destination Folder",
            bg=self.colors['bg'],
            fg=self.colors['text'],
            font=("Segoe UI", 11, "bold")
        ).pack(anchor=tk.W, pady=(0, 6))

        card = tk.Frame(section, bg=self.colors['card'])
        card.pack(fill=tk.X)

        content = tk.Frame(card, bg=self.colors['card'])
        content.pack(fill=tk.X, padx=18, pady=10)

        path_frame = tk.Frame(content, bg=self.colors['input_bg'])
        path_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            path_frame,
            textvariable=self.output_path,
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            font=("Segoe UI", 9),
            anchor=tk.W
        ).pack(fill=tk.X, padx=10, pady=6)

        tk.Button(
            content,
            text="Browse",
            bg=self.colors['primary'],
            fg=self.colors['text'],
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            command=self.browse_folder
        ).pack(side=tk.RIGHT, padx=(10, 0), ipady=4)

    # ================= DOWNLOAD =================
    def create_download_button(self, parent):
        """Main download button."""
        self.download_button = tk.Button(
            parent,
            text="DOWNLOAD NOW",
            bg=self.colors['primary'],
            fg=self.colors['text'],
            font=("Segoe UI", 13, "bold"),
            relief=tk.FLAT,
            command=self.start_download
        )
        self.download_button.pack(fill=tk.X, pady=(15, 0), ipady=10)

    # ================= PROGRESS =================
    def create_progress_section(self, parent):
        """Download progress and status display."""
        section = tk.Frame(parent, bg=self.colors['bg'])
        section.pack(fill=tk.X, pady=(15, 0))

        card = tk.Frame(section, bg=self.colors['card'])
        card.pack(fill=tk.X)

        content = tk.Frame(card, bg=self.colors['card'])
        content.pack(fill=tk.X, padx=18, pady=12)

        self.status_label = tk.Label(
            content,
            text="Waiting...",
            bg=self.colors['card'],
            fg=self.colors['text_secondary'],
            font=("Segoe UI", 10, "bold")
        )
        self.status_label.pack(anchor=tk.W, pady=(0, 6))

        self.progress = ttk.Progressbar(
            content,
            style="Modern.Horizontal.TProgressbar",
            mode="determinate",
            maximum=100
        )
        self.progress.pack(fill=tk.X)

        self.detail_label = tk.Label(
            content,
            text="",
            bg=self.colors['card'],
            fg=self.colors['text_secondary'],
            font=("Segoe UI", 8)
        )
        self.detail_label.pack(anchor=tk.W, pady=(6, 0))

    # ================= LOGIC (UNCHANGED) =================
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_path.get())
        if folder:
            self.output_path.set(folder)

    def start_download(self):
        if self.is_downloading:
            return

        url = self.url_var.get().strip()
        if "youtube" not in url:
            messagebox.showerror("Error", "Invalid URL")
            return

        self.is_downloading = True
        self.download_button.config(state=tk.DISABLED, bg=self.colors['input_bg'])
        self.status_label.config(text="Starting download...")
        self.progress['value'] = 0

        threading.Thread(
            target=self.download,
            args=(url, self.output_path.get()),
            daemon=True
        ).start()

    def download(self, url, output):
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                is_playlist = 'entries' in info

            q = self.quality_var.get()
            if q == "1":
                fmt = "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]"
                pp = [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}]
            elif q == "2":
                fmt = "bestvideo[ext=mp4][height<=1080]"
                pp = []
            else:
                fmt = "bestaudio[ext=m4a]/bestaudio"
                pp = [{"key": "FFmpegExtractAudio", "preferredcodec": "m4a", "preferredquality": "192"}]

            outtmpl = os.path.join(
                output,
                "%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s"
                if is_playlist else "%(title)s.%(ext)s"
            )

            opts = {
                "format": fmt,
                "outtmpl": outtmpl,
                "postprocessors": pp,
                "progress_hooks": [self.progress_hook],
            }

            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])

            self.root.after(0, self.on_complete)

        except Exception as e:
            self.root.after(0, lambda: self.on_error(str(e)))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            if total:
                percent = d.get('downloaded_bytes', 0) / total * 100
                self.root.after(
                    0,
                    lambda: self.progress.config(value=percent)
                )

    def on_complete(self):
        self.is_downloading = False
        self.download_button.config(state=tk.NORMAL, bg=self.colors['primary'])
        self.status_label.config(text="Download completed")

    def on_error(self, error):
        self.is_downloading = False
        self.download_button.config(state=tk.NORMAL, bg=self.colors['primary'])
        self.status_label.config(text="Error")
        messagebox.showerror("Error", error)


def main():
    """Application entry point."""
    root = tk.Tk()
    app = YouTubeDownloader(root)

    # Center window on screen
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
