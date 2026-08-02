"""
Premium Typography Engine
"""

from pathlib import Path
import textwrap
import requests

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from app.themes import get_theme

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


def get_font(size):

    return ImageFont.truetype(
        str(ensure_font()),
        size
    )


def create_quote_image(
    quote,
    output_path="temp/quote.png",
    theme_name="apple",
):

    Path("temp").mkdir(exist_ok=True)

    theme = get_theme(theme_name)

    img = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(img)

    font = get_font(
        theme["font_size"]
    )

    wrapped = textwrap.fill(
        f"“{quote.strip()}”",
        width=18
    )

    bbox = draw.multiline_textbbox(
        (0, 0),
        wrapped,
        font=font,
        spacing=20,
        align="center"
    )

    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (WIDTH - w) // 2

    position = theme.get(
        "text_position",
        "center"
    )

    if position == "upper":

        y = HEIGHT // 4

    elif position == "lower":

        y = int(HEIGHT * 0.65)

    elif position == "bottom":

        y = int(HEIGHT * 0.75)

    else:

        y = (HEIGHT - h) // 2

    blur = theme.get(
        "shadow_blur",
        4
    )

    shadow = theme.get(
        "shadow_color",
        (0, 0, 0)
    )

    for dx in range(-blur, blur + 1):
        for dy in range(-blur, blur + 1):

            if dx == 0 and dy == 0:
                continue

            draw.multiline_text(
                (x + dx, y + dy),
                wrapped,
                font=font,
                fill=shadow,
                spacing=20,
                align="center"
            )

    draw.multiline_text(
        (x, y),
        wrapped,
        font=font,
        fill=theme["text_color"],
        spacing=20,
        align="center"
    )

    img.save(output_path)

    return output_path