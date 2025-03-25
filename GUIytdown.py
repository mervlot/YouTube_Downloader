"""Module to download YouTube videos using a GUI."""

# Importing required modules
import customtkinter as ctk
from customtkinter import CTkImage  # Import CTkImage for better image handling
import yt_dlp
from PIL import Image
import requests  # Import for fetching the thumbnail
import shutil  # Import for checking ffmpeg availability
import threading  # Import for running tasks in a separate thread


class App(ctk.CTk):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.title("Mervlot")
        self.geometry("600x480")
        self.resizable(True, True)  # Allow resizing
        ctk.set_appearance_mode("dark")
        self.current_frame = None
        self.grid_rowconfigure(0, weight=1)  # Make the frame fill the window
        self.grid_columnconfigure(0, weight=1)
        self.show_frame(Home)

    def show_frame(self, frame_class):
        """Destroy current frame and create a new one."""
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        # Use grid layout


class Home(ctk.CTkFrame):
    """Home frame containing the main UI components."""

    def __init__(self, parent, **kwargs):
        """Initialize the Home frame."""
        super().__init__(parent, **kwargs)
        self.grid_rowconfigure(3, weight=1)  # Make the layout responsive
        self.grid_columnconfigure(0, weight=1)
        self.header = ctk.CTkLabel(
            self, text="YouTube Video Downloader", font=("Arial", 20)
        )
        self.header.grid(row=0, column=0, pady=10, padx=10, sticky="n")
        self.label = ctk.CTkLabel(
            self, text="Enter a YouTube URL below:", font=("Arial", 14)
        )
        self.label.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.input = ctk.CTkEntry(self, width=400, height=40)
        self.input.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        self.button = ctk.CTkButton(
            self, text="Download Video", command=self.handle_download
        )
        self.button.grid(row=3, column=0, pady=10, padx=10, sticky="s")
        self.progress = ctk.CTkProgressBar(self)
        self.progress.grid(row=4, column=0, pady=10, padx=10, sticky="ew")
        self.progress.set(0)  # Initialize progress bar
        self.thumbnail_label = ctk.CTkLabel(self, text="")  # Placeholder for thumbnail
        self.thumbnail_label.grid(row=5, column=0, pady=10, padx=10, sticky="n")

    def handle_download(self):
        """Handle download button click."""
        url = self.input.get().strip()
        if not url:
            self.label.configure(text="Error: URL cannot be empty.", text_color="red")
            return
        if not url.startswith("http"):
            self.label.configure(text="Error: Invalid URL format.", text_color="red")
            return

        # Start the download in a separate thread
        threading.Thread(target=self.start_download, args=(url,), daemon=True).start()

    def start_download(self, url):
        """Start the download process."""
        self.display_thumbnail(url)  # Display the thumbnail
        self.download_video(url)

    def display_thumbnail(self, url):
        """Fetch and display the video thumbnail."""
        try:
            ydl_opts = {"quiet": True, "skip_download": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                thumbnail_url = info.get("thumbnail")
                if thumbnail_url:
                    response = requests.get(thumbnail_url, stream=True)
                    response.raise_for_status()
                    image_data = Image.open(response.raw)
                    image_data = image_data.resize((200, 150))  # Resize thumbnail
                    photo = CTkImage(
                        light_image=image_data, size=(200, 150)
                    )  # Use CTkImage
                    self.thumbnail_label.configure(image=photo, text="")
                    self.thumbnail_label.image = (
                        photo  # Keep a reference to avoid garbage collection
                    )
                else:
                    self.thumbnail_label.configure(
                        text="No thumbnail available.", text_color="orange"
                    )
        except yt_dlp.utils.DownloadError:
            self.thumbnail_label.configure(
                text="Error: Unable to fetch video info. Check the URL.",
                text_color="red",
            )
        except Exception as e:
            self.thumbnail_label.configure(
                text=f"Error loading thumbnail: {str(e)}", text_color="red"
            )

    def download_video(self, url):
        """Download video from YouTube."""
        self.label.configure(text="Loading...", text_color="blue")
        self.progress.set(0.2)  # Update progress bar
        try:
            ydl_opts = {
                "format": "best",
                "progress_hooks": [self.progress_hook],  # Add progress hook
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.label.configure(text="Download complete!", text_color="green")
            self.progress.set(1)  # Complete progress bar
        except yt_dlp.utils.DownloadError:
            self.label.configure(
                text="Error: Unable to download video. Check the URL.",
                text_color="red",
            )
            self.progress.set(0)  # Reset progress bar
        except Exception as e:
            self.label.configure(text=f"Error: {str(e)}", text_color="red")
            self.progress.set(0)  # Reset progress bar

    def progress_hook(self, d):
        """Update progress bar dynamically."""
        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes", 1)
            self.progress.set(downloaded / total)


if __name__ == "__main__":
    # Check if ffmpeg is installed
    if not shutil.which("ffmpeg"):
        print(
            "WARNING: ffmpeg not found. The downloaded format may not be the best available. "
            "Please install ffmpeg for better results: https://github.com/yt-dlp/yt-dlp#dependencies"
        )
    else:
        print("ffmpeg is installed and ready to use.")

    app = App()
    app.mainloop()
