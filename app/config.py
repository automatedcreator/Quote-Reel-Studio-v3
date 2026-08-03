"""
Global Configuration
"""

from pathlib import Path

# ---------------------------------------
# Video
# ---------------------------------------

WIDTH = 1080
HEIGHT = 1920

FPS = 30

CLIP_DURATION = 20

VIDEO_CODEC = "libx264"

AUDIO_CODEC = "aac"

PRESET = "medium"

THREADS = 4


# ---------------------------------------
# Project
# ---------------------------------------

PROJECT_NAME = "Quote Reel Studio"

VERSION = "1.0"

DEFAULT_THEME = "apple"


# ---------------------------------------
# Directories
# ---------------------------------------

ROOT_DIR = Path(".")

OUTPUT_DIR = ROOT_DIR / "output"

PROJECTS_DIR = ROOT_DIR / "Projects"

TEMP_DIR = ROOT_DIR / "temp"

VIDEOS_DIR = ROOT_DIR / "videos"

QUOTES_DIR = ROOT_DIR / "quotes"

ASSETS_DIR = ROOT_DIR / "assets"

FONT_DIR = ASSETS_DIR / "fonts"


# ---------------------------------------
# Export
# ---------------------------------------

EXPORT_ZIP_NAME = "reels.zip"

SUMMARY_FILE = "summary.txt"

CAPTIONS_FILE = "captions.txt"

HASHTAGS_FILE = "hashtags.txt"


# ---------------------------------------
# Instagram
# ---------------------------------------

REEL_MAX_DURATION = 90

RECOMMENDED_DURATION = 20

ASPECT_RATIO = "9:16"


# ---------------------------------------
# Create Folders
# ---------------------------------------

for folder in [

    OUTPUT_DIR,

    PROJECTS_DIR,

    TEMP_DIR,

    VIDEOS_DIR,

    QUOTES_DIR,

    FONT_DIR,

]:

    folder.mkdir(

        parents=True,

        exist_ok=True

    )