"""
Typography Engine
"""

from pathlib import Path
import requests
from PIL import ImageFont

FONT_DIR = Path("assets/fonts")

FONT_FILE = FONT_DIR / "NotoSansDevanagari-Regular.ttf"

FONT_URL = (
    "https://github.com/googlefonts/noto-fonts/raw/main/"
    "hinted/ttf/NotoSansDevanagari/"
    "NotoSansDevanagari-Regular.ttf"
)


def ensure_font():

    FONT_DIR.mkdir(parents=True, exist_ok=True)

    if not FONT_FILE.exists():

        print("Downloading font...")

        response = requests.get(FONT_URL, timeout=30)

        response.raise_for_status()

        FONT_FILE.write_bytes(response.content)

    return FONT_FILE


def get_font(size):

    return ImageFont.truetype(
        str(ensure_font()),
        size
    )
