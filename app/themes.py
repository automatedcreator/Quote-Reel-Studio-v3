"""
Quote Reel Studio
Theme Engine
"""

# ----------------------------------------
# Base Theme
# ----------------------------------------

BASE_THEME = {
    "font": "Inter-Bold.ttf",
    "font_size": 72,
    "text_color": "white",
    "shadow_color": "black",
    "overlay_opacity": 0.30,
    "animation": "slide_up",
    "zoom": 0.08,
    "brightness": 1.05,
    "line_spacing": 15,
    "text_width": 850,
}

# ----------------------------------------
# Apple
# ----------------------------------------

APPLE = {
    **BASE_THEME,

    "name": "Apple",

    "font": "SF-Pro-Display-Bold.otf",

    "font_size": 74,

    "text_color": "white",

    "overlay_opacity": 0.38,

    "animation": "fade",

    "zoom": 0.06,

    "brightness": 1.02,
}

# ----------------------------------------
# Minimal
# ----------------------------------------

MINIMAL = {
    **BASE_THEME,

    "name": "Minimal",

    "font_size": 70,

    "overlay_opacity": 0.25,

    "animation": "fade",

    "zoom": 0.05,
}

# ----------------------------------------
# Luxury
# ----------------------------------------

LUXURY = {
    **BASE_THEME,

    "name": "Luxury",

    "font": "PlayfairDisplay-Bold.ttf",

    "font_size": 76,

    "text_color": "#F6D36B",

    "overlay_opacity": 0.45,

    "animation": "zoom_in",

    "zoom": 0.05,

    "brightness": 0.95,
}

# ----------------------------------------
# Motivation
# ----------------------------------------

MOTIVATION = {
    **BASE_THEME,

    "name": "Motivation",

    "font_size": 80,

    "overlay_opacity": 0.32,

    "animation": "bounce",

    "zoom": 0.10,

    "brightness": 1.12,
}
# ----------------------------------------
# Stoic
# ----------------------------------------

STOIC = {
    **BASE_THEME,

    "name": "Stoic",

    "font": "Cinzel-Bold.ttf",

    "font_size": 74,

    "text_color": "#F2F2F2",

    "overlay_opacity": 0.50,

    "animation": "slide_up",

    "zoom": 0.04,

    "brightness": 0.90,
}

# ----------------------------------------
# Podcast
# ----------------------------------------

PODCAST = {
    **BASE_THEME,

    "name": "Podcast",

    "font": "Inter-Bold.ttf",

    "font_size": 68,

    "text_color": "white",

    "overlay_opacity": 0.55,

    "animation": "slide_up",

    "zoom": 0.05,

    "brightness": 0.95,
}

# ----------------------------------------
# Finance
# ----------------------------------------

FINANCE = {
    **BASE_THEME,

    "name": "Finance",

    "font": "Montserrat-Bold.ttf",

    "font_size": 72,

    "text_color": "#D7F205",

    "overlay_opacity": 0.40,

    "animation": "zoom_in",

    "zoom": 0.07,

    "brightness": 1.00,
}

# ----------------------------------------
# Neon
# ----------------------------------------

NEON = {
    **BASE_THEME,

    "name": "Neon",

    "font": "Orbitron-Bold.ttf",

    "font_size": 72,

    "text_color": "#00F5FF",

    "overlay_opacity": 0.45,

    "animation": "zoom_in",

    "zoom": 0.08,

    "brightness": 1.08,
}

# ----------------------------------------
# Theme Registry
# ----------------------------------------

THEMES = {
    "apple": APPLE,
    "minimal": MINIMAL,
    "luxury": LUXURY,
    "motivation": MOTIVATION,
    "stoic": STOIC,
    "podcast": PODCAST,
    "finance": FINANCE,
    "neon": NEON,
}

DEFAULT_THEME = "apple"


def get_theme(name="apple"):
    """
    Returns theme dictionary.
    Falls back to Apple theme.
    """
    return THEMES.get(
        str(name).lower(),
        APPLE
    )


def list_themes():
    return list(THEMES.keys())