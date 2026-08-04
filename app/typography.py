"""
Premium Typography Engine v3
Reference Style Edition
(Fixed)
"""

import re
import uuid
from pathlib import Path
import requests

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageFilter,
)

from app.themes import get_theme
from app.config import TEMP_DIR


# --------------------------------------------------
# Canvas
# --------------------------------------------------

WIDTH = 1080
HEIGHT = 1920

CONTENT_WIDTH = 760

TOP_SAFE = 180
BOTTOM_SAFE = 240
SIDE_PADDING = 110


# --------------------------------------------------
# Premium Fonts
# --------------------------------------------------

FONT_DIR = Path("assets/fonts")

# Each theme maps to a (family, named weight instance) pair. All of these
# families now ship from Google Fonts as a single variable-font file, so
# the "weight" is selected at load time via set_variation_by_name(), not
# via a separate static font file per weight.
FONTS = {
    "apple": ("Manrope", "SemiBold"),
    "luxury": ("CormorantGaramond", "Bold"),
    "podcast": ("Inter", "SemiBold"),
    "finance": ("IBMPlexSans", "SemiBold"),
    "book": ("PlayfairDisplay", "Bold"),
    "travel": ("PlusJakartaSans", "SemiBold"),
    "motivation": ("Outfit", "Bold"),
    "stoic": ("Inter", "Medium"),
    "neon": ("SpaceGrotesk", "Bold"),
    "default": ("Manrope", "SemiBold"),
}

# None of the fonts above contain Devanagari glyphs (Hindi/Marathi/etc.),
# so Hindi quotes would render as blank "tofu" boxes. Any quote containing
# Devanagari characters is automatically routed to this font instead,
# regardless of theme. Mukta ExtraBold has full Devanagari + Latin coverage.
DEVANAGARI_FONT = ("Mukta", "ExtraBold")
DEVANAGARI_PATTERN = re.compile(r"[\u0900-\u097F]")


def contains_devanagari(text):
    return bool(DEVANAGARI_PATTERN.search(text or ""))


FONT_DOWNLOADS = {
    "Manrope":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/Manrope%5Bwght%5D.ttf",

    "Inter":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",

    "Outfit":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/outfit/Outfit%5Bwght%5D.ttf",

    "PlusJakartaSans":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/plusjakartasans/PlusJakartaSans%5Bwght%5D.ttf",

    "CormorantGaramond":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf",

    "IBMPlexSans":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexsans/IBMPlexSans%5Bwdth%2Cwght%5D.ttf",

    "PlayfairDisplay":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf",

    "SpaceGrotesk":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf",

    "Mukta":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/mukta/Mukta-ExtraBold.ttf",
}


# --------------------------------------------------
# Font Downloader
# --------------------------------------------------

def ensure_font(family):

    FONT_DIR.mkdir(parents=True, exist_ok=True)

    font_path = FONT_DIR / f"{family}.ttf"

    if font_path.exists():
        return font_path

    url = FONT_DOWNLOADS.get(family)

    if url is None:
        default_family = FONTS["default"][0]
        return ensure_font(default_family)

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    font_path.write_bytes(r.content)

    return font_path


# --------------------------------------------------
# Load Theme Font
# --------------------------------------------------

def get_font(size, theme_name="apple", text=None):

    if contains_devanagari(text):
        family, weight = DEVANAGARI_FONT
    else:
        family, weight = FONTS.get(theme_name, FONTS["default"])

    font = ImageFont.truetype(str(ensure_font(family)), size)

    # These are variable fonts; select the desired weight by its named
    # instance. Falls back silently to the font's default weight if the
    # named instance isn't available (e.g. a non-variable font slipped in).
    try:
        font.set_variation_by_name(weight)
    except Exception:
        pass

    return font


# --------------------------------------------------
# Measure Single Line
# --------------------------------------------------

def text_width(draw, text, font):

    box = draw.textbbox((0, 0), text, font=font)

    return box[2] - box[0]


# --------------------------------------------------
# Premium Pixel Wrapper
# --------------------------------------------------

def wrap_quote(quote, font, draw):

    quote = f"\u201c{quote.strip()}\u201d"

    words = quote.split()

    lines = []
    current = ""

    for word in words:

        trial = word if current == "" else current + " " + word

        if text_width(draw, trial, font) <= CONTENT_WIDTH:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return "\n".join(lines)


# --------------------------------------------------
# Dynamic Font Fitting
# --------------------------------------------------

