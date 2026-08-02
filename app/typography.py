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

DEFAULT_FONT = FONT_DIR / "NotoSansDevanagari-Regular.ttf"

FONT_URL = (
    "https://github.com/googlefonts/noto-fonts/raw/main/"
    "hinted/ttf/NotoSansDevanagari/"
    "NotoSansDevanagari-Regular.ttf"
)


# ------------------------------------
# Font
# ------------------------------------

def ensure_font():

    FONT_DIR.mkdir(parents=True, exist_ok=True)

    if not DEFAULT_FONT.exists():

        r = requests.get(FONT_URL)

        r.raise_for_status()

        DEFAULT_FONT.write_bytes(r.content)

    return DEFAULT_FONT


def load_font(size):

    return ImageFont.truetype(
        str(ensure_font()),
        size
    )


# ------------------------------------
# Auto Font Size
# ------------------------------------

def auto_font(draw, text, theme):

    size = theme["font_size"]

    while size > 40:

        font = load_font(size)

        wrapped = textwrap.fill(
            text,
            width=max(12, int(1100 / size))
        )

        bbox = draw.multiline_textbbox(
            (0, 0),
            wrapped,
            font=font,
            spacing=theme["line_spacing"],
            align="center"
        )

        width = bbox[2] - bbox[0]

        if width <= theme["text_width"]:
            return font, wrapped

        size -= 2

    return load_font(40), wrapped


# ------------------------------------
# Shadow
# ------------------------------------

def draw_shadow(draw, pos, text, font, theme):

    x, y = pos

    for ox in [-3, -2, -1, 1, 2, 3]:

        for oy in [-3, -2, -1, 1, 2, 3]:

            draw.multiline_text(
                (x + ox, y + oy),
                text,
                font=font,
                fill=theme["shadow_color"],
                spacing=theme["line_spacing"],
                align="center"
            )
            # ------------------------------------
# Main
# ------------------------------------

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

    # Premium Quote Marks
    quote = f"“{quote.strip()}”"

    font, wrapped = auto_font(
        draw,
        quote,
        theme
    )

    bbox = draw.multiline_textbbox(
        (0, 0),
        wrapped,
        font=font,
        spacing=theme["line_spacing"],
        align="center"
    )

    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2

    # Shadow
    draw_shadow(
        draw,
        (x, y),
        wrapped,
        font,
        theme
    )

    # Main Text
    draw.multiline_text(
        (x, y),
        wrapped,
        font=font,
        fill=theme["text_color"],
        spacing=theme["line_spacing"],
        align="center"
    )

    img.save(output_path)

    return output_path