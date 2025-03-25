from pytube import YouTube


def download_video(link):
    yt = YouTube(link)
    yt_stream = yt.streams.get_highest_resolution()
    try:
        yt_stream.download()
        print("Video downloaded successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


link = "https://youtube.com/shorts/0PaEzOyFi8s?si=KxEpLaLXI5hbSjFC"
download_video(link)
