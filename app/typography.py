"""
Premium Typography Engine v3
Reference Style Edition
(Fixed)
"""

from pathlib import Path
import requests

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageFilter,
)

from app.themes import get_theme


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

FONTS = {
    "apple": "Manrope-SemiBold.ttf",
    "luxury": "CormorantGaramond-Bold.ttf",
    "podcast": "Inter-SemiBold.ttf",
    "finance": "IBMPlexSans-SemiBold.ttf",
    "book": "PlayfairDisplay-Bold.ttf",
    "travel": "PlusJakartaSans-SemiBold.ttf",
    "motivation": "Outfit-Bold.ttf",
    "stoic": "Inter-Medium.ttf",
    "neon": "SpaceGrotesk-Bold.ttf",
    "default": "Manrope-SemiBold.ttf",
}


FONT_DOWNLOADS = {
    "Manrope-SemiBold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/manrope/Manrope-SemiBold.ttf",

    "Inter-SemiBold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/inter/Inter-SemiBold.ttf",

    "Inter-Medium.ttf":
        "https://github.com/google/fonts/raw/main/ofl/inter/Inter-Medium.ttf",

    "Outfit-Bold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-Bold.ttf",

    "PlusJakartaSans-SemiBold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/plusjakartasans/PlusJakartaSans-SemiBold.ttf",

    "CormorantGaramond-Bold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/cormorantgaramond/CormorantGaramond-Bold.ttf",

    "IBMPlexSans-SemiBold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/ibmplexsans/IBMPlexSans-SemiBold.ttf",

    "PlayfairDisplay-Bold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay-Bold.ttf",

    "SpaceGrotesk-Bold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/spacegrotesk/SpaceGrotesk-Bold.ttf",
}


# --------------------------------------------------
# Font Downloader
# --------------------------------------------------

def ensure_font(font_name):

    FONT_DIR.mkdir(parents=True, exist_ok=True)

    font_path = FONT_DIR / font_name

    if font_path.exists():
        return font_path

    url = FONT_DOWNLOADS.get(font_name)

    if url is None:
        return FONT_DIR / FONTS["default"]

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    font_path.write_bytes(r.content)

    return font_path


# --------------------------------------------------
# Load Theme Font
# --------------------------------------------------

def get_font(size, theme_name="apple"):

    font_name = FONTS.get(theme_name, FONTS["default"])

    return ImageFont.truetype(str(ensure_font(font_name)), size)


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

        font = get_font(size, theme_name)

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

    font = get_font(34, theme_name)
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