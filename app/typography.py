"""
Premium Typography Engine v4
Reference Style Edition + Two-Tone Highlighting + Emoji Support
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

# Emoji fallback font. Main theme fonts (and Mukta) have no emoji glyphs,
# so any emoji characters found in a quote are rendered with this font
# instead, mixed inline word-by-word / run-by-run with the main text.
EMOJI_FONT = "NotoEmoji"

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"  # symbols, pictographs, emoticons, supplemental
    "\U00002600-\U000027BF"  # misc symbols & dingbats (â˜€ â¤ âœ… âœ¨ etc.)
    "\U0001F1E6-\U0001F1FF"  # regional indicators (flags)
    "\U00002190-\U000021FF"  # arrows
    "\U0000FE0F"             # variation selector-16
    "\U0000200D"             # zero-width joiner (emoji sequences)
    "]"
)


def contains_devanagari(text):
    return bool(DEVANAGARI_PATTERN.search(text or ""))


def is_emoji_char(ch):
    return bool(EMOJI_PATTERN.match(ch))


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

    "NotoEmoji":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/notoemoji/NotoEmoji%5Bwght%5D.ttf",
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
# Load Theme / Emoji Fonts
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


def get_emoji_font(size):
    return ImageFont.truetype(str(ensure_font(EMOJI_FONT)), size)


# --------------------------------------------------
# Measure Text
# --------------------------------------------------

def text_width(draw, text, font):

    box = draw.textbbox((0, 0), text, font=font)

    return box[2] - box[0]


def line_height_for(font, draw):
    # Probe string covering Latin ascenders/descenders and Devanagari
    # matras (above/below-baseline marks) so the measured height covers
    # the tallest/deepest glyphs likely to appear in a real quote.
    probe = "Agjpqà¤•à¥€à¥‚à¤à¥ˆà¤‚h"
    box = draw.textbbox((0, 0), probe, font=font)
    return box[3] - box[1]


# --------------------------------------------------
# Accent-word markup: **word** -> highlighted in accent_color.
# If a quote has no ** markup at all, the first wrapped line is
# auto-highlighted instead (matches the two-tone look seen across
# most reference reels) unless the theme opts out.
# --------------------------------------------------

ACCENT_SPLIT_RE = re.compile(r"(\*\*.+?\*\*)")


def tokenize_accents(quote):

    tokens = []

    for chunk in ACCENT_SPLIT_RE.split(quote):

        if not chunk:
            continue

        if chunk.startswith("**") and chunk.endswith("**"):
            for word in chunk[2:-2].split():
                tokens.append((word, True))
        else:
            for word in chunk.split():
                tokens.append((word, False))

    return tokens


# --------------------------------------------------
# Emoji-aware run splitting
# --------------------------------------------------

def split_runs(word):
    """Split a word into consecutive runs of (text, is_emoji)."""

    runs = []
    current = ""
    current_is_emoji = None

    for ch in word:

        e = is_emoji_char(ch)

        if current_is_emoji is None:
            current = ch
            current_is_emoji = e
        elif e == current_is_emoji:
            current += ch
        else:
            runs.append((current, current_is_emoji))
            current = ch
            current_is_emoji = e

    if current:
        runs.append((current, current_is_emoji))

    return runs


def measure_word(draw, word, font, emoji_font):
    """Returns (runs, total_width) where runs is [(text, font_used, width)]."""

    runs = []
    total = 0

    for run_text, is_emoji in split_runs(word):

        font_used = emoji_font if is_emoji else font
        w = text_width(draw, run_text, font_used)

        runs.append((run_text, font_used, w))
        total += w

    return runs, total


# --------------------------------------------------
# Word Wrapping (accent + emoji aware)
# --------------------------------------------------

def wrap_words(tokens, font, emoji_font, draw, max_width):

    space_width = text_width(draw, " ", font)

    lines = []
    current_line = []
    current_width = 0

    for word, accent in tokens:

        runs, width = measure_word(draw, word, font, emoji_font)

        extra = width if not current_line else space_width + width

        if current_line and (current_width + extra) > max_width:
            lines.append(current_line)
            current_line = []
            current_width = 0
            extra = width

        current_line.append({
            "text": word,
            "accent": accent,
            "runs": runs,
            "width": width,
        })
        current_width += extra

    if current_line:
        lines.append(current_line)

    return lines, space_width


def apply_quote_marks(tokens):

    if not tokens:
        return tokens

    tokens = list(tokens)
    first_word, first_accent = tokens[0]
    last_word, last_accent = tokens[-1]

    tokens[0] = ("\u201c" + first_word, first_accent)
    tokens[-1] = (last_word + "\u201d", last_accent)

    return tokens


def apply_auto_highlight(lines):
    """If nothing was manually marked with **word**, highlight the first
    wrapped line automatically â€” the two-tone look seen in most reference
    reels, without requiring the quote text to be specially formatted."""

    has_explicit_accent = any(
        w["accent"] for line in lines for w in line
    )

    if not has_explicit_accent and len(lines) > 1:
        for w in lines[0]:
            w["accent"] = True

    return lines


def line_width(line, space_width):
    if not line:
        return 0
    return sum(w["width"] for w in line) + space_width * (len(line) - 1)


# --------------------------------------------------
# Dynamic Font Fitting
# --------------------------------------------------

def fit_layout(quote, theme_name, add_quotes=True):

    dummy = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(dummy)

    tokens = tokenize_accents(quote.strip())

    if add_quotes:
        tokens = apply_quote_marks(tokens)

    size = 86
    spacing_ratio = 0.14

    while size >= 34:

        font = get_font(size, theme_name, text=quote)
        emoji_font = get_emoji_font(size)

        lines, space_width = wrap_words(tokens, font, emoji_font, draw, CONTENT_WIDTH)

        lh = line_height_for(font, draw)
        spacing = int(size * spacing_ratio)

        block_w = max((line_width(line, space_width) for line in lines), default=0)
        block_h = len(lines) * lh + max(0, len(lines) - 1) * spacing

        if block_w <= CONTENT_WIDTH and block_h <= 900:
            lines = apply_auto_highlight(lines)
            return (font, emoji_font, lines, block_w, block_h, spacing, lh, space_width)

        size -= 2

    font = get_font(34, theme_name, text=quote)
    emoji_font = get_emoji_font(34)

    lines, space_width = wrap_words(tokens, font, emoji_font, draw, CONTENT_WIDTH)
    lh = line_height_for(font, draw)

    block_w = max((line_width(line, space_width) for line in lines), default=0)
    block_h = len(lines) * lh + max(0, len(lines) - 1) * 10

    lines = apply_auto_highlight(lines)

    return (font, emoji_font, lines, block_w, block_h, 10, lh, space_width)


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
# Build Render Layout
# --------------------------------------------------

def build_layout(lines, x, y, block_w, line_h, spacing, space_width):
    """Flattens wrapped lines into a list of draw instructions:
    (draw_x, draw_y, run_text, font_used, is_accent)."""

    layout = []
    cursor_y = y

    for line in lines:

        lw = line_width(line, space_width)
        cursor_x = x + (block_w - lw) // 2

        for i, word in enumerate(line):

            for run_text, font_used, run_w in word["runs"]:
                layout.append((cursor_x, cursor_y, run_text, font_used, word["accent"]))
                cursor_x += run_w

            if i < len(line) - 1:
                cursor_x += space_width

        cursor_y += line_h + spacing

    return layout


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
# Side Accent Bar (matches the vertical color-bar style
# seen in some reference reels) â€” opt-in via theme key.
# --------------------------------------------------

def draw_side_accent_bar(img, x, y, h, color):

    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    painter = ImageDraw.Draw(layer)

    bar_w = 7
    bar_x = x - 28

    painter.rounded_rectangle(
        (bar_x, y, bar_x + bar_w, y + h),
        radius=4,
        fill=(*color[:3], 255),
    )

    img.alpha_composite(layer)


# --------------------------------------------------
# Large Decorative Quote Mark (magazine-style accent,
# drawn faint behind the text block) â€” opt-in via theme key.
# --------------------------------------------------

def draw_big_quote_mark(img, x, y, block_h, color):

    mark_size = max(80, int(block_h * 0.55))

    font = get_font(mark_size, theme_name="default", text=None)

    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    painter = ImageDraw.Draw(layer)

    painter.text(
        (x - 18, y - int(mark_size * 0.62)),
        "\u201c",
        font=font,
        fill=(*color[:3], 70),
    )

    img.alpha_composite(layer)


# --------------------------------------------------
# Soft Drop Shadow (premium, matches reference reels â€”
# each theme already defines shadow_color/shadow_blur;
# this replaces the old hard 8-directional stroke that
# ignored those values and made every theme look identical)
# --------------------------------------------------

def draw_soft_shadow(img, layout, shadow_color, blur_radius):

    if blur_radius <= 0:
        return

    offset = max(2, blur_radius // 2)

    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    painter = ImageDraw.Draw(layer)

    r, g, b = shadow_color[:3]

    for draw_x, draw_y, run_text, font_used, _accent in layout:
        painter.text(
            (draw_x, draw_y + offset),
            run_text,
            font=font_used,
            fill=(r, g, b, 180),
        )

    layer = layer.filter(ImageFilter.GaussianBlur(blur_radius))

    img.alpha_composite(layer)


# Optional hard outline â€” off by default (no theme sets "stroke"),
# kept for anyone who explicitly wants a poster/meme-style outline
# instead of a soft shadow.
def draw_stroke(draw, layout, stroke_width, stroke_color):

    for draw_x, draw_y, run_text, font_used, _accent in layout:
        for ox in range(-stroke_width, stroke_width + 1):
            for oy in range(-stroke_width, stroke_width + 1):

                if ox == 0 and oy == 0:
                    continue

                draw.text(
                    (draw_x + ox, draw_y + oy),
                    run_text,
                    font=font_used,
                    fill=stroke_color,
                )


def draw_main_text(draw, layout, text_color, accent_color):

    for draw_x, draw_y, run_text, font_used, accent in layout:
        draw.text(
            (draw_x, draw_y),
            run_text,
            font=font_used,
            fill=accent_color if accent else text_color,
        )


# --------------------------------------------------
# Main Typography Renderer
# --------------------------------------------------

def draw_text(img, quote, theme_name, theme, output_path):
    """
    img must be an RGBA Pillow Image.
    Renders the wrapped/fitted quote onto img, applies optional card
    background, side accent bar, decorative quote mark, soft shadow (or
    hard outline if explicitly requested), two-tone accent-word/first-line
    highlighting, emoji-aware inline glyphs, accent line and watermark,
    then saves to output_path.
    """

    draw = ImageDraw.Draw(img)

    add_quotes = theme.get("quote_marks", False)

    (
        font,
        emoji_font,
        lines,
        block_w,
        block_h,
        spacing,
        line_h,
        space_width,
    ) = fit_layout(quote, theme_name, add_quotes=add_quotes)

    x, y = calculate_position(block_w, block_h, theme)

    text_color = theme.get("text_color", (255, 255, 255))
    accent_color = theme.get("accent_color", text_color)

    # Glass card background (optional)
    draw_card(img, x, y, block_w, block_h, theme)
    draw = ImageDraw.Draw(img)

    # Large decorative quote mark behind the text (optional, premium touch)
    if theme.get("big_quote_mark", False):
        draw_big_quote_mark(img, x, y, block_h, accent_color)
        draw = ImageDraw.Draw(img)

    layout = build_layout(lines, x, y, block_w, line_h, spacing, space_width)

    # Soft shadow (default, premium look) or hard outline (opt-in)
    stroke_width = theme.get("stroke", 0)

    if stroke_width > 0:
        draw_stroke(draw, layout, stroke_width, theme.get("stroke_color", (0, 0, 0)))
    else:
        draw_soft_shadow(img, layout, theme.get("shadow_color", (0, 0, 0)), theme.get("shadow_blur", 4))
        draw = ImageDraw.Draw(img)

    # Main two-tone text (accent-marked / auto-highlighted words in accent_color)
    draw_main_text(draw, layout, text_color, accent_color)

    # Side accent bar (optional, matches the vertical color-bar reference style)
    if theme.get("side_accent_bar", False):
        draw_side_accent_bar(img, x, y, block_h, accent_color)
        draw = ImageDraw.Draw(img)

    # Accent line
    if theme.get("accent_line", False):

        line_w = int(block_w * 0.55)
        lx = (WIDTH - line_w) // 2
        ly = y + block_h + 70

        draw.rounded_rectangle(
            (lx, ly, lx + line_w, ly + 8),
            radius=8,
            fill=accent_color,
        )

    # Watermark
    watermark = theme.get("watermark")

    if watermark:

        wm_font = get_font(34, theme_name, text=watermark)
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

    Supports:
      - Auto Devanagari font routing (Hindi renders correctly)
      - Auto emoji rendering, inline with text
      - Two-tone accent-word highlighting via **word** markup in the
        quote text, or automatic first-line highlighting if no markup
        is present
    """

    theme = get_theme(theme_name, preset_name)

    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))

    output_path = TEMP_DIR / f"quote_{uuid.uuid4().hex}.png"

    return draw_text(img, quote, theme_name, theme, str(output_path))
