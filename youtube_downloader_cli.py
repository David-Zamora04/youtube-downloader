import yt_dlp
import sys


def main():
    print("=== Simple YouTube Downloader (no external dependencies) ===\n")

    # URL input
    print("Paste the video or playlist URL:")
    print("(type 'exit' or press Enter to quit)\n")
    url = input("URL: ").strip()

    if not url or url.lower() in ['exit', 'quit', 'q']:
        print("\nGoodbye!")
        sys.exit(0)

    if "youtube.com" not in url and "youtu.be" not in url:
        print("This does not look like a YouTube URL. Please try again.\n")
        return main()

    # Options menu
    print("\nWhat do you want to download?")
    print("  1) Video + Audio     (best <=1080p, mp4 with sound)")
    print("  2) Video only        (no audio, mp4)")
    print("  3) Audio only        (best quality, m4a)")
    print()

    while True:
        choice = input("Choose (1 / 2 / 3): ").strip()
        if choice in ["1", "2", "3"]:
            break
        print("Please choose 1, 2, or 3")

    if choice == "1":
        format_sel = "bestvideo[ext=mp4][vcodec=h264][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]"
        merge_format = "mp4"
        postprocessors = [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        }]
        desc = "Video + Audio (mp4)"

    elif choice == "2":
        format_sel = "bestvideo[ext=mp4][vcodec=h264][height<=1080]/bestvideo[ext=mp4][height<=1080]"
        merge_format = None
        postprocessors = []
        desc = "Video only (mp4, no audio)"

    else:  # choice == "3"
        format_sel = "bestaudio[ext=m4a]/bestaudio/best"
        merge_format = None
        postprocessors = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
            "preferredquality": "192",
        }]
        desc = "Audio only (m4a)"

    # Output filename: playlist structure if available, otherwise single title
    outtmpl = "%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s" if "%(playlist_title)s" else "%(title)s.%(ext)s"

    ydl_opts = {
        "format": format_sel,
        "outtmpl": outtmpl,
        "merge_output_format": merge_format,
        "postprocessors": postprocessors,
        "noplaylist": False,
        "extractor_args": {"youtube": {"player_client": ["default", "ios"]}},
        "quiet": False,
        "no_warnings": False,
    }

    print(f"\nDownloading → {url}")
    print(f"Mode: {desc}")
    print("Starting...\n")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\nDownload completed successfully!\n")

    except Exception as e:
        print("\nAn error occurred:")
        print(e)
        print("\nPossible solutions:")
        print("- Update yt-dlp → pip install -U yt-dlp")
        print("- Make sure ffmpeg is installed (required for merging and audio extraction)")
        print("- Try another URL or a different mode")

    # Ask if the user wants to continue
    print("\nDo you want to download something else? (Enter = yes / any text = no)")
    if input().strip() == "":
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        sys.exit(0)
