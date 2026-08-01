"""
Theme Definitions
"""

THEMES = {
    "poetry": {
        "font_size": 60,
        "font_color": (255, 255, 255),
        "shadow": True,
        "shadow_color": (0, 0, 0, 180),
        "shadow_offset": 4,
        "line_spacing": 20,
        "max_text_width": 760,
        "text_position": 0.42,
        "overlay_opacity": 0.35,
    },

    "minimal": {
        "font_size": 54,
        "font_color": (255, 255, 255),
        "shadow": False,
        "shadow_color": None,
        "shadow_offset": 0,
        "line_spacing": 18,
        "max_text_width": 820,
        "text_position": 0.45,
        "overlay_opacity": 0.20,
    }
}


def get_theme(name="poetry"):
    """Return a theme by name."""
    return THEMES.get(name, THEMES["poetry"])


def list_themes():
    """Return all available theme names."""
    return list(THEMES.keys())
