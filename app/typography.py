"""
Premium Typography Engine v2
"""

from pathlib import Path
import textwrap
import requests

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)

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


# ---------------------------------------------------
# Font
# ---------------------------------------------------

def ensure_font():

    FONT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

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


# ---------------------------------------------------
# Glass Card
# ---------------------------------------------------

def draw_glass_card(

    draw,

    box,

    theme,

):

    if not theme.get("card", True):
        return

    alpha = theme.get(
        "card_alpha",
        90
    )

    radius = theme.get(
        "card_radius",
        50
    )

    draw.rounded_rectangle(

        box,

        radius=radius,

        fill=(25, 25, 25, alpha),

        outline=(255, 255, 255, 18),

        width=2,

    )
    # ---------------------------------------------------
# Quote Image
# ---------------------------------------------------

def create_quote_image(

    quote,

    output_path="temp/quote.png",

    theme_name="apple",

):

    Path("temp").mkdir(
        exist_ok=True
    )

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

        width=22

    )

    bbox = draw.multiline_textbbox(

        (0, 0),

        wrapped,

        font=font,

        spacing=34,

        align="center"

    )

    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2

    padding_x = 90
    padding_y = 70

    card = (

        x - padding_x,

        y - padding_y,

        x + w + padding_x,

        y + h + padding_y,

    )

    draw_glass_card(

        draw,

        card,

        theme

    )

    shadow = theme.get(
        "shadow_color",
        (0, 0, 0)
    )

    blur = theme.get(
        "shadow_blur",
        4
    )

    for dx in range(-blur, blur + 1):

        for dy in range(-blur, blur + 1):

            if dx == 0 and dy == 0:
                continue

            draw.multiline_text(

                (

                    x + dx,

                    y + dy,

                ),

                wrapped,

                font=font,

                fill=shadow,

                spacing=34,

                align="center",

            )

    draw.multiline_text(

        (

            x,

            y,

        ),

        wrapped,

        font=font,

        fill=theme["text_color"],

        spacing=34,

        align="center",

    )

    img.save(output_path)

    return output_path