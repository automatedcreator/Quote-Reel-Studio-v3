"""
Premium Typography Engine v2
Inspired by Premium Instagram Quote Pages
"""

from pathlib import Path
import textwrap
import math
import requests

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageFilter
)

from app.themes import get_theme


# -------------------------------------------------------
# Canvas
# -------------------------------------------------------

WIDTH = 1080
HEIGHT = 1920


# -------------------------------------------------------
# Font
# -------------------------------------------------------

FONT_DIR = Path("assets/fonts")

DEFAULT_FONT = FONT_DIR / "NotoSansDevanagari-Regular.ttf"

FONT_URL = (
    "https://github.com/googlefonts/noto-fonts/raw/main/"
    "hinted/ttf/NotoSansDevanagari/"
    "NotoSansDevanagari-Regular.ttf"
)


# -------------------------------------------------------
# Download Font
# -------------------------------------------------------

def ensure_font():

    FONT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not DEFAULT_FONT.exists():

        r = requests.get(FONT_URL)

        r.raise_for_status()

        DEFAULT_FONT.write_bytes(
            r.content
        )

    return DEFAULT_FONT


# -------------------------------------------------------
# Load Font
# -------------------------------------------------------

def get_font(size):

    return ImageFont.truetype(

        str(

            ensure_font()

        ),

        size

    )


# -------------------------------------------------------
# Dynamic Font Size
# -------------------------------------------------------

def calculate_font_size(

    quote,

    theme,

):

    words = len(

        quote.split()

    )

    base = theme.get(

        "font_size",

        56

    )

    if words <= 8:

        return int(

            base * 1.25

        )

    elif words <= 15:

        return int(

            base * 1.10

        )

    elif words <= 24:

        return base

    elif words <= 35:

        return int(

            base * 0.88

        )

    elif words <= 45:

        return int(

            base * 0.78

        )

    else:

        return int(

            base * 0.70

        )


# -------------------------------------------------------
# Smart Wrap Width
# -------------------------------------------------------

def calculate_wrap_width(

    quote,

):

    words = len(

        quote.split()

    )

    if words <= 8:

        return 10

    elif words <= 15:

        return 14

    elif words <= 25:

        return 18

    elif words <= 35:

        return 22

    else:

        return 26


# -------------------------------------------------------
# Wrap Quote
# -------------------------------------------------------

def wrap_quote(

    quote,

):

    width = calculate_wrap_width(

        quote

    )

    return textwrap.fill(

        f"“{quote.strip()}”",

        width=width

    )
    # -------------------------------------------------------
# Instagram Safe Zones
# -------------------------------------------------------

TOP_SAFE = 180

BOTTOM_SAFE = 260

SIDE_PADDING = 110


# -------------------------------------------------------
# Theme Position
# -------------------------------------------------------

def calculate_y(

    theme,

    text_height,

):

    position = theme.get(

        "text_position",

        "center"

    )

    if position == "upper":

        return int(

            HEIGHT * 0.28

        )

    elif position == "lower":

        return int(

            HEIGHT * 0.63

        )

    elif position == "bottom":

        return (

            HEIGHT

            - text_height

            - BOTTOM_SAFE

        )

    else:

        return (

            HEIGHT

            - text_height

        ) // 2


# -------------------------------------------------------
# Measure Text
# -------------------------------------------------------

def measure_text(

    draw,

    text,

    font,

):

    bbox = draw.multiline_textbbox(

        (0, 0),

        text,

        font=font,

        spacing=28,

        align="center"

    )

    width = bbox[2] - bbox[0]

    height = bbox[3] - bbox[1]

    return width, height


# -------------------------------------------------------
# Horizontal Center
# -------------------------------------------------------

def calculate_x(

    text_width,

):

    x = (

        WIDTH

        - text_width

    ) // 2

    if x < SIDE_PADDING:

        x = SIDE_PADDING

    return x


# -------------------------------------------------------
# Premium Glass Card
# -------------------------------------------------------

def draw_card(

    img,

    x,

    y,

    w,

    h,

    theme,

):

    if not theme.get(

        "card",

        False

    ):

        return

    alpha = theme.get(

        "card_alpha",

        85

    )

    radius = theme.get(

        "card_radius",

        45

    )

    padding = 55

    layer = Image.new(

        "RGBA",

        img.size,

        (0, 0, 0, 0)

    )

    painter = ImageDraw.Draw(

        layer

    )

    painter.rounded_rectangle(

        (

            x - padding,

            y - padding,

            x + w + padding,

            y + h + padding,

        ),

        radius=radius,

        fill=(

            0,

            0,

            0,

            alpha

        )

    )

    layer = layer.filter(

        ImageFilter.GaussianBlur(

            6

        )

    )

    img.alpha_composite(

        layer

    )


# -------------------------------------------------------
# Premium Shadow
# -------------------------------------------------------

def draw_shadow(

    draw,

    text,

    x,

    y,

    font,

    theme,

):

    blur = theme.get(

        "shadow_blur",

        4

    )

    color = theme.get(

        "shadow_color",

        (0, 0, 0)

    )

    for dx in range(

        -blur,

        blur + 1

    ):

        for dy in range(

            -blur,

            blur + 1

        ):

            if dx == 0 and dy == 0:

                continue

            draw.multiline_text(

                (

                    x + dx,

                    y + dy

                ),

                text,

                font=font,

                fill=color,

                spacing=28,

                align="center"

            )
            # -------------------------------------------------------
# Create Quote Image
# -------------------------------------------------------

def create_quote_image(

    quote,

    output_path="temp/quote.png",

    theme_name="apple",

    preset_name=None,

):

    Path("temp").mkdir(

        exist_ok=True

    )

    theme = get_theme(

        theme_name,

        preset_name

    )

    font_size = calculate_font_size(

        quote,

        theme

    )

    font = get_font(

        font_size

    )

    text = wrap_quote(

        quote

    )

    img = Image.new(

        "RGBA",

        (

            WIDTH,

            HEIGHT

        ),

        (

            0,

            0,

            0,

            0

        )

    )

    draw = ImageDraw.Draw(

        img

    )

    text_width, text_height = measure_text(

        draw,

        text,

        font

    )

    x = calculate_x(

        text_width

    )

    y = calculate_y(

        theme,

        text_height

    )

    draw_card(

        img,

        x,

        y,

        text_width,

        text_height,

        theme

    )

    draw = ImageDraw.Draw(

        img

    )

    draw_shadow(

        draw,

        text,

        x,

        y,

        font,

        theme

    )

    draw.multiline_text(

        (

            x,

            y

        ),

        text,

        font=font,

        fill=theme.get(

            "text_color",

            (

                255,

                255,

                255

            )

        ),

        spacing=28,

        align="center"

    )

    img.save(

        output_path

    )

    return output_path