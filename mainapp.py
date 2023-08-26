import os
from flask import Flask, render_template, request, redirect, url_for
from pytube import Playlist, YouTube

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    playlist_url = request.form["playlist_url"]
    playlist = Playlist(playlist_url)
    path = os.path.join(os.path.abspath("."), playlist.title)

    if not os.path.isdir(path):
        os.mkdir(path)

    for url in playlist:
        try:
            video = YouTube(url)
            print(f"Downloading {video.title}")

            # Check if the file already exists before downloading again
            video_path = os.path.join(path, f"{video.title}.mp4")

            if os.path.isfile(video_path):
                print("Video already exists. Skipping...")
                continue

            stream = video.streams.get_highest_resolution()
            stream.download(output_path=path)
            print("Download completed.")

        except Exception as e:
            print(f"An error occurred while downloading the video: {e}")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
