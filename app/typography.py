"""
Premium Typography Engine v3
Quote Reel Studio

Part 1 / 3
"""

from pathlib import Path
import textwrap
import requests

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageFilter,
)

from app.themes import get_theme
from app.presets import get_preset

# --------------------------------------------------------
# Canvas
# --------------------------------------------------------

WIDTH = 1080
HEIGHT = 1920

TOP_SAFE = 180
BOTTOM_SAFE = 260
SIDE_PADDING = 110

LINE_SPACING = 28

# --------------------------------------------------------
# Fonts
# --------------------------------------------------------

FONT_DIR = Path("assets/fonts")

DEFAULT_FONT = (
    FONT_DIR /
    "NotoSansDevanagari-Regular.ttf"
)

FONT_URL = (
    "https://github.com/googlefonts/noto-fonts/raw/main/"
    "hinted/ttf/NotoSansDevanagari/"
    "NotoSansDevanagari-Regular.ttf"
)

# --------------------------------------------------------
# Font Download
# --------------------------------------------------------

def ensure_font():

    FONT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not DEFAULT_FONT.exists():

        response = requests.get(
            FONT_URL,
            timeout=30
        )

        response.raise_for_status()

        DEFAULT_FONT.write_bytes(
            response.content
        )

    return DEFAULT_FONT


# --------------------------------------------------------
# Font Loader
# --------------------------------------------------------

def get_font(size):

    return ImageFont.truetype(
        str(ensure_font()),
        size
    )


# --------------------------------------------------------
# Theme Builder
# --------------------------------------------------------

def build_theme(
    theme_name,
    preset_name=None,
):

    theme = dict(
        get_theme(theme_name)
    )

    if preset_name:

        preset = get_preset(
            preset_name
        )

        if preset:

            theme.update(preset)

    return theme


# --------------------------------------------------------
# Font Size
# --------------------------------------------------------

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
        return int(base * 1.25)

    if words <= 15:
        return int(base * 1.10)

    if words <= 24:
        return base

    if words <= 35:
        return int(base * 0.90)

    if words <= 45:
        return int(base * 0.80)

    return int(base * 0.72)


# --------------------------------------------------------
# Wrap Width
# --------------------------------------------------------

def calculate_wrap_width(
    quote,
):

    words = len(
        quote.split()
    )

    if words <= 8:
        return 10

    if words <= 15:
        return 14

    if words <= 25:
        return 18

    if words <= 35:
        return 22

    return 26


# --------------------------------------------------------
# Quote Wrapper
# --------------------------------------------------------

def wrap_quote(
    quote,
):

    return textwrap.fill(
        f"“{quote.strip()}”",
        width=calculate_wrap_width(
            quote
        )
    )


# --------------------------------------------------------
# Measure Text
# --------------------------------------------------------

def measure_text(
    draw,
    text,
    font,
):

    box = draw.multiline_textbbox(
        (0, 0),
        text,
        font=font,
        spacing=LINE_SPACING,
        align="center",
    )

    width = box[2] - box[0]
    height = box[3] - box[1]

    return width, height


# --------------------------------------------------------
# Horizontal Position
# --------------------------------------------------------

def calculate_x(
    text_width,
):

    x = (
        WIDTH - text_width
    ) // 2

    return max(
        SIDE_PADDING,
        x
    )


# --------------------------------------------------------
# Vertical Position
# --------------------------------------------------------

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

    if position == "lower":

        return int(
            HEIGHT * 0.63
        )

    if position == "bottom":

        return (
            HEIGHT
            - text_height
            - BOTTOM_SAFE
        )

    return (
        HEIGHT
        - text_height
    ) // 2
# --------------------------------------------------------
# Premium Glass Card
# --------------------------------------------------------

def draw_card(
    img,
    x,
    y,
    width,
    height,
    theme,
):

    if not theme.get(
        "card",
        False
    ):
        return

    alpha = theme.get(
        "card_alpha",
        70
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
            x + width + padding,
            y + height + padding,
        ),

        radius=radius,

        fill=(
            0,
            0,
            0,
            alpha,
        ),

    )

    layer = layer.filter(

        ImageFilter.GaussianBlur(
            6
        )

    )

    img.alpha_composite(
        layer
    )


# --------------------------------------------------------
# Premium Shadow
# --------------------------------------------------------

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

    shadow = theme.get(
        "shadow_color",
        (0, 0, 0)
    )

    for dx in range(
        -blur,
        blur + 1,
    ):

        for dy in range(
            -blur,
            blur + 1,
        ):

            if dx == 0 and dy == 0:
                continue

            draw.multiline_text(

                (
                    x + dx,
                    y + dy,
                ),

                text,

                font=font,

                fill=shadow,

                spacing=LINE_SPACING,

                align="center",

            )


# --------------------------------------------------------
# Main Text Renderer
# --------------------------------------------------------

def draw_text(

    img,

    quote,

    theme,

):

    draw = ImageDraw.Draw(
        img
    )

    font_size = calculate_font_size(
        quote,
        theme,
    )

    font = get_font(
        font_size
    )

    wrapped = wrap_quote(
        quote
    )

    text_width, text_height = measure_text(

        draw,

        wrapped,

        font,

    )

    x = calculate_x(
        text_width
    )

    y = calculate_y(
        theme,
        text_height,
    )

    draw_card(

        img,

        x,

        y,

        text_width,

        text_height,

        theme,

    )

    draw = ImageDraw.Draw(
        img
    )

    draw_shadow(

        draw,

        wrapped,

        x,

        y,

        font,

        theme,

    )

    draw.multiline_text(

        (
            x,
            y,
        ),

        wrapped,

        font=font,

        fill=theme.get(
            "text_color",
            (
                255,
                255,
                255,
            ),
        ),

        spacing=LINE_SPACING,

        align="center",

    )
# --------------------------------------------------------
# Create Quote Image
# --------------------------------------------------------

def create_quote_image(

    quote,

    output_path="temp/quote.png",

    theme_name="apple",

    preset_name=None,

):

    Path("temp").mkdir(

        exist_ok=True

    )

    theme = build_theme(

        theme_name,

        preset_name,

    )

    img = Image.new(

        "RGBA",

        (

            WIDTH,

            HEIGHT,

        ),

        (

            0,

            0,

            0,

            0,

        ),

    )

    draw_text(

        img,

        quote,

        theme,

    )

    img.save(

        output_path

    )

    return output_path


# --------------------------------------------------------
# Test
# --------------------------------------------------------

if __name__ == "__main__":

    create_quote_image(

        "The quality of your future depends on the habits you repeat every day.",

        output_path="temp/test.png",

        theme_name="apple",

    )

    print(

        "Typography Engine Ready"

    )