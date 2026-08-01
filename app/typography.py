"""
Typography Engine
"""

from pathlib import Path
import textwrap
import requests

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

WIDTH = 1080
HEIGHT = 1920

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
        r = requests.get(FONT_URL)
        r.raise_for_status()
        FONT_FILE.write_bytes(r.content)

    return FONT_FILE


def get_font(size=60):
    return ImageFont.truetype(str(ensure_font()), size)


def create_quote_image(
    quote,
    output_path="temp/quote.png"
):

    Path("temp").mkdir(exist_ok=True)

    img = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(img)

    font = get_font()

    wrapped = textwrap.fill(
        quote,
        width=18
    )

    bbox = draw.multiline_textbbox(
        (0, 0),
        wrapped,
        font=font,
        align="center",
        spacing=20
    )

    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2

    draw.multiline_text(
        (x + 4, y + 4),
        wrapped,
        font=font,
        fill=(0, 0, 0, 180),
        spacing=20,
        align="center"
    )

    draw.multiline_text(
        (x, y),
        wrapped,
        font=font,
        fill="white",
        spacing=20,
        align="center"
    )

    img.save(output_path)

    return output_path