from fastapi import FastAPI, HTTPException
from pytubefix import YouTube
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# cors
origins = [
    "*",
    "http://localhost:5173/",
    "http://127.0.0.1:5173/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the YouTube video downloader API!"}

@app.post("/video/")
async def download_video(request: VideoRequest):
    """
    Endpoint to download a YouTube video.
    Takes a video URL and returns the download path or error.
    """
    try:
        # Initialize YouTube object with the URL
        yt = YouTube(request.url)

        # Get the stream (highest resolution available)
        stream = yt.streams.get_highest_resolution()

        # Create a directory for downloads if it doesn't exist
        download_dir = "downloads"
        os.makedirs(download_dir, exist_ok=True)

        # Download the video
        download_path = os.path.join(download_dir, f"{yt.title}.mp4")
        stream.download(output_path=download_dir, filename=f"{yt.title}.mp4")

        return {"message": "Download successful", "file_path": download_path}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error downloading video: {str(e)}")




@app.post("/audio/")
async def download_audio(request: VideoRequest):
    """
    Endpoint to download a YouTube video.
    Takes a video URL and returns the download path or error.
    """
    try:
        # Initialize YouTube object with the URL
        yt = YouTube(request.url)

        # Get the stream (highest resolution available)
        stream = yt.streams.get_audio_only()

        # Create a directory for downloads if it doesn't exist
        download_dir = "downloads"
        os.makedirs(download_dir, exist_ok=True)

        # Download the video
        download_path = os.path.join(download_dir, f"{yt.title}.mp4")
        stream.download(output_path=download_dir, filename=f"{yt.title}.m4a")

        return {"message": "Download successful", "file_path": download_path}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error downloading video: {str(e)}")





@app.get("/info/{video_id}")
async def get_video_info(video_id: str):
    """
    Endpoint to get YouTube video info (title, author, duration, etc.)
    """
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        
        # Get video details
        video_info = {
            "title": yt.title,
            "author": yt.author,
            "length": yt.length,
            "views": yt.views,
            "description": yt.description[:200],  # Preview first 200 characters
            "thumbnail": yt.thumbnail_url,
        }

        return video_info

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Video not found: {str(e)}")