def fit_font_size(quote, theme_name):

    dummy = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(dummy)

    size = 86

    while size >= 34:

        font = get_font(size, theme_name, text=quote)

        wrapped = wrap_quote(quote, font, draw)

        bbox = draw.multiline_textbbox(
            (0, 0),
            wrapped,
            font=font,
            spacing=int(size * 0.20),
            align="center",
        )

        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        if w <= CONTENT_WIDTH and h <= 900:
            return (font, wrapped, w, h, int(size * 0.20))

        size -= 2

    font = get_font(34, theme_name, text=quote)
    wrapped = wrap_quote(quote, font, draw)

    bbox = draw.multiline_textbbox(
        (0, 0),
        wrapped,
        font=font,
        spacing=10,
        align="center",
    )

    return (font, wrapped, bbox[2] - bbox[0], bbox[3] - bbox[1], 10)


# --------------------------------------------------
# Optical Positioning
# --------------------------------------------------

def calculate_position(text_w, text_h, theme):

    x = (WIDTH - text_w) // 2
    x = max(SIDE_PADDING, x)

    layout = theme.get("text_position", "center")

    if layout == "upper":
        y = int(HEIGHT * 0.24)
    elif layout == "lower":
        y = int(HEIGHT * 0.60)
    elif layout == "bottom":
        y = HEIGHT - text_h - BOTTOM_SAFE
    else:
        y = (HEIGHT - text_h) // 2 - 35

    return x, y


# --------------------------------------------------
# Premium Glass Card
# --------------------------------------------------

def draw_card(img, x, y, w, h, theme):

    if not theme.get("card", False):
        return

    padding = 55
    radius = theme.get("card_radius", 42)
    alpha = theme.get("card_alpha", 65)

    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    painter = ImageDraw.Draw(layer)

    painter.rounded_rectangle(
        (x - padding, y - padding, x + w + padding, y + h + padding),
        radius=radius,
        fill=(0, 0, 0, alpha),
    )

    layer = layer.filter(ImageFilter.GaussianBlur(10))

    img.alpha_composite(layer)


# --------------------------------------------------
# Premium Stroke (theme-aware outline)
# --------------------------------------------------

def draw_stroke(draw, text, x, y, font, spacing, stroke_width, stroke_color):

    for ox in range(-stroke_width, stroke_width + 1):
        for oy in range(-stroke_width, stroke_width + 1):

            if ox == 0 and oy == 0:
                continue

            draw.multiline_text(
                (x + ox, y + oy),
                text,
                font=font,
                fill=stroke_color,
                spacing=spacing,
                align="center",
            )


# --------------------------------------------------
# Main Typography Renderer
# --------------------------------------------------

def draw_text(img, quote, theme_name, theme, output_path):
    """
    img must be an RGBA Pillow Image.
    Renders the wrapped/fitted quote onto img, applies optional card
    background, stroke outline, accent line and watermark, then saves
    to output_path.
    """

    draw = ImageDraw.Draw(img)

    font, wrapped, w, h, spacing = fit_font_size(quote, theme_name)

    x, y = calculate_position(w, h, theme)

    # Glass card background (optional)
    draw_card(img, x, y, w, h, theme)

    # Re-bind draw in case draw_card composited a new layer onto img
    draw = ImageDraw.Draw(img)

    # Stroke / outline
    stroke_width = theme.get("stroke", 2)
    stroke_color = theme.get("stroke_color", (0, 0, 0))

    draw_stroke(
        draw,
        wrapped,
        x,
        y,
        font,
        spacing,
        stroke_width,
        stroke_color,
    )

    # Main text fill
    draw.multiline_text(
        (x, y),
        wrapped,
        font=font,
        fill=theme.get("text_color", (255, 255, 255)),
        spacing=spacing,
        align="center",
    )

    # Accent line
    if theme.get("accent_line", False):

        line_width = int(w * 0.55)
        lx = (WIDTH - line_width) // 2
        ly = y + h + 70

        draw.rounded_rectangle(
            (lx, ly, lx + line_width, ly + 8),
            radius=8,
            fill=theme.get("accent_color", (255, 255, 255)),
        )

    # Watermark
    watermark = theme.get("watermark")

    if watermark:

        wm_font = get_font(34, theme_name)
        wm_color = (255, 255, 255, 120)

        draw.text(
            (WIDTH // 2, HEIGHT - 90),
            watermark,
            font=wm_font,
            fill=wm_color,
            anchor="mm",
        )

    # Save
    img.save(output_path)

    return output_path


# --------------------------------------------------
# Public Entry Point
# --------------------------------------------------

def create_quote_image(quote, theme_name="apple", preset_name=None):
    """
    Builds a transparent 1080x1920 PNG with the quote rendered on it,
    using the given theme/preset. This is the function main.py and
    ui.py call â€” it creates the canvas and delegates to draw_text().
    Returns the path to the saved PNG (str).
    """

    theme = get_theme(theme_name, preset_name)

    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))

    output_path = TEMP_DIR / f"quote_{uuid.uuid4().hex}.png"

    return draw_text(img, quote, theme_name, theme, str(output_path))