import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
from pytube import Playlist, YouTube
import re  # Import the re module for regular expressions

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    playlist_url = request.form["playlist_url"]
    playlist = Playlist(playlist_url)
    download_path = os.path.join(os.path.abspath("."), "downloads")

    if not os.path.exists(download_path):
        os.mkdir(download_path)

    video_links = []  # Store video download links
    c = 0  # to download all video remove this
    for url in playlist:
        try:
            c = c + 1  # to download all video remove this
            if c == 3:  # to download all video remove this
                break  # to download all video remove this

            video = YouTube(url)
            print(f"Downloading {video.title}")
            title = video.title.strip()
            print(title)

            # Sanitize the video title for use in URLs
            sanitized_title = re.sub(r"[^a-zA-Z0-9]", "_", title)

            # Check if the file already exists before downloading again
            video_path = os.path.join(download_path, f"{sanitized_title}.mp4")

            if os.path.isfile(video_path):
                print("Video already exists. Skipping...")
            else:
                stream = video.streams.get_highest_resolution()
                stream.download(
                    output_path=download_path, filename=f"{sanitized_title}.mp4"
                )

            # Generate download link for the user
            video_links.append((title, f"/downloads/{sanitized_title}.mp4"))

        except Exception as e:
            print(f"An error occurred while downloading the video: {e}")

    return render_template("download.html", video_links=video_links)


@app.route("/downloads/<filename>")
def serve_file(filename):
    # Ensure the requested file exists
    file_path = os.path.join(os.path.abspath("."), "downloads", filename)
    if os.path.isfile(file_path):
        return send_from_directory("downloads", filename)
    else:
        return "File not found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
