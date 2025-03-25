# import yt_dlp

# def download_video(url):
#     try:
#         ydl_opts = {"format": "best"}
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])
#         print("Download complete!")
#     except Exception as e:
#         print("Error:", e)

# video_url = input("Enter YouTube video URL: ")
# download_video(video_url)


import yt_dlp


class ytDown:
    def __init__(self):
        pass

    def download_video(self, url):
        self.url = url
        try:
            ydl_opts = {"format": "best"}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            print("Download complete!")
        except Exception as e:
            print("Error:", e)


video_url = input("Enter YouTube video URL: ")
yt = ytDown()
yt.download_video(video_url)
