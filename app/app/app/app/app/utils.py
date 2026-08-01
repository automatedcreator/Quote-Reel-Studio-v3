"""
Utility Functions
"""

from pathlib import Path
import random

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".mkv",
    ".avi"
}


def list_videos(folder):

    folder = Path(folder)

    videos = []

    for file in folder.iterdir():

        if file.suffix.lower() in VIDEO_EXTENSIONS:
            videos.append(file)

    return sorted(videos)


def random_video(folder):

    videos = list_videos(folder)

    if not videos:
        raise FileNotFoundError(
            "No videos found."
        )

    return random.choice(videos)


def ensure_directory(path):

    Path(path).mkdir(
        parents=True,
        exist_ok=True
    )
